# hostel_management/auth_urls.py

from django.urls import path
from .views import student_signin, warden_signin, admin_signin, logout_view, admin_signup

urlpatterns = [
    path('student/signin/', student_signin, name='student_signin'),
    path('warden/signin/', warden_signin, name='warden_signin'),
    path('admin/signin/', admin_signin, name='admin_signin'),
    path('admin/signup/', admin_signup, name='admin_signup'),  # Add this line
    path('logout/', logout_view, name='logout'),
]
