from django.db import OperationalError, connections
from mock import patch
from rest_framework import status

from v1 import models
from v1.tests.tests_base import BaseApiTest


class HealthCheckTests(BaseApiTest):
    url = '/healthcheck/'

    def test_healthcheck_returns_200(self):
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        self.assertIn('OK', result.json().get('database'))

    def test_healthcheck_db_fail(self):
        conn = connections['default']
        with patch.object(conn.__class__, 'cursor') as mock_method:
            mock_method.side_effect = OperationalError('Mocked database error')

            result = self.client.get(self.url)
            self.assertEqual(result.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
            self.assertIn('ERROR', result.json().get('database'))


class AdminTests(BaseApiTest):
    def test_locale_middleware(self):
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, status.HTTP_302_FOUND)


class DepartmentViewTests(BaseApiTest):
    url = '/v1/departments/'

    def test_list_department(self):
        department_42, _ = self.save_department(id=42)
        department_314, _ = self.save_department(id=314)

        url = self.url
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([department_42, department_314], response)

    def test_list_department_invalid_page(self):
        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=-1,
            page_size=1,
        )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_department_last_page(self):
        self.save_department(id=1)
        department_2, _ = self.save_department(id=2)

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page='last',
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([department_2], response)

    def test_list_department_paginated(self):
        department_1, _ = self.save_department(id=1)
        department_2, _ = self.save_department(id=2)
        department_3, _ = self.save_department(id=3)

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=1,
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([department_1], response)

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=2,
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([department_2], response)

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=3,
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([department_3], response)

    def test_detail_department(self):
        department_1, _ = self.save_department(id=1)

        url = '{}{}/'.format(self.url, 1)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse(department_1, response)

    def test_post_department(self):
        data = self.make_department(id=1)
        url = self.url
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Department.objects.count(), 1)


class EmployeeViewTests(BaseApiTest):
    url = '/v1/employees/'

    def test_list_employees(self):
        _, department = self.save_department()

        employee_42, _ = self.save_employee(id=42, email='42@lem.com', department=department)
        employee_314, _ = self.save_employee(id=314, email='314@lem.com', department=department)

        url = self.url
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([employee_42, employee_314], response, fields=['email'])

    def test_list_employee_invalid_page(self):
        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=-1,
            page_size=1,
        )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_employee_last_page(self):
        _, department = self.save_department()

        self.save_employee(id=1, email='1@lem.com', department=department)
        department_2, _ = self.save_employee(id=2, email='2@lem.com', department=department)

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page='last',
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([department_2], response, fields=['email'])

    def test_list_employee_paginated(self):
        _, department = self.save_department()

        employee_1, _ = self.save_employee(id=1, email='1@lem.com', department=department)
        employee_2, _ = self.save_employee(id=2, email='2@lem.com', department=department)
        employee_3, _ = self.save_employee(id=3, email='3@lem.com', department=department)

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=1,
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([employee_1], response, fields=['email'])

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=2,
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([employee_2], response, fields=['email'])

        url = '{url}?page={page}&page_size={page_size}'.format(
            url=self.url,
            page=3,
            page_size=1,
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse([employee_3], response, fields=['email'])

    def test_detail_employee(self):
        _, department = self.save_department()

        employee_id = 42
        employee, _ = self.save_employee(id=employee_id, email='42@lem.com', department=department)

        url = '{}{}/'.format(self.url, employee_id)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFieldInResponse(employee, response, fields=['email'])

    def test_post_employee(self):
        _, department = self.save_department()

        data = self.make_employee(id=1, department=department)
        url = self.url
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Employee.objects.count(), 1)

    def test_post_employee_without_department(self):
        _, department = self.save_department()

        employee = self.make_employee(id=42, department=department)

        data = employee
        data.pop('department_id')

        url = self.url
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(models.Employee.objects.exists())
