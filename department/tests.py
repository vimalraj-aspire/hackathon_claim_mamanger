
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import DepartmentSerializer, EmployeeRoleSerializer, EmployeeSerializer



class CreateEmployeeTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@gmail.com', 'aspire@123')
        self.client.login(username='admin', password='aspire@123')
        self.data = {'username': 'vimal', 'first_name': 'Vimal', 'last_name': 'sankar'}

    def test_can_create_employee(self):
        response = self.client.post(reverse('employee-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


