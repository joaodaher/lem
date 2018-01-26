from django.core.management import call_command
from django.utils.six import StringIO

from v1 import models
from v1.tests.tests_base import BaseApiTest


class MigrationTest(BaseApiTest):
    def test_missing_migration(self):
        out = StringIO()
        message = None
        try:
            call_command(
                'makemigrations',
                'v1',
                '--check',
                '--dry-run',
                interactive=False,
                stdout=out
            )
        except SystemExit:
            message = 'Missing migration. Run python manage.py makemigrations'
        self.assertIn('No changes', out.getvalue(), msg=message)


class DepartmentModelTest(BaseApiTest):
    def test_str_representation(self):
        name = 'Heart of Gold'
        department = models.Department.objects.create(name=name)
        department_str = str(department)
        self.assertEquals(department_str, name)

    def test_debug_representation(self):
        name = 'Heart of Gold'
        pk = 42
        department = models.Department.objects.create(id=pk, name=name)
        department_str = repr(department)
        self.assertEquals(department_str, '[{}] {}'.format(pk, name))


class EmployeeModelTest(BaseApiTest):
    def test_str_representation(self):
        _, department = self.save_department()

        name = 'Marvin'
        email = 'marvin@nope.com'
        employee = models.Employee.objects.create(
            name=name,
            email=email,
            department=department,
        )
        employee_str = str(employee)
        self.assertEquals(employee_str, email)

    def test_debug_representation(self):
        _, department = self.save_department()

        name = 'Marvin'
        email = 'marvin@nope.com'
        pk = 42
        employee = models.Employee.objects.create(
            id=pk,
            name=name,
            email=email,
            department=department,
        )

        employee_str = repr(employee)
        self.assertEquals(employee_str, '[{}] {}'.format(pk, email))
