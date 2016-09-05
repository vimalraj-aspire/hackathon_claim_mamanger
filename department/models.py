from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
 name = models.CharField(max_length=30)

class EmployeeRole(models.Model):
  '''
    Employee role model, an employee can be a partr of multiple teams 
  '''
  employee = models.ForeignKey(User, on_delete=models.CASCADE)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)
  role = models.IntegerField(default=2)