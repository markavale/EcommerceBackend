from .views import TodoViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'todo'

router = DefaultRouter()
router.register('todos', TodoViewSet)

urlpatterns = router.urls
