from rest_framework.routers import DefaultRouter

from v1 import views

router = DefaultRouter()

router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = router.urls
