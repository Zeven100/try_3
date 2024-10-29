# hostel_management/urls.py

from django.urls import path, include
from .views import home , admin_dashboard  # Import the home view or other relevant views

urlpatterns = [
    path('', home, name='home'),                       # Home page
    path('auth/', include('hostel_management.auth_urls')),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),  # Corrected this line

]
