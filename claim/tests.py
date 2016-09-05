
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from serializer import ClaimSerializer
from department.serializers import EmployeeSerializer, DepartmentSerializer



class CreateClaimTest(APITestCase):
    def setUp(self):
        self.client.login(username='vimal', password='aspire@123')
        self.data = {'description': 'claim test deacription', 'date': '2015-06-07', 'department': 'java', }

    def test_can_create_employee(self):
        response = self.client.post(reverse('claims'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_intiate(self):
      response = self.client.post(reverse('claim-intiate'), {'claim_id':2})
      self.assertEqual(response.state, 'INTIATED')

    def test_manager_can_approve(self):
      self.client.login(username='kannan', password='aspire@123')
      response = self.client.post(reverse('claim-intiate'), {'claim_id':2})
      self.assertEqual(response.state, 'APPROVED')

    def test_manager_can_reject(self):
      self.client.login(username='kannan', password='aspire@123')
      response = self.client.post(reverse('claim-intiate'), {'claim_id':2})
      self.assertEqual(response.state, 'REJECTED')

    def test_manager_can_settle(self):
      self.client.login(username='kannan', password='aspire@123')
      response = self.client.post(reverse('claim-intiate'), {'claim_id':2})
      self.assertEqual(response.state, 'SETTLED')



