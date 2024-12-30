"""
URL configuration for PublicTransport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from system.views import public
from system.views import passenger
from system.views import driver
from system.views import manager
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', public.login),
    path('register/', public.register),
    path('logout/', public.logout),

    # 乘客
    path('passenger/homepage', passenger.homepage),
    path('passenger/line_search', passenger.line_search),
    path('passenger/site_search', passenger.site_search),
    path('passenger/ride_view', passenger.ride_view),
    path('passenger/ride_search', passenger.ride_search),
    path('passenger/ride_view/<int:nid>/driver_view', passenger.driver_view),
    path('passenger/complaint', passenger.complaint),
    path('passenger/complaint_result', passenger.complaint_result),
    path('passenger/complaint_result/<int:nid>/text_view', passenger.text_view),
    path('passenger/announcement', passenger.announcement),
    path('passenger/announcement/<int:nid>/announcement_view', passenger.announcement_view),
    path('passenger/message', passenger.message),

    # 司机
    path('driver/homepage', driver.homepage),
    path('driver/work', driver.work),
    path('driver/violation', driver.violation),
    path('driver/violation/<int:nid>/text_view', driver.text_view),
    path('driver/announcement', driver.announcement),
    path('driver/announcement/<int:nid>/announcement_view', driver.announcement_view),
    path('driver/message', driver.message),

    # 管理员
    path('manager/homepage', manager.homepage),
    path('manager/line_manage', manager.line_manager),
    path('manager/line_manage/line_add', manager.line_add),
    path('manager/line_manage/<int:nid>/line_edit', manager.line_edit),
    path('manager/line_manage/<int:nid>/line_delete', manager.line_delete),
    path('manager/line_manage/<int:nid>/line_view', manager.line_view),
    path('manager/site_manage', manager.site_manager),
    path('manager/site_manage/site_add', manager.site_add),
    path('manager/site_manage/<int:nid>/site_edit', manager.site_edit),
    path('manager/site_manage/<int:nid>/site_delete', manager.site_delete),
    path('manager/site_manage/<int:nid>/site_view', manager.site_view),
    path('manager/site_manage/site_search', manager.site_search),
    path('manager/bus_manage', manager.bus_manager),
    path('manager/bus_manage/bus_add', manager.bus_add),
    path('manager/bus_manage/<str:nid>/bus_edit', manager.bus_edit),
    path('manager/bus_manage/<str:nid>/bus_delete', manager.bus_delete),
    path('manager/bus_manage/bus_search', manager.bus_search),
    path('manager/driver_message_manage', manager.driver_message_manage),
    path('manager/driver_message_manage/driver_message_add', manager.driver_message_add),
    path('manager/driver_message_manage/<str:nid>/driver_message_delete', manager.driver_message_delete),
    path('manager/driver_message_manage/<str:nid>/driver_message_edit', manager.driver_message_edit),
    path('manager/driver_message_manage/driver_message_search', manager.driver_message_search),
    path('manager/driver_work_manage', manager.driver_work_manage),
    path('manager/driver_work_manage/driver_work_add', manager.driver_work_add),
    path('manager/driver_work_manage/<int:nid>/driver_work_delete', manager.driver_work_delete),
    path('manager/driver_work_manage/<int:nid>/driver_work_edit', manager.driver_work_edit),
    path('manager/driver_work_manage/driver_work_search', manager.driver_work_search),
    path('manager/violation', manager.violation),
    path('manager/violation/<int:nid>/violation_solve', manager.violation_solve),
    path('manager/announcement', manager.announcement),
    path('manager/announcement/<int:nid>/announcement_view', manager.announcement_view),
    path('manager/announcement_release', manager.announcement_release),
    path('manager/message', manager.message),
]
