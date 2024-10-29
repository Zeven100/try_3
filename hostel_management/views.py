from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages  # To display messages
from django import forms  # Import forms
from .models import Hostel, Warden , Admin , Room , Student # Ensure you import the Hostel and Warden models
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

        # Updated part of the admin_dashboard view
        if 'add_warden' in request.POST:
            warden_id = request.POST.get('warden_id')  # Get warden_id from form
            warden_name = request.POST.get('warden_name')
            mobile_number = request.POST.get('mobile_number')
            hostel_id = request.POST.get('hostel_id')
            dummy_password = request.POST.get('dummy_password')

            new_warden = Warden(
                warden_id=warden_id,  # Set the warden_id here
                name=warden_name,
                mobile_no=mobile_number,
                password=dummy_password,  # Save the password directly without hashing
                hostel_id=hostel_id
            )
            new_warden.save()

    return render(request, 'admin/admin_dashboard.html', {
        'hostels': hostels,
        'admin_name': admin_name
    })



def warden_signin(request):
    if request.method == 'POST':
        warden_id = request.POST['warden_id']
        password = request.POST['password']

        try:
            warden = Warden.objects.get(warden_id=warden_id)

            # Verify the password
            if warden.password == password:  # You may want to hash and verify instead
                request.session['warden_name'] = warden.name
                request.session['warden_id'] = warden.warden_id
                
                # Redirect to the warden dashboard
                return HttpResponseRedirect('http://localhost:8000/warden_dashboard')  
            else:
                messages.error(request, "Invalid credentials.")
        except Warden.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    return render(request, 'auth/warden_signin.html')

from django.shortcuts import get_object_or_404, redirect, render
from .models import Room, Student, Warden, Hostel

from django.shortcuts import get_object_or_404, redirect, render
from .models import Room, Student, Warden, Hostel

# .....
def warden_dashboard(request):
    if not request.session.get('warden_id'):
        return redirect('warden_signin')  # Redirect to sign in if not logged in

    warden = Warden.objects.get(warden_id=request.session['warden_id'])
    available_rooms = Room.objects.filter(hostel=warden.hostel, occupancy_status=False)
    
    return render(request, 'warden/warden_dashboard.html', {
        'warden_name': warden.name,
        'available_rooms': available_rooms,
    })

def add_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        mobile_number = request.POST.get('mobile_number')
        room_id = request.POST.get('room_id')
        dummy_password = request.POST.get('dummy_password')  # Get the dummy password
        hostel_id = request.POST.get('hostel_id')

        # Create new student
        hostel = Hostel.objects.get(hostel_id=hostel_id)
        new_student = Student(student_id=student_id, name=student_name, mobile_number=mobile_number, hostel=hostel)
        new_student.save()

        # Update room occupancy status
        room = Room.objects.get(room_id=room_id)
        room.student = new_student
        room.occupancy_status = True
        room.save()

        # You can store the dummy password in a way that suits your needs, for example in a related model or handle it separately.

        return redirect('warden_dashboard')

    # For GET request, populate available rooms
    warden = Warden.objects.get(warden_id=request.session['warden_id'])
    available_rooms = Room.objects.filter(hostel=warden.hostel, occupancy_status=False)

    return render(request, 'warden/add_student.html', {
        'available_rooms': available_rooms,
        'warden': warden,
    })


from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import Student, Transaction

def view_student_info(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, student_id=student_id)

        # Fetch the transactions for the student
        transactions = Transaction.objects.filter(student=student)

        if 'change_room' in request.POST:
            new_room_id = request.POST.get('new_room_id')
            try:
                new_room = Room.objects.get(room_id=new_room_id, occupancy_status=False)
                # Update the student's room
                if student.room:
                    # Free the current room if occupied
                    student.room.occupancy_status = False
                    student.room.save()
                student.room = new_room
                student.room.occupancy_status = True  # Mark new room as occupied
                student.save()
                new_room.save()  # Save the new room
                messages.success(request, f"Room changed to {new_room.room_id} successfully.")
            except Room.DoesNotExist:
                messages.error(request, "Room does not exist or is already occupied.")
        
        return render(request, 'warden/view_student_info.html', {
            'student': student,
            'transactions': transactions,
            'rooms': Room.objects.filter(hostel=student.hostel, occupancy_status=False)  # Fetch available rooms
        })

    return render(request, 'warden/view_student.html')
