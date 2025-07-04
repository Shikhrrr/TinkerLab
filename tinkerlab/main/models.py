from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model for students
class StudentUser(AbstractUser):
    roll = models.CharField(max_length=15, unique=True, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')


    def __str__(self):
        return f"{self.username} ({self.roll})"

class Item(models.Model):
    item_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    available = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/')
    location = models.CharField(max_length=100)  # lab name

    def __str__(self):
        return f"{self.title} ({self.item_id})"

class BookingRequest(models.Model):
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purpose = models.TextField()
    duration_days = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")
    request_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    admin_comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.item.title} ({self.status})"
