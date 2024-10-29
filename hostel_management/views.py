from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages  # To display messages
from django import forms  # Import forms
from .models import Hostel, Warden , Admin , Room  # Ensure you import the Hostel and Warden models
from django.contrib.auth.hashers import make_password

# Home view
def home(request):
    return render(request, 'home.html')

# Sign-in view for students
def student_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Student').exists():
            login(request, user)
            return redirect('student_dashboard')  # Redirect to student's dashboard
        else:
            messages.error(request, "Invalid credentials or not a student.")
    return render(request, 'auth/student_signin.html')

# Sign-in view for wardens
def warden_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Warden').exists():
            login(request, user)
            return redirect('warden_dashboard')  # Redirect to warden's dashboard
        else:
            messages.error(request, "Invalid credentials or not a warden.")
    return render(request, 'auth/warden_signin.html')

from django.http import HttpResponseRedirect  # Import HttpResponseRedirect

# Sign-in view for admins
def admin_signin(request):
    if request.method == 'POST':
        admin_id = request.POST['admin_id']
        password = request.POST['password']

        try:
            admin = Admin.objects.get(Admin_id=admin_id)

            # Verify the password
            if admin.password == password:  
                request.session['admin_name'] = admin.name
                request.session['admin_id'] = admin.Admin_id
                
                # Redirect to the absolute URL
                return HttpResponseRedirect('http://localhost:8000/admin_dashboard')  
            else:
                messages.error(request, "Invalid credentials.")
        except Admin.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    return render(request, 'auth/admin_signin.html')



# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')  

# Signup view for Admin
def admin_signup(request):
    if request.method == 'POST':
        admin_id = request.POST['admin_id']
        name = request.POST['name']
        mobile_no = request.POST['mobile_no']
        password = request.POST['password'] 

        # Create the admin instance
        Admin.objects.create(Admin_id=admin_id, name=name, mobile_no=mobile_no, password=password)
        
        messages.success(request, "Admin account created successfully.")
        return redirect('admin_signin')  # Redirect to the admin sign-in page

    return render(request, 'auth/admin_signup.html')

def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_signin')  # Redirect to sign in if not logged in

    admin_name = request.session.get('admin_name')
    hostels = Hostel.objects.all()  # Retrieve all hostels

    if request.method == 'POST':
        if 'add_hostel' in request.POST:
            hostel_id = request.POST.get('hostel_id')  # Get hostel_id from form
            hostel_name = request.POST.get('hostel_name')
            total_rooms = int(request.POST.get('total_rooms'))  # Get the total rooms

            # Create the new hostel with the provided hostel_id
            new_hostel = Hostel(hostel_id=hostel_id, name=hostel_name, total_rooms=total_rooms)
            new_hostel.save()

            # Create rooms for the new hostel
            for _ in range(total_rooms):
                Room.objects.create(hostel=new_hostel)

        if 'add_warden' in request.POST:
            warden_name = request.POST.get('warden_name')
            mobile_number = request.POST.get('mobile_number')
            hostel_id = request.POST.get('hostel_id')
            dummy_password = request.POST.get('dummy_password')

            new_warden = Warden(
                name=warden_name,
                mobile_no=mobile_number,
                password=make_password(dummy_password),
                hostel_id=hostel_id
            )
            new_warden.save()

    return render(request, 'admin/admin_dashboard.html', {
        'hostels': hostels,
        'admin_name': admin_name
    })



