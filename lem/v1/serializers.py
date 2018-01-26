from django.core.exceptions import ValidationError
from rest_framework import serializers

from utils.serializers import BaseModelSerializer
from v1 import models


class DepartmentSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = models.Department
        fields = (
            'id',
            'name',
        )


class EmployeeSerializer(BaseModelSerializer):
    department = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    department_id = serializers.IntegerField(
        write_only=True,
    )

    class Meta(BaseModelSerializer.Meta):
        model = models.Employee
        fields = (
            'name',
            'email',
            'department',
            'department_id',
        )

    def validate_department_id(self, value):
        try:
            department = models.Department.objects.get(pk=value)
        except models.Department.DoesNotExist:
            raise ValidationError({'error': "Department {pk} does not exist".format(pk=value)})
        return department.pk
