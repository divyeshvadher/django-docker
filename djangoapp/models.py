from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll = models.IntegerField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)  # Hash the password
        super().save(*args, **kwargs)
           
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    subject = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.subject
    
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    marks = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject} - {self.marks}"