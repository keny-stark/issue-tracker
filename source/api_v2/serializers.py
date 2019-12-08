from rest_framework import serializers
from webapp.models import Project, Tracker
from accounts.models import Profile


class TrackerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Tracker
        fields = ('id', 'created_by', 'assigned_to', 'summary', 'description',
                  'status', 'type', 'project_id', 'created_at')


class ProjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    tracker = TrackerSerializer(many=True, read_only=True, source='tracker_project')

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'tracker', 'status', 'created_at', 'updated_at')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'site', 'birth_date', 'text')
