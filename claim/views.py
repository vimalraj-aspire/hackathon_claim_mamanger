from .models import Claim
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .serializers import ClaimSerializer
from django.http import Http404
from department.models import EmployeeRole
from rest_framework.decorators import api_view
from claims_manager import settings
import json
from decorators import has_manger_permission
from department.models import Department
from notification.models import Notification
from django.contrib.auth.models import User

def get_claims(user):
  '''
  Function to return the available claims of user, If requester is a manager 
  it will return all the claims on the departments of the manager
  '''
  user_departments = EmployeeRole.objects.filter(employee=user, role=settings.ROLES.get('MANAGER')).values_list('department')
  if not user_departments:
    claims = Claim.objects.filter(owner=user)
  else:          
    claims = Claim.objects.filter(department=user_departments).exclude(state=settings.CLAIM_STATE.get('DRAFT'))
  return claims

def get_user_department(user):
  '''
    Returns department id of user
  '''
  return EmployeeRole.objects.filter(employee=user).values('department')[0].get('department')

def get_department_manager(department):
  return User.objects.get(id=EmployeeRole.objects.filter(department=department, role=settings.ROLES.get('MANAGER')).values('employee')[0].get('employee'))

class ClaimList(APIView):
    ''' Returns list of claims and create a claim instance'''
    def get(self, request, format=None):
        serializer_context = {
          'request': Request(request),
        }
        claims = get_claims(self.request.user)
        serializer = ClaimSerializer(claims, many=True, context=serializer_context)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
      serializer_context = {
        'request': Request(request),
      }
      serializer_data = request.data
      serializer_data['owner'] = self.request.user
      serializer_data['department'] = get_user_department(self.request.user)
      serializer = ClaimSerializer(data=serializer_data, context=serializer_context)
      if serializer.is_valid():
        claim = serializer.save(owner=self.request.user)           
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClaimDetail(APIView):
    ''' Class based view to perform retreive, udate and delete a claim'''
    def get_object(self, claim_id):
        try:
            return Claim.objects.get(id=claim_id)
        except Claim.DoesNotExist:
            raise Http404

    def get(self, request, claim_id, format=None):
        claim = self.get_object(claim_id)
        serializer_context = {
        'request': Request(request),
        }        
        serializer = ClaimSerializer(claim, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, claim_id, format=None):
        claim = self.get_object(claim_id)
        if claim.state == settings.CLAIM_STATE.get('DRAFT'):
          serializer_context = {
            'request': Request(request),
          }
          serializer = ClaimSerializer(claim, data=request.data,  context=serializer_context)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('CLAIM_NOT_AVAILABLE')}, status=status.HTTP_412_PRECONDITION_FAILED)


    def delete(self, request, claim_id, format=None):
        claim = self.get_object(claim_id)
        claim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def submit_claim(request, claim_id):
  ''' Function to submit the claim for approval '''
  try:
    claim = Claim.objects.get(id=claim_id, owner=request.user, state=settings.CLAIM_STATE.get('DRAFT'))
    claim.state = settings.CLAIM_STATE.get('INTIATED')
    Notification.objects.create(owner=get_department_manager(get_user_department(self.request.user)), claim=claim)
    claim.save()
    return Response({'status': 'success', 'msg': settings.API_ERRORS.get('CLAIM_INTIATED')})
  except Claim.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('CLAIM_IN_PROCESS_ERROR')}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
@has_manger_permission
def approve_claim(request, claim_id):
  ''' Approves claim, needs manager permission'''
  try:
    claim = Claim.objects.get(id=claim_id)
    if settings.DEPARTMENT.get('FINANCE') == claim.department.id:
      if int(request.POST.get('amount_approved',0)): 
        claim.state = settings.CLAIM_STATE.get('SETTLED')
        claim.processed_by = request.user
        claim.amount_approved = request.POST.get('amount_approved')
        claim.save()
        Notification.objects.create(owner=claim.owner, claim=claim)

        return Response({'status': 'success', 'msg': settings.API_ERRORS.get('CLAIM_APPROVED_BY_FINANCE')})
      else:
        return Response({'status': 'success', 'msg': settings.API_ERRORS.get('AMOUNT_APPROVED_NOT_AVAILABLE')})
    else:
      claim.state = settings.CLAIM_STATE.get('MOVED_TO_FINANCE')
      claim.department = Department.objects.get(id=settings.DEPARTMENT.get('FINANCE'))
      claim.processed_by = request.user
      claim.save()
      Notification.objects.create(owner=claim.owner, claim=claim)
      return Response({'status': 'success', 'msg': settings.API_ERRORS.get('CLAIM_APPROVED')})
  except Claim.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('CLAIM_NOT_AVAILABLE')}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@has_manger_permission
def reject_claim(request, claim_id):
  ''' Rejects claim, needs manager permission'''
  try:
    claim = Claim.objects.get(id=claim_id)
    if settings.DEPARTMENT.get('FINANCE') == claim.department.id:
      claim.state = settings.CLAIM_STATE.get('REJECTED_BY_FINANCE')
      claim.processed_by = request.user
      claim.save()
      Notification.objects.create(owner=claim.owner, claim=claim)
      return Response({'status': 'success', 'msg': settings.API_ERRORS.get('CLAIM_REJECTED_BY_FINANCE')})
    else:
      claim.state = settings.CLAIM_STATE.get('REJECTED')
      claim.processed_by = request.user
      claim.save()
      Notification.objects.create(owner=claim.owner, claim=claim)
      return Response({'status': 'success', 'msg': settings.API_ERRORS.get('CLAIM_REJECTED')})
  except Claim.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('CLAIM_NOT_AVAILABLE')}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@has_manger_permission
def settle_claim(request, claim_id):
  ''' Settle claim, needs manager permission'''
  try:
    claim = Claim.objects.get(id=claim_id)
    claim.state = settings.CLAIM_STATE.get('SETTLED')
    claim.processed_by = request.user
    claim.save()
    Notification.objects.create(owner=claim.owner, claim=claim)
    return Response({'status': 'success', 'msg': settings.API_ERRORS.get('CLAIM_SETTLED')})
  except Claim.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('CLAIM_NOT_AVAILABLE')}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def approved_claims(request):
  ''' Function to return list of approved claims'''
  claims =  get_claims(request.user).filter(state=settings.CLAIM_STATE.get('APPROVED'))  
  serializer = ClaimSerializer(claims, many=True)
  return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def rejected_claims(request):
  ''' Function to return list of rejected claims '''
  claims =  get_claims(request.user).filter(state=settings.CLAIM_STATE.get('REJECTED'))  
  serializer = ClaimSerializer(claims, many=True, context=serializer_context)
  return Response(data=serializer.data, status=status.HTTP_200_OK)
  