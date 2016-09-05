from __future__ import unicode_literals
from request.models import ResourceRequest
from claim.models import Claim
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Notification(models.Model):
  owner =  models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, default=None)
  request =  models.ForeignKey(ResourceRequest, blank=True, null=True, on_delete=models.SET_NULL, default=None)
  claim =  models.ForeignKey(Claim, blank=True, null=True, on_delete=models.SET_NULL, default=None)
  is_notified = models.BooleanField(default=False)
  created_at = models.DateTimeField(default=datetime.now)