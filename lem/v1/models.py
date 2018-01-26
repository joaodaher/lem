from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel
from v1 import managers


class Department(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _("department")

    def __str__(self):
        return self.name

    def __repr__(self):
        return '[{}] {}'.format(self.pk, self.name)


class Employee(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("email"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )
    department = models.ForeignKey(
        to='v1.Department',
        related_name='employees',
        verbose_name=_("department"),
        on_delete=models.CASCADE,
    )

    objects = models.Manager()
    active = managers.ActiveEmployeeManager()

    class Meta(BaseModel.Meta):
        verbose_name = _("employee")

    def __str__(self):
        return self.email

    def __repr__(self):
        return '[{}] {}'.format(self.pk, self.email)
