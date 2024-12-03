from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll = models.IntegerField()
    std = models.IntegerField()

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    subject = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.subject
    
# class Marks(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
#     marks = models.FloatField()

#     def __str__(self):
#         return self.subject.name