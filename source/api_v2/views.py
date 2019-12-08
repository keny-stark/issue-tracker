from rest_framework import viewsets
from .serializers import ProjectSerializer, ProfileSerializer, TrackerSerializer
from webapp.models import Project, Tracker
from accounts.models import Profile


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class TrackerViewSet(viewsets.ModelViewSet):
    serializer_class = TrackerSerializer
    queryset = Tracker.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
