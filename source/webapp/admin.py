from django.contrib import admin
from webapp.models import *


class TrackerAdmin(admin.ModelAdmin):
    list_display = ['summary', 'description', 'type', 'status', 'created_at']


admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Project)
admin.site.register(ProjectStatus)
