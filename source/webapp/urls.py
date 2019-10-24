from django.urls import path
from webapp.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tracker/<int:pk>/', TrackerView.as_view(), name='tracker'),
    path('tracker/add/', TrackerCreateView.as_view(), name='tracker_add'),
    path('tracker/<int:pk>/edit/', TrackerUpdate.as_view(), name='update_tracker'),
    path('tracker/<int:pk>/delete/', DeleteTracker.as_view(), name='delete_tracker'),
    path('tracker/type/', TypeView.as_view(), name='type_views'),
    path('tracker/type/add/', TypeAddView.as_view(), name='add_type'),
    path('tracker/type/delete/<int:pk>/', DeleteType.as_view(), name='delete_type'),
    path('tracker/type/update/<int:pk>/', UpdateTypeView.as_view(), name='update_type'),
    path('tracker/status/', StatusView.as_view(), name='status_views'),
    path('tracker/status/add/', StatusAddView.as_view(), name='add_status'),
    path('tracker/status/update/<int:pk>/', UpdateStatusView.as_view(), name='update_status'),
    path('tracker/status/delete/<int:pk>/', DeleteStatus.as_view(), name='delete_status'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdate.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='delete_project'),
    path('article/<int:pk>/add-comment/', TrackerForProjectCreateView.as_view(), name='create_new_tracker')
]
