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
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        try:
            # Check if a student with the provided ID exists
            student = Student.objects.get(student_id=student_id)

            # Verify password
            if student.password == password:
                # Store student data in the session
                request.session['student_name'] = student.name
                request.session['student_id'] = student.student_id
                
                # Redirect to the student dashboard
                return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid credentials.")
        except Student.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    
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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Admin

def admin_signin(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(Admin_id=admin_id)
            if admin.password == password:
                request.session['admin_name'] = admin.name
                request.session['admin_id'] = admin.Admin_id

                # Debug message to check session data
                print("Admin signed in:", request.session['admin_name'], request.session['admin_id'])

                # Redirect using reverse to ensure proper URL resolution
                return redirect(reverse('admin_dashboard'))
            else:
                messages.error(request, "Invalid credentials.")
        except Admin.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    # Debug message to check redirection cause
    print("Redirecting back to sign-in due to invalid credentials or session")

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
    # Check if the admin is logged in by verifying the session
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        # Log the reason for redirection
        print("Admin ID not found in session. Redirecting to admin_signin.")
        messages.error(request, "You need to sign in to access the admin dashboard.")
        return redirect('admin_signin')  # Redirect to sign in if not logged in

    # Admin is logged in, proceed to retrieve admin details
    print(f"Admin {admin_name} (ID: {admin_id}) accessed the dashboard.")
    hostels = Hostel.objects.all()  # Retrieve all hostels

    if request.method == 'POST':
        # Handling the addition of a new hostel
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

        # Handling the addition of a new warden
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
from .models import Room, Student, Warden, Hostel , Wallet

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
        new_student = Student(student_id=student_id, name=student_name, mobile_number=mobile_number, hostel=hostel, password=dummy_password)
        new_student.save()

        # Update room occupancy status
        room = Room.objects.get(room_id=room_id)
        room.student = new_student
        room.occupancy_status = True
        room.save()

        # Create a wallet for the new student with a balance of 0.00
        Wallet.objects.create(student=new_student, balance=0.00)

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

def change_password(request):
    if not request.session.get('warden_id'):
        return redirect('warden_signin')  # Redirect to sign in if not logged in

    warden = Warden.objects.get(warden_id=request.session['warden_id'])

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        # Here, you would typically verify the current password
        if current_password == warden.password:  # Adjust this to use hashed passwords if applicable
            warden.password = new_password  # Update the password
            warden.save()
            messages.success(request, "Your password has been changed successfully.")
            return redirect('warden_dashboard')
        else:
            messages.error(request, "Current password is incorrect.")

    return render(request, 'warden/change_password.html', {'warden': warden})
from decimal import Decimal , InvalidOperation  
def student_dashboard(request):
    student_id = request.session.get('student_id')
    wallet_info = None

    if student_id:
        # Fetch wallet information for the student
        wallet_info = Wallet.objects.filter(student_id=student_id).first()  # Get wallet for the current student

    return render(request, 'student/student_dashboard.html', {
        'wallet_info': wallet_info,  # Pass wallet info to the template
    })

def view_transactions(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_signin')  # Redirect if not logged in

    # Get the student's transactions
    transactions = Transaction.objects.filter(student_id=student_id)

    return render(request, 'student/view_transactions.html', {'transactions': transactions})

def make_payment(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        student_id = request.session.get('student_id')

        if student_id:
            # Fetch the student's wallet balance
            try:
                wallet = Wallet.objects.get(student_id=student_id)
                current_balance = wallet.balance
                amount = Decimal(amount)  # Convert to Decimal for comparison

                # Check if the student has enough balance
                if amount <= current_balance:
                    # Process the payment
                    transaction = Transaction(student_id=student_id, amount=amount, status='Completed')
                    transaction.save()

                    # Deduct the amount from the wallet balance
                    wallet.balance -= amount
                    wallet.save()

                    messages.success(request, "Payment made successfully!")
                    return redirect('student_dashboard')  # Redirect after successful payment
                else:
                    messages.error(request, "Insufficient balance for this transaction.")
            except Wallet.DoesNotExist:
                messages.error(request, "Wallet not found. Please contact support.")
        else:
            return redirect('student_signin')  # Redirect if not logged in

    return render(request, 'student/make_payment.html')

# views.py

def add_dummy_money(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', 0)
        student_id = request.session.get('student_id')

        if student_id:
            # Ensure the amount is a valid decimal number
            try:
                amount = Decimal(amount)  # Convert to Decimal
                if amount > 0:  # Validate that the amount is positive
                    wallet, created = Wallet.objects.get_or_create(student_id=student_id)
                    wallet.balance += amount  # Add the amount to the wallet balance
                    wallet.save()

                    messages.success(request, "Dummy money added successfully!")
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "Please enter a positive amount.")
            except (ValueError, InvalidOperation):
                messages.error(request, "Invalid amount entered.")
        else:
            return redirect('student_signin')  # Redirect if not logged in

    return render(request, 'student/add_dummy_money.html')
