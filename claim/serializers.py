from rest_framework import serializers
from .models import Claim
from department.serializers import EmployeeSerializer, DepartmentSerializer
from department.models import Department
from django.contrib.auth.models import User
from claims_manager import settings

class ClaimSerializer(serializers.HyperlinkedModelSerializer):
  owner = EmployeeSerializer()
  processed_by = EmployeeSerializer()
  department = DepartmentSerializer()
  class Meta:
    model = Claim
    fields = ('id', 'image', 'owner', 'date', 'description', 'department', 'state', 'amount_requested', 'amount_approved', 'processed_by')
    extra_kwargs = {'department': {'read_only': True}, 'amount_approved': {'read_only': True}, 'processed_by':{'read_only': True}}
    owner = serializers.Field(source='owner.id')

  def to_representation(self, instance):
      data = super(ClaimSerializer, self).to_representation(instance)
      data['department'] = data['department']['name']
      data['owner'] = data['owner']['username']
      if data['processed_by']:
        data['processed_by'] = data['processed_by']['username']
      data['image'] = '/'.join(data['image'].split('/')[-2:])
      data['state'] = {v: k for k, v in settings.CLAIM_STATE.items()}.get(data['state'])
      return data

  def to_internal_value(self, data):
    data['department'] = Department.objects.get(id=data.get('department', 0))
    return data
