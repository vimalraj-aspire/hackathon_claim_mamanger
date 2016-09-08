from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from department.models import EmployeeRole
from claims_manager import settings
from models import ResourceRequest
from serializers import ResourceRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from claim.views import get_user_department
from decorators import has_manger_permission
from rest_framework.decorators import api_view
from department.models import Department
from notification.models import Notification
from django.contrib.auth.models import User


def get_user_department(user):
  '''
    Returns department id of user
  '''
  return EmployeeRole.objects.filter(employee=user).values('department')[0].get('department')


def get_department_manager(department):
  return User.objects.get(id=EmployeeRole.objects.filter(department=department, role=settings.ROLES.get('MANAGER')).values('employee')[0].get('employee'))


def get_requests(user):
  '''
  Function to return the available claims of user, If requester is a manager 
  it will return all the claims on the departments of the manager
  '''
  user_departments = EmployeeRole.objects.filter(employee=user, role=settings.ROLES.get('MANAGER')).values_list('department')
  if not user_departments:
    requests = ResourceRequest.objects.filter(owner=user)
  else:          
    requests = ResourceRequest.objects.filter(department=user_departments).exclude(state=settings.REQUEST_STATE.get('DRAFT'))
  return requests


class RequestList(APIView): 
    ''' Returns list of requests and create a request instance'''
    def get(self, request, format=None):
        
        requests = get_requests(self.request.user)
        serializer = ResourceRequestSerializer(requests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
      request.POST._mutable = True
      serializer_data = request.data
      serializer_data['owner'] = self.request.user
      serializer_data['department'] = get_user_department(self.request.user)
      serializer = ResourceRequestSerializer(data=serializer_data)

      if serializer.is_valid():
        resource_request = serializer.save(owner=self.request.user)
        Notification.objects.create(owner=get_department_manager(get_user_department(self.request.user)), request=resource_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDetail(APIView):
    ''' Class based view to perform retreive, udate and delete a claim'''
    def get_object(self, request_id):
        try:
            return ResourceRequest.objects.get(id=request_id)
        except ResourceRequest.DoesNotExist:
            raise Http404

    def get(self, request, request_id, format=None):
        claim = self.get_object(request_id)
        serializer = ResourceRequestSerializer(claim)
        return Response(serializer.data)

    def delete(self, request, request_id, format=None):
        claim = self.get_object(request_id)
        claim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@has_manger_permission
def reject_request(request, request_id):
  try:
    resource_request = ResourceRequest.objects.get(id=request_id)
    resource_request.state = settings.REQUEST_STATE.get('REJECTED')
    resource_request.processed_by = request.user
    resource_request.save()
    Notification.objects.create(owner=resource_request.owner, request=resource_request)
    return Response({'status': 'success', 'msg': settings.API_ERRORS.get('REQUEST_REJECTED')})
  except ResourceRequest.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('REQUEST_NOT_AVAILABLE')}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@has_manger_permission
def approve_request(request, request_id):
  ''' Approves resource request, needs manager permission'''
  try:
    resource_request = ResourceRequest.objects.get(id=request_id)
    if resource_request.department.id in [3, 4, 5]:
      resource_request.state = settings.REQUEST_STATE.get('APPROVED')
      resource_request.processed_by = request.user
      resource_request.save()
      Notification.objects.create(owner=resource_request.owner, request=resource_request)
      return Response({'status': 'success', 'msg': settings.API_ERRORS.get('REQUEST_APPROVED')})
    else:
      if resource_request.flight_from and resource_request.flight_to:
        ResourceRequest.objects.create(owner=resource_request.owner, department=Department.objects.get(id=settings.DEPARTMENT.get('FACILITIES')), passport= resource_request.passport, visa=resource_request.visa, travel_date=resource_request.travel_date, insurance_required= resource_request.insurance_required)
      if resource_request.laptop_config:
        ResourceRequest.objects.create(owner=resource_request.owner, department=Department.objects.get(id=settings.DEPARTMENT.get('SYSADMIN')),laptop_config=resource_request.laptop_config, laptop_short_term= resource_request.laptop_short_term, laptop_long_term=resource_request.laptop_long_term)
      if resource_request.forex_details:
        ResourceRequest.objects.create(owner=resource_request.owner, department=Department.objects.get(id=settings.DEPARTMENT.get('FACILITIES')), forex_details=resource_request.forex_details)
      resource_request.delete()
      return Response({'status': 'success', 'msg': settings.API_ERRORS.get('SUB_REQUESTS_CREATED')})
  except ResourceRequest.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('REQUEST_NOT_AVAILABLE')}, status=status.HTTP_404_NOT_FOUND)
