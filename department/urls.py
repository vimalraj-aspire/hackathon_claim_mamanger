"""tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import EmployeeViewSet, DepartmentViewSet, EmployeeList, DepartmentDetailView, map_employee, my_details



department_list = DepartmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})



urlpatterns = [
    url(r'^my-details/$', my_details, name='employee-list'),
    url(r'^employees/$', EmployeeList.as_view(), name='employee-list'),
    url(r'^employee/(?P<id>[0-9]+)/$', EmployeeViewSet.as_view(), name='employee-detail'),
    url(r'^employee/map/(?P<id>[0-9]+)/$', map_employee, name='employee-detail'),

    url(r'^departments/$', department_list, name='department-list'),
    url(r'^department/(?P<id>[0-9]+)/$', DepartmentDetailView.as_view(), name='department-detail'),
]
