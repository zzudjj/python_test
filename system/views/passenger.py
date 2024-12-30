from django.shortcuts import render, redirect,HttpResponse
from system import models
import json
from django.views.decorators.csrf import csrf_exempt
from system.utils.encryption import md5


def homepage(request):
    return render(request, 'passenger_homepage.html')


def line_search(request):
    if request.method == 'GET':
        return render(request, 'passenger_line_search.html')
    nid = request.POST.get('line_id')
    search_data = models.LineView.objects.filter(line_id=nid)
    if not search_data:
        errors = "线路不存在"
        return render(request, 'passenger_line_search.html', {'errors': errors})
    start_data = models.LineView.objects.filter(line_id=nid, last_site_id=None).first()
    data = []
    next_site_id = start_data.next_site_id
    data.append(start_data.name)
    while next_site_id != -1:
        for contain in search_data:
            if next_site_id == contain.site_id:
                data.append(contain.name)
                if contain.next_site_id:
                    next_site_id = contain.next_site_id
                else:
                    next_site_id = -1
    return render(request, 'passenger_line_search_result.html', {'nid': nid, 'data': data})


def site_search(request):
    if request.method == 'GET':
        return render(request, 'passenger_site_search.html')
    nid = request.POST.get('site_name')
    data = models.LineView.objects.filter(name=nid)
    if not data:
        errors = "站点不存在"
        return render(request, 'passenger_site_search.html', {'errors': errors})
    name = data.first().name
    return render(request, 'passenger_site_search_result.html', {'name': name, 'data': data})


def ride_view(request):
    info = request.session.get('info')
    form = []
    data = (models.RideView.objects.filter(passenger_tel_id=info['id'])
            .order_by('-travel_time'))
    for each in data:
        form.append({'id': each.id, 'line_id': each.line_id,
                     'travel_time': each.travel_time.strftime('%Y-%m-%d %H:%M:%S')})
    return render(request, 'passenger_ride.html', {'form': json.dumps(form)})


@csrf_exempt
def ride_search(request):
    search_text = request.POST.get('search_text')
    data = []
    info = request.session.get('info')
    if search_text:
        search_result = models.RideView.objects.filter(passenger_tel_id=info['id'], line_id=int(search_text)).order_by('-travel_time')
    else:
        search_result = models.RideView.objects.filter(passenger_tel_id=info['id']).order_by('-travel_time')
    for each in search_result:
        data.append({'id': each.id, 'line_id': each.line_id, 'travel_time': each.travel_time.strftime('%Y-%m-%d %H:%M:%S')})
    data_dirct = {'status': True, 'data': data}
    return HttpResponse(json.dumps(data_dirct))


def driver_view(request, nid):
    ride_data = models.RideView.objects.filter(id=nid).first()
    work_data = models.WorkView.objects.filter(plate_number_id=ride_data.plate_number, start_time__lt=ride_data.travel_time, end_time__gt=ride_data.travel_time).first()
    driver_data = models.DriverView.objects.filter(id=work_data.driver_id).first()
    data = {'工号': driver_data.id, '姓名': driver_data.name, '性别': driver_data.sex, '电话号码': driver_data.telephone}
    return render(request, 'passenger_driver_view.html', {'data': data})


def complaint(request):
    data_dict = {'status': False}
    if request.method == 'GET':
        return render(request,'passenger_violation_complaint.html',{'data': json.dumps(data_dict)})
    driver_id = request.POST.get('driver_id')
    driver = models.Driver.objects.filter(id=driver_id).first()
    if not driver:
        return render(request,'passenger_violation_complaint.html',{'data': json.dumps(data_dict), 'errors': '该司机不存在'})
    title = request.POST.get('title')
    text = request.POST.get('text')
    info = request.session.get('info')
    passenger = models.Passenger.objects.filter(telephone=info['id']).first()
    models.Violation.objects.create(title=title, text=text, driver=driver, passenger_tel=passenger)
    data_dict['status'] = True
    return render(request,'passenger_violation_complaint.html',{'data': json.dumps(data_dict)})


def complaint_result(request):
    info = request.session.get('info')
    form = []
    data = models.ViolationView.objects.filter(passenger_tel_id=info['id'])
    status_dict = {0: '未处理', 1: '已通过', 2: '未通过'}
    for each in data:
        form.append(
            {'id': each.id, 'title': each.title, 'driver_id': each.driver_id, 'status': status_dict[each.status]})
    return render(request, 'passenger_violation_result.html', {'form': json.dumps(form)})


def text_view(request, nid):
    violation = models.ViolationView.objects.filter(id=nid).first()
    title = violation.title
    text = violation.text
    return render(request,'passenger_text_view.html',{'title': title, 'text': text})


def announcement(request):
    form = []
    data = models.AnnouncementView.objects.all()
    for each in data:
        form.append(
            {'id': each.id, 'title': each.title, 'date': each.date.strftime('%Y-%m-%d')})
    return render(request, 'passenger_announcement.html', {'form': json.dumps(form)})


def announcement_view(request, nid):
    notice = models.AnnouncementView.objects.filter(id=nid).first()
    title = notice.title
    text = notice.text
    return render(request, 'passenger_announcement_view.html', {'title': title, 'text': text})


@csrf_exempt
def message(request):
    info = request.session.get('info')
    passenger = models.Passenger.objects.filter(telephone=info['id']).first()
    if request.method == 'GET':
        name = passenger.name
        telephone = passenger.telephone
        date = {'name': name, 'telephone': telephone}
        return render(request, 'passenger_message.html',date)
    password_confirm = request.POST.get('password_confirm')
    if md5(password_confirm) == passenger.password:
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        password_new = request.POST.get('password_new')
        models.Passenger.objects.filter(telephone=info['id']).update(name=name, telephone=telephone)
        if password_new:
            password_new = md5(password_new)
            models.Passenger.objects.filter(telephone=info['id']).update(password=password_new)
        return HttpResponse(json.dumps({'status': True}))
    else:
        return HttpResponse(json.dumps({'status': False}))







