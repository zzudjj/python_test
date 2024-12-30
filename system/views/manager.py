import json
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from system import models
from system.utils.modelform import SiteAdd, LineAdd, LineEdit, BusAdd, BusEdit, DriverAdd, DriverEdit, WorkAdd
from django.views.decorators.csrf import csrf_exempt
from system.utils.encryption import md5


def homepage(request):
    return render(request, 'manager_homepage.html')


def line_manager(request):
    form = []
    search_result = models.Line.objects.all().order_by('id')
    for line in search_result:
        search_start = models.Contain.objects.filter(line=line, last_site=None).first()
        search_end = models.Contain.objects.filter(line=line, next_site=None).first()
        data = {"id": line.id, "start_site": search_start.site.name, "end_site": search_end.site.name}
        form.append(data)
    return render(request, 'line_manage.html', {'form': json.dumps(form)})


@csrf_exempt
def line_add(request,):
    if request.method == 'GET':
        form = LineAdd()
        data = []
        search_result = models.Site.objects.all().order_by('id')
        for site in search_result:
            data1 = {"value": site.id, "title": site.name}
            data.append(data1)
        return render(request, 'line_add.html', {'form': form, 'data': data})
    form = LineEdit(data=request.POST)
    if form.is_valid():
        form.save()
        line_data = request.POST.dict()
        last_site_id = -1
        next_site_id = -1
        for i in range(int((len(line_data)-1)/2)):
            if i == int((len(line_data)-1)/2)-1:
                next_site_id = -1
            else:
                next_site_id = line_data[f'site_data[{i+1}][value]']
            site_id = line_data[f'site_data[{i}][value]']
            line_id = line_data['id']
            next_site = models.Site.objects.filter(id=next_site_id).first()
            line = models.Line.objects.filter(id=line_id).first()
            site = models.Site.objects.filter(id=site_id).first()
            last_site = models.Site.objects.filter(id=last_site_id).first()
            models.Contain.objects.create(site=site, line=line, last_site=last_site, next_site=next_site)
            last_site_id = line_data[f'site_data[{i}][value]']
        data_dirct = {'status': True}
        return HttpResponse(json.dumps(data_dirct))
    data_dirct = {'status': False, 'errors':form.errors}
    return HttpResponse(json.dumps(data_dirct, ensure_ascii=False))


@csrf_exempt
def line_edit(request, nid):
    if request.method == 'GET':
        line = models.Line.objects.filter(id=nid).first()
        form = LineEdit(instance=line)
        left_data = []
        right_data = []
        search_result_left = models.Site.objects.all().order_by('id')
        search_result_right = models.Contain.objects.filter(line=line).order_by('id')
        search_start = models.Contain.objects.filter(line=line, last_site=None).first()
        for site in search_result_left:
            data = {"value": site.id, "title": site.name}
            left_data.append(data)
        next_site_id = search_start.next_site.id
        right_data.append(search_start.site.id)
        right_data.append(next_site_id)
        while next_site_id != -1:
            for contain in search_result_right:
                if next_site_id == contain.site.id:
                    if contain.next_site:
                        next_site_id = contain.next_site.id
                        right_data.append(next_site_id)
                    else:
                        next_site_id = -1
        return render(request, 'line_edit.html', {'form': form, 'left_data': left_data, 'right_data': right_data, 'nid': nid})
    line_now = models.Line.objects.filter(id=nid).first()
    models.Contain.objects.filter(line=line_now).delete()
    line_data = request.POST.dict()
    last_site_id = -1
    next_site_id = -1
    for i in range(int((len(line_data) - 1) / 2)):
        if i == int((len(line_data) - 1) / 2) - 1:
            next_site_id = -1
        else:
            next_site_id = line_data[f'site_data[{i + 1}][value]']
        site_id = line_data[f'site_data[{i}][value]']
        line_id = line_data['id']
        next_site = models.Site.objects.filter(id=next_site_id).first()
        line = models.Line.objects.filter(id=line_id).first()
        site = models.Site.objects.filter(id=site_id).first()
        last_site = models.Site.objects.filter(id=last_site_id).first()
        models.Contain.objects.create(site=site, line=line, last_site=last_site, next_site=next_site)
        last_site_id = line_data[f'site_data[{i}][value]']
    data_dirct = {'status': True}
    print("成功")
    return HttpResponse(json.dumps(data_dirct))


def line_delete(request, nid):
    models.Line.objects.filter(id=nid).delete()
    return redirect('/manager/line_manage')


def line_view(request, nid):
    search_data = models.LineView.objects.filter(line_id=nid)
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
    return render(request, 'line_view.html', {'nid': nid, 'data': data})


def site_manager(request):
    form = []
    search_result = models.Site.objects.all().order_by('id')
    for site in search_result:
        data = {"id": site.id, "name": site.name}
        form.append(data)
    return render(request, 'site_manage.html', {'form': json.dumps(form)})


@csrf_exempt
def site_add(request):
    if request.method == 'GET':
        form = SiteAdd()
        return render(request,'site_add.html',{'form': form})
    form = SiteAdd(data=request.POST)
    if form.is_valid():
        form.save()
        data_dirct = {'status': True}
        return HttpResponse(json.dumps(data_dirct))
    data_dirct = {'status': False, 'errors': form.errors}
    return HttpResponse(json.dumps(data_dirct, ensure_ascii=False))


def site_edit(request, nid):
    data = models.Site.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = SiteAdd(instance=data)
        return render(request, 'site_edit.html', {'form': form})
    form = SiteAdd(data=request.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/manager/site_manage')
    return render(request, 'site_edit.html', {'form': form})


def site_delete(request, nid):
    models.Site.objects.filter(id=nid).delete()
    return redirect('/manager/site_manage')


def site_view(request, nid):
    data = models.LineView.objects.filter(site_id=nid)
    name = models.Site.objects.filter(id=nid).first().name
    return render(request, 'line_of_site.html', {'name': name, 'data': data})


@csrf_exempt
def site_search(request):
    search_text = request.POST.get('search_text')
    search_result = models.Site.objects.filter(name__icontains=search_text).order_by('id')
    data = []
    for site in search_result:
        data.append({"id": site.id, "name": site.name})
    data_dirct = {'status': True, 'data': data}
    return HttpResponse(json.dumps(data_dirct))


def bus_manager(request):
    form = []
    search_result = models.Bus.objects.all().order_by('plate_number')
    for bus in search_result:
        data = {"plate_number": bus.plate_number, "passenger_capacity": bus.passenger_capacity, 'line': bus.line.id}
        form.append(data)
    return render(request, 'bus_manage.html', {'form': json.dumps(form)})


@csrf_exempt
def bus_add(request):
    if request.method == 'GET':
        form = BusAdd()
        return render(request, 'bus_add.html', {'form': form})
    form = BusAdd(data=request.POST)
    if form.is_valid():
        form.save()
        data_dirct = {'status': True}
        return HttpResponse(json.dumps(data_dirct))
    data_dirct = {'status': False, 'errors': form.errors}
    print(form.errors)
    print(type(form.errors))
    return HttpResponse(json.dumps(data_dirct, ensure_ascii=False))


def bus_edit(request, nid):
    data = models.Bus.objects.filter(plate_number=nid).first()
    if request.method == 'GET':
        form = BusEdit(instance=data)
        return render(request, 'bus_edit.html', {'form': form})
    form = BusEdit(data=request.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/manager/bus_manage')
    return render(request, 'bus_edit.html', {'form': form})


def bus_delete(request, nid):
    models.Bus.objects.filter(plate_number=nid).delete()
    return redirect('/manager/bus_manage')


@csrf_exempt
def bus_search(request):
    search_text = request.POST.get('search_text')
    line = models.Line.objects.filter(id=search_text).first()
    search_result = models.Bus.objects.filter(line=line).order_by('plate_number')
    data = []
    for bus in search_result:
        data.append({"plate_number": bus.plate_number, "passenger_capacity": bus.passenger_capacity, 'line': bus.line.id})
    data_dirct = {'status': True, 'data': data}
    return HttpResponse(json.dumps(data_dirct))


def driver_message_manage(request):
    form = []
    search_result = models.DriverView.objects.all().order_by('id')
    for driver_view in search_result:
        data = {'id': driver_view.id, 'name': driver_view.name, 'sex': driver_view.sex, 'telephone': driver_view.telephone}
        form.append(data)
    return render(request, 'driver_message_manage.html', {'form': json.dumps(form)})


@csrf_exempt
def driver_message_add(request):
    if request.method == 'GET':
        return render(request, 'driver_message_add.html')
    name = request.POST.get('name')
    sex = request.POST.get('sex')
    models.Driver.objects.create(name=name, sex=sex)
    driver = models.Driver.objects.latest('id')
    id = driver.id
    password = driver.password
    models.Driver.objects.filter(id=id).update(password=md5(password))
    telephone_first = request.POST.get('telephone_first')
    telephone_second = request.POST.get('telephone_second')
    driver_new = models.Driver.objects.filter(id=id).first()
    models.DriverTelephone.objects.create(telephone=telephone_first, driver=driver_new)
    if telephone_second:
        models.DriverTelephone.objects.create(telephone=telephone_second, driver=driver_new)
    data_dirct = {'status': True}
    return HttpResponse(json.dumps(data_dirct))


def driver_message_edit(request, nid):
    data = models.Driver.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = DriverEdit(instance=data)
        telephone = models.DriverTelephone.objects.filter(driver=data).order_by('telephone')
        phone_number = []
        for tel in telephone:
            phone_number.append(tel.telephone)
        telephone_first = phone_number[0]
        telephone_second = ""
        if int(len(phone_number)) > 1:
            telephone_second = phone_number[0]
            telephone_first = phone_number[1]
        return render(request, 'driver_message_edit.html', {'form': form, 'telephone_first': telephone_first, 'telephone_second': telephone_second})
    form = DriverEdit(data=request.POST, instance=data)
    models.DriverTelephone.objects.filter(driver=data).delete()
    if form.is_valid():
        form.save()
        telephone_first = request.POST.get('telephone_first')
        telephone_second = request.POST.get('telephone_second')
        models.DriverTelephone.objects.create(telephone=telephone_first, driver=data)
        if telephone_second:
            models.DriverTelephone.objects.create(telephone=telephone_second, driver=data)
        return redirect('/manager/driver_message_manage')
    return render(request, 'driver_message_edit.html', {'form': form})


def driver_message_delete(request, nid):
    models.Driver.objects.filter(id=nid).delete()
    return redirect('/manager/driver_message_manage')


@csrf_exempt
def driver_message_search(request):
    search_text = request.POST.get('search_text')
    driver_view = models.DriverView.objects.filter(name__icontains=search_text).order_by('id')
    data = []
    for driver in driver_view:
        data.append({'id': driver.id, 'name': driver.name, 'sex': driver.sex, 'telephone': driver.telephone})
    data_dirct = {'status': True, 'data': data}
    return HttpResponse(json.dumps(data_dirct))


def driver_work_manage(request):
    form = []
    search_result = models.WorkView.objects.all().order_by('driver_id')
    for work_view in search_result:
        data = {'id': work_view.id ,'driver_id': work_view.driver_id, 'name':work_view.name, 'plate_number': work_view.plate_number_id, 'start_time':work_view.start_time.strftime('%Y-%m-%d %H:%M:%S'), 'end_time': work_view.end_time.strftime('%Y-%m-%d %H:%M:%S')}
        form.append(data)
    return render(request, 'driver_work_manage.html', {'form': json.dumps(form)})


@csrf_exempt
def driver_work_add(request):
    if request.method == 'GET':
        form = WorkAdd()
        return render(request, 'driver_work_add.html', {'form': form})
    form = WorkAdd(data=request.POST)
    if form.is_valid():
        form.save()
        data_dirct = {'status': True}
        return HttpResponse(json.dumps(data_dirct))
    data_dirct = {'status': False, 'errors': form.errors}
    return HttpResponse(json.dumps(data_dirct, ensure_ascii=False))


def driver_work_edit(request, nid):
    data = models.Drive.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = WorkAdd(instance=data)
        return render(request, 'driver_work_edit.html', {'form': form})
    form = WorkAdd(data=request.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/manager/driver_work_manage')
    return render(request, 'driver_work_edit.html', {'form': form})


def driver_work_delete(request, nid):
    models.Drive.objects.filter(id=nid).delete()
    return redirect('/manager/driver_work_manage')


@csrf_exempt
def driver_work_search(request):
    search_text = request.POST.get('search_text')
    data = []
    search_result = models.WorkView.objects.filter(name__contains=search_text).order_by('driver_id')
    for work_view in search_result:
        data1 = {'id': work_view.id, 'driver_id': work_view.driver_id, 'name': work_view.name,
                'plate_number': work_view.plate_number_id,
                'start_time': work_view.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': work_view.end_time.strftime('%Y-%m-%d %H:%M:%S')}
        data.append(data1)
    data_dirct = {'status': True, 'data': data}
    return HttpResponse(json.dumps(data_dirct))


def violation(request):
    form = []
    data = models.ViolationView.objects.filter(status=0)
    status_dict = {0: '未处理'}
    for each in data:
        form.append(
            {'id': each.id, 'title': each.title, 'status': status_dict[each.status]})
    return render(request, 'violation_manage.html', {'form': json.dumps(form)})


@csrf_exempt
def violation_solve(request, nid):
    data = models.ViolationView.objects.filter(id=nid).first()
    if request.method == 'GET':
        title = data.title
        text = data.text
        driver_id = data.driver_id
        passenger_tel = data.passenger_tel_id
        data_dict = {'title': title, 'text': text, 'driver_id': driver_id, 'passenger_tel': passenger_tel, 'id': nid}
        return render(request,'violation_solve.html', data_dict)
    status = request.POST.get('status')
    info = request.session.get("info")
    manager_id = info['id']
    manager = models.Manager.objects.filter(id=manager_id).first()
    models.Violation.objects.filter(id=nid).update(status=status,manager=manager)
    data_dict = {'status': True}
    return HttpResponse(json.dumps(data_dict))


def announcement(request):
    form = []
    data = models.AnnouncementView.objects.all()
    for each in data:
        form.append(
            {'id': each.id, 'title': each.title, 'date': each.date.strftime('%Y-%m-%d')})
    return render(request, 'manager_announcement.html', {'form': json.dumps(form)})


def announcement_view(request, nid):
    notice = models.AnnouncementView.objects.filter(id=nid).first()
    title = notice.title
    text = notice.text
    return render(request,'manager_announcement_view.html',{'title': title, 'text': text})


def announcement_release(request):
    data_dict = {'status': False}
    if request.method == 'GET':
        date = datetime.now().strftime('%Y-%m-%d')
        return render(request,'manager_announcement_release.html',{'data': json.dumps(data_dict),'date': date})
    info = request.session.get('info')
    manager_id = info['id']
    manager = models.Manager.objects.filter(id=manager_id).first()
    title = request.POST.get('title')
    text = request.POST.get('text')
    date = request.POST.get('date')
    print(date)
    date = datetime.strptime(date, '%Y-%m-%d')
    models.Announcement.objects.create(title=title, text=text, manager=manager, date=date)
    data_dict['status'] = True
    return render(request,'manager_announcement_release.html',{'data': json.dumps(data_dict)})


@csrf_exempt
def message(request):
    info = request.session.get('info')
    manager = models.Manager.objects.filter(id=info['id']).first()
    if request.method == 'GET':
        name = manager.name
        telephone = models.ManagerTelephone.objects.filter(manager=manager).first()
        telephone_second = models.ManagerTelephone.objects.filter(manager=manager).last()
        if telephone == telephone_second:
            telephone_second = ""
            if not telephone:
                telephone = ""
            else:
                telephone = telephone.telephone
        else:
            telephone_second = telephone_second.telephone
        date = {'name': name, 'telephone': telephone, 'telephone_second': telephone_second}
        return render(request, 'manager_message.html', date)
    password_confirm = request.POST.get('password_confirm')
    if md5(password_confirm) == manager.password:
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        telephone_second = request.POST.get('telephone_second')
        password_new = request.POST.get('password_new')
        models.Manager.objects.filter(id=info['id']).update(name=name)
        models.ManagerTelephone.objects.filter(manager=manager).delete()
        if telephone:
            models.ManagerTelephone.objects.create(manager=manager,telephone=telephone)
        if telephone_second:
            models.ManagerTelephone.objects.create(manager=manager,telephone=telephone_second)
        if password_new:
            password_new = md5(password_new)
            models.Manager.objects.filter(id=info['id']).update(password=password_new)
        return HttpResponse(json.dumps({'status': True}))
    else:
        return HttpResponse(json.dumps({'status': False}))