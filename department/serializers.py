from rest_framework import serializers
from .models import Department, EmployeeRole
from django.contrib.auth.models import User



class DepartmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Department


class EmployeeRoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = EmployeeRole
    fields = ('department', 'role')


class EmployeeSerializer(serializers.ModelSerializer):
  department = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ('id', 'password', 'first_name', 'last_name', 'email', 'username', 'department')
    extra_kwargs = {'password': {'write_only': True}}
    readonly_fields = ('is_active', 'date_joined')

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User.objects.create(**validated_data)
    user.set_password(password)
    user.save()
    return user

  def get_department(self, user):
    return EmployeeRole.objects.filter(employee=user).values()