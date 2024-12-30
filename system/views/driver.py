from django.shortcuts import render, redirect, HttpResponse
from system import models
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from system.utils.encryption import md5


def homepage(request):
    return render(request, 'driver_homepage.html')


def work(request):
    info = request.session.get('info')
    form = []
    time = datetime.now()
    search_result = models.WorkView.objects.filter(end_time__gt=time, driver_id=info['id']).order_by('start_time')
    for work_view in search_result:
        data = {'driver_id': work_view.driver_id, 'name': work_view.name,
                'plate_number': work_view.plate_number_id,
                'start_time': work_view.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': work_view.end_time.strftime('%Y-%m-%d %H:%M:%S')}
        form.append(data)
    return render(request, 'driver_work.html', {'form': json.dumps(form)})


def violation(request):
    info = request.session.get('info')
    form = []
    data = models.ViolationView.objects.filter(driver_id=info['id'], status=1)
    status_dict = {1: '已通过'}
    for each in data:
        form.append(
            {'id': each.id, 'title': each.title, 'manager_id': each.manager_id, 'status': status_dict[each.status]})
    return render(request, 'driver_violation.html', {'form': json.dumps(form)})


def text_view(request, nid):
    data = models.ViolationView.objects.filter(id=nid).first()
    title = data.title
    text = data.text
    return render(request,'driver_text_view.html',{'title': title, 'text': text})


def announcement(request):
    form = []
    data = models.AnnouncementView.objects.all()
    for each in data:
        form.append(
            {'id': each.id, 'title': each.title, 'date': each.date.strftime('%Y-%m-%d')})
    return render(request, 'driver_announcement.html', {'form': json.dumps(form)})


def announcement_view(request, nid):
    notice = models.AnnouncementView.objects.filter(id=nid).first()
    title = notice.title
    text = notice.text
    return render(request,'driver_announcement_view.html',{'title': title, 'text': text})


@csrf_exempt
def message(request):
    info = request.session.get('info')
    driver = models.Driver.objects.filter(id=info['id']).first()
    if request.method == 'GET':
        name = driver.name
        telephone = models.DriverTelephone.objects.filter(driver=driver).first()
        telephone_second = models.DriverTelephone.objects.filter(driver=driver).last()
        if telephone == telephone_second:
            telephone_second = ""
        date = {'name': name, 'telephone': telephone.telephone, 'telephone_second': telephone_second.telephone}
        return render(request, 'driver_message.html', date)
    password_confirm = request.POST.get('password_confirm')
    if md5(password_confirm) == driver.password:
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        telephone_second = request.POST.get('telephone_second')
        password_new = request.POST.get('password_new')
        models.Driver.objects.filter(id=info['id']).update(name=name)
        models.DriverTelephone.objects.filter(driver=driver).delete()
        models.DriverTelephone.objects.create(driver=driver,telephone=telephone)
        if telephone_second:
            models.DriverTelephone.objects.create(driver=driver,telephone=telephone_second)
        if password_new:
            password_new = md5(password_new)
            models.Driver.objects.filter(id=info['id']).update(password=password_new)
        return HttpResponse(json.dumps({'status': True}))
    else:
        return HttpResponse(json.dumps({'status': False}))