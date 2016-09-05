from rest_framework import serializers
from .models import ResourceRequest
from department.serializers import EmployeeSerializer, DepartmentSerializer
from department.models import Department
from claims_manager import settings


class ResourceRequestSerializer(serializers.ModelSerializer):
  owner = EmployeeSerializer()
  department = DepartmentSerializer()
  processed_by = EmployeeSerializer()
  class Meta:
    model = ResourceRequest
    fields = ('id', 'owner', 'department', 'passport', 'visa', 'flight_from', 'flight_to', 'travel_date', 'accomodation_at', 'insurance_required', 'laptop_short_term', 'laptop_config', 'laptop_long_term', 'forex_details', 'processed_by', 'state')
    extra_kwargs = {'department': {'read_only': True}, 'owner': {'read_only': True}, 'processed_by':{'read_only': True}}
    
  def to_representation(self, instance):
    data = super(ResourceRequestSerializer, self).to_representation(instance)
    data['department'] = data['department']['name']
    data['owner'] = data['owner']['username']
    if data['processed_by']:
      data['processed_by'] = data['processed_by']['username']
    data['state'] = {v: k for k, v in settings.REQUEST_STATE.items()}.get(data['state'])
    return data

  def to_internal_value(self, data):
    import pdb
    pdb.set_trace()
    data['department'] = Department.objects.get(id=data.get('department', 0))
    return data