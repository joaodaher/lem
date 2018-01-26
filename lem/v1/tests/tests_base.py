from rest_framework.test import APITransactionTestCase

from v1 import models


class FieldFactoryMixin:
    def make_department(self, **kwargs):
        fields = {
            'name': 'Heart of Gold',
        }
        fields.update(**kwargs)
        return fields

    def make_employee(self, department, **kwargs):
        fields = {
            'name': 'Marvin',
            'email': 'marvin@galaxy.com',
            'department_id': department.pk,
        }
        fields.update(**kwargs)
        return fields


class ModelFactoryMixin(FieldFactoryMixin):
    def save_department(self, **kwargs):
        fields = super().make_department(**kwargs)
        model = models.Department.objects.create(**fields)
        return fields, model

    def save_employee(self, department=None, **kwargs):
        if not department:
            department, _ = self.save_department()
        fields = super().make_employee(department=department, **kwargs)
        model = models.Employee.objects.create(**fields)
        return fields, model


class BaseApiTest(ModelFactoryMixin, APITransactionTestCase):
    def assertFieldInResponse(self, members, response, fields=None):
        def _create_key(item):
            return '#'.join([str(item.get(field)) for field in fields])

        if not fields:
            fields = ['id']

        data = response.data
        try:
            results = data['results']
        except KeyError:
            results = [data]

        pks = [_create_key(item=r) for r in results]

        if not isinstance(members, list):
            members = [members]
        for member in members:
            pk = _create_key(item=member)
            self.assertIn(pk, pks)
            pks.remove(pk)
        self.assertEqual(any(pks), False)
