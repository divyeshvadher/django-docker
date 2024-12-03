from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'subject', 'student_name']

    def get_student_name(self, obj):
        # Return the student's name (assuming the student relationship is defined)
        return obj.student.name
        
# class MarksSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = '__all__'