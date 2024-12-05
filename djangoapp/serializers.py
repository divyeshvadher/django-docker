from rest_framework import serializers
from .models import *
        
class SubjectSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'subject', 'student_name']

    def get_student_name(self, obj):
        # Return the student's name (assuming the student relationship is defined)
        return obj.student.name
        
class MarksSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    subject_name = serializers.CharField(source='subject.subject', read_only=True)

    class Meta:
        model = Marks
        fields = ['id', 'student_name', 'subject_name', 'marks']
        
class StudentSerializer(serializers.ModelSerializer):
    flat_subjects = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['name', 'age', 'roll', 'flat_subjects']

    def get_flat_subjects(self, obj):
        marks = Marks.objects.filter(student=obj)
        flat_data = {}
        for mark in marks:
            flat_data[mark.subject.subject] = mark.marks
        return flat_data