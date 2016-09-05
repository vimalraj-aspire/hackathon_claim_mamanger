from .models import Claim
from claims_manager import settings
from department.models import EmployeeRole
from rest_framework.response import Response
from rest_framework import status

def has_manger_permission(func):
  def inner(request, *args, **kwargs):    
    claim = Claim.objects.get(id=kwargs.get('claim_id'))
    if EmployeeRole.objects.filter(department=claim.department, role=settings.ROLES.get('MANAGER'), employee=request.user):
      return func(request, *args, **kwargs)
    else:
      return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('MANAGER_PERMISSION_ERROR')}, status=status.HTTP_403_FORBIDDEN)
  return inner

