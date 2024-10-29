# hostel_management/urls.py

from django.urls import path, include
from .views import home , admin_dashboard , warden_dashboard , add_student , view_student_info # Import the home view or other relevant views

urlpatterns = [
    path('', home, name='home'),                       # Home page
    path('auth/', include('hostel_management.auth_urls')),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),  # Corrected this line
    path('warden_dashboard/', warden_dashboard, name='warden_dashboard'), 
    path('add_student/', add_student, name='add_student'),
    path('view_student_info/', view_student_info, name='view_student_info'),
]
