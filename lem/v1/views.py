from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from v1 import models, serializers


class DepartmentViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class EmployeeViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = models.Employee.active.all()
    serializer_class = serializers.EmployeeSerializer
