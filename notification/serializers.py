from rest_framework import serializers
from request.serializers import ResourceRequestSerializer
from claim.serializers import ClaimSerializer
from department.serializers import EmployeeSerializer, DepartmentSerializer
from models import Notification

class NotificationSerializer(serializers.ModelSerializer):
  # owner = EmployeeSerializer()
  request = ResourceRequestSerializer()
  claim = ClaimSerializer()
  class Meta:
    model = Notification
    fields = ('id', 'claim', 'request', 'created_at')
    