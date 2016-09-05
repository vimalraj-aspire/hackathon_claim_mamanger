from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from department.models import Department
from validators import validate_file_extension


# Create your models here.
class Claim(models.Model):
  owner =  models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, default=None)
  department = models.ForeignKey(Department, blank=False, null=True, on_delete=models.SET_NULL, default=None)
  image = models.FileField(upload_to='claim_documents', validators=[validate_file_extension])
  date = models.DateTimeField(default=datetime.now)
  description = models.CharField(max_length=500, default=None)
  state = models.IntegerField(default=0)
  amount_requested = models.IntegerField(default=0)
  amount_approved = models.IntegerField(default=0)
  processed_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, default=None, related_name='processed_by')
  created_at = models.DateTimeField(default=datetime.now)
  processed_at = models.DateTimeField(default=datetime.now)