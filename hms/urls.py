# hms/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                   # Admin page
    path('', include('hostel_management.urls')),      # Include URLs from hostel_management app
]
