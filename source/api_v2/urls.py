from django.urls import path, include
from rest_framework import routers
from .views import ProfileViewSet, TrackerViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'trackers', TrackerViewSet)
router.register(r'profile', ProfileViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]