from django.contrib import admin

from v1 import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )

    fieldsets = [
        ('Informações', {
            'fields': (
                'id',
                'name',
                'created_at',
                'updated_at',
            )
        }),
    ]


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
    )

    list_filter = (
        'department__name',
    )

    search_fields = (
        'name',
        'email',
    )

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )

    fieldsets = [
        ('Informações', {
            'fields': (
                'id',
                'name',
                'email',
                'department',
                'is_active',
                'created_at',
                'updated_at',
            )
        }),
    ]
