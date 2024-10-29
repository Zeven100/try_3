from django.db import models

class Admin(models.Model):
    Admin_id = models.CharField(max_length=50, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    password = models.CharField(max_length=100)  # Use hashing for security

    def __str__(self):
        return self.name

class Warden(models.Model):
    warden_id = models.CharField(max_length=50, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    password = models.CharField(max_length=100)  # Use hashing for security
    # This field defines the one-to-one relationship with Hostel
    hostel = models.OneToOneField(
        'Hostel',  # Use string reference to avoid NameError
        on_delete=models.CASCADE,
        related_name='warden'  # This allows reverse access from Hostel to Warden
    )

    def __str__(self):
        return self.name

class Hostel(models.Model):
    hostel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    total_rooms = models.PositiveIntegerField()
    # The warden field is defined here, but it's not necessary since it's already in Warden
    # Uncomment the below line if you want to explicitly define it here as well
    # warden = models.OneToOneField(Warden, on_delete=models.CASCADE, related_name='managed_hostel')

    def __str__(self):
        return self.name

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    occupancy_status = models.BooleanField(default=False)
    student = models.OneToOneField(
        'Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='room'  # This allows `student.room` to access the Room instance
    )

    def __str__(self):
        return f"Room {self.room_id} in {self.hostel.name}"

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"Student {self.name} ({self.student_id})"

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.student.name}"

class Wallet(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet for {self.student.name} with balance {self.balance}"
