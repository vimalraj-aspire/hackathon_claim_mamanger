from django.shortcuts import render
from models import Notification
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serializers import NotificationSerializer
from copy import deepcopy


@api_view(['GET'])
def get_notifications(request):
  notifications = Notification.objects.filter(owner=request.user, is_notified=False)
  serializer = NotificationSerializer(notifications, many=True)
  data =  serializer.data
  Notification.objects.filter(owner=request.user).update(is_notified=True)
  return Response(data)
