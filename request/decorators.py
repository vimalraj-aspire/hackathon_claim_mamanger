from models import ResourceRequest
from claims_manager import settings
from department.models import EmployeeRole
from rest_framework.response import Response
from rest_framework import status

def has_manger_permission(func):
  def inner(request, *args, **kwargs):
    import pdb
    pdb.set_trace()
    resource_request = ResourceRequest.objects.get(id=kwargs.get('request_id'))
    if EmployeeRole.objects.filter(department=resource_request.department, role=settings.ROLES.get('MANAGER'), employee=request.user):
      return func(request, *args, **kwargs)
    else:
      return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('MANAGER_PERMISSION_ERROR_ON_REQUEST')}, status=status.HTTP_403_FORBIDDEN)
  return inner

