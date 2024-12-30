from django.shortcuts import render,redirect
from system import models
from system.utils.modelform import LoginForm,RegisterModelForm
from system.utils.encryption import md5


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        data = form.cleaned_data
        request.session['info'] = {'identity': request.POST.get('identity'), 'id': data['username']}
        if request.POST.get('identity') == '0':
            passenger = models.Passenger.objects.filter(telephone=data['username']).first()
            if passenger is not None and passenger.password == md5(data['password']):
                return redirect('/passenger/homepage')
            else:
                form.add_error('password','账号或密码错误')
                return render(request, 'login.html', {'form': form})
        elif request.POST.get('identity') == '1':
            driver = models.Driver.objects.filter(id=data['username']).first()
            if driver is not None and driver.password == md5(data['password']):
                return redirect('/driver/homepage')
            else:
                form.add_error('password', '账号或密码错误')
                return render(request, 'login.html', {'form': form})
        elif request.POST.get('identity') == '2':
            manager = models.Manager.objects.filter(id=data['username']).first()
            if manager is not None and manager.password == md5(data['password']):
                return redirect('/manager/homepage')
            else:
                form.add_error('password', '账号或密码错误')
                return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        modelform = RegisterModelForm()
        return render(request, 'register.html', {'modelform':modelform})
    modelform = RegisterModelForm(data=request.POST)
    if modelform.is_valid():
        modelform.save()
        return redirect('/login/')
    return render(request, 'register.html', {'modelform': modelform})


def logout(request):
    request.session.clear()
    return redirect('/login/')