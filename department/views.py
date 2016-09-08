
from rest_framework import viewsets
from .serializers import EmployeeSerializer, DepartmentSerializer
from django.contrib.auth.models import User
from .models import Department, EmployeeRole
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.cache import cache
import json
from claims_manager import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils.decorators import method_decorator

class EmployeeList(APIView):
    """
    List all Employees, or create a new Employee.
    """
    def get(self, request, format=None):
        user = User.objects.all().exclude(is_superuser=1)
        serializer = EmployeeSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.POST._mutable = True
        serializer = EmployeeSerializer(data=request.data)
        # Team should have one manager
        if int(request.data.get('role')) == settings.ROLES.get('MANAGER') and EmployeeRole.objects.filter(department= Department.objects.get(pk=request.data.get('department')), role=settings.ROLES.get('MANAGER')):
          return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('TEAM_ALREADY_HAVE_A_MANAGER')}, status=status.HTTP_412_PRECONDITION_FAILED)
        
        if serializer.is_valid(request.data):
            employee = serializer.save()
            EmployeeRole.objects.create(employee=employee, department= Department.objects.get(pk=request.data.get('department')), role=request.data.get('role'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(APIView):
  """
  Retrieve, update or delete a Employee instance.
  """
  def get_object(self, id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404

  def get(self, request, id, format=None):
    user = self.get_object(id)
    serializer = EmployeeSerializer(user)
    return Response(serializer.data)

  def put(self, request, id, format=None):
    user = self.get_object(id)
    serializer = EmployeeSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id, format=None):
    user = self.get_object(id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentViewSet(viewsets.ModelViewSet):
  def get_objects():
    '''
    Function to return data from cache if exists
    '''
  serializer_class = DepartmentSerializer
  queryset =  Department.objects.all()


class DepartmentDetailView(APIView):
  """
  Retrieve, update or delete a department instance.
  """
  def get_object(self, id):
    try:
        return Department.objects.get(id=id)
    except Department.DoesNotExist:
        raise Http404

  def get(self, request, id, format=None):
    department = self.get_object(id)
    serializer = DepartmentSerializer(department)
    return Response(serializer.data)

  def put(self, request, id, format=None):
    department = self.get_object(id)
    serializer = DepartmentSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id, format=None):
    department = self.get_object(id)
    department.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_details(request):
  serializer = EmployeeSerializer(request.user)
  return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAdminUser])
def map_employee(request, id):
  ''' Function to employee to a department'''
  employee = User.objects.get(id=id)
  if int(request.data.get('role')) == settings.ROLES.get('MANAGER') and EmployeeRole.objects.filter(department= Department.objects.get(pk=request.data.get('department')), role=settings.ROLES.get('MANAGER')):
      return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('TEAM_ALREADY_HAVE_A_MANAGER')}, status=status.HTTP_412_PRECONDITION_FAILED)

  EmployeeRole.objects.create(employee=employee, department= Department.objects.get(pk=request.data.get('department')), role=request.data.get('role'))

  return Response(status=status.HTTP_201_CREATED)
