
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^get-notifications/$', views.get_notifications, name='get-notifications'),
]