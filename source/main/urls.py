"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
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
]
