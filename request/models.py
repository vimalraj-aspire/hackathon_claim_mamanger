from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from department.models import Department
from datetime import datetime

# Create your models here.


class ResourceRequest(models.Model):
  owner =  models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, default=None)
  department = models.ForeignKey(Department, blank=False, null=True, on_delete=models.SET_NULL, default=None)
  passport = models.CharField(max_length=50, default=None, null=True)
  visa = models.CharField(max_length=50, default=None, null=True)
  flight_from = models.CharField(max_length=50, default=None, null=True)
  flight_to = models.CharField(max_length=50, default=None, null=True)
  travel_date = models.DateTimeField(default=datetime.now)
  accomodation_at = models.CharField(max_length=50, default=None, null=True)
  insurance_required = models.BooleanField(default=False)
  laptop_config = models.CharField(max_length=100, default=None, null=True)
  laptop_short_term = models.BooleanField(default=False)
  laptop_long_term = models.BooleanField(default=False)
  forex_details = models.CharField(max_length=100, default=None, null=True)
  state = models.IntegerField(default=1)
  processed_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, default=None, related_name='request_processed_by')
  created_at = models.DateTimeField(default=datetime.now)