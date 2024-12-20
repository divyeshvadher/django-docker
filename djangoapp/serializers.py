from rest_framework import serializers
from .models import *
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed        
    
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
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'roll', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_flat_subjects(self, obj):
        marks = Marks.objects.filter(student=obj)
        flat_data = {}
        for mark in marks:
            flat_data[mark.subject.subject] = mark.marks
        return flat_data
    
class StudentLoginSerializer(serializers.Serializer):
    roll = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        roll = attrs.get('roll')
        password = attrs.get('password')

        if not roll or not password:
            raise AuthenticationFailed('Roll number and password are required.')

        # Check if the student exists
        try:
            student = Student.objects.get(roll=roll)  # Make sure you're querying the Student model, not User
        except Student.DoesNotExist:
            raise AuthenticationFailed('Student not found.')

        # Check password
        if not student.check_password(password):  # Make sure you're using the check_password method from the Student model
            raise AuthenticationFailed('Invalid credentials.')

        attrs['student'] = student
        return attrs