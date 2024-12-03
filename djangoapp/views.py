from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *


# Create your views here.

# get all students
@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

# get single student
@api_view(['GET'])
def get_student(request, pk):
    student = Student.objects.get(id=pk)
    serializer = StudentSerializer(student, many=False)
    return Response(serializer.data)

# add student
@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

# update student
@api_view(['PUT'])
def update_student(request, pk):
    student = Student.objects.get(id=pk)
    serializer = StudentSerializer(instance=student, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

# delete student
@api_view(['DELETE'])
def delete_student(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    
    return Response('Student deleted successfully')

# Subject Views
@api_view(['GET'])
def get_subjects(request):
    try:
        # Get optional student_id from query parameters
        student_id = request.query_params.get('student_id')
        
        if student_id:
            # Retrieve subjects for the specific student
            subjects = Subject.objects.filter(student_id=student_id)
            if not subjects.exists():
                return Response({'error': 'No subjects found for the given student.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all subjects if no student_id is provided
            subjects = Subject.objects.all()
        
        # Serialize the subjects
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_subject(request, pk):
#     subject = Subject.objects.get(id=pk)
#     serializer = SubjectSerializer(subject, many=False)
#     return Response(serializer.data)

@api_view(['POST'])
def add_subject(request):
    try:
        print("Request data:", request.data)  # Debugging
        student_id = request.data.get('student_id')
        subject_name = request.data.get('subject')
        if not student_id or not subject_name:
            return Response({'error': 'Both student_id and subject are required.'}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.get(id=student_id)
        print("Student found:", student)  # Debugging
        subject = Subject.objects.create(student=student, subject=subject_name)
        subject.save()

        print("Subject created:", subject)  # Debugging
        return Response({'message': 'Subject added successfully!'}, status=status.HTTP_201_CREATED)
    except Student.DoesNotExist:
        print("Student not found")  # Debugging
        return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Error:", str(e))  # Debugging
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def update_subject(request, pk):
#     subject = Subject.objects.get(id=pk)
#     serializer = SubjectSerializer(instance=subject, data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()
    
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def delete_subject(request, pk):
#     subject = Subject.objects.get(id=pk)
#     subject.delete()
    
#     return Response('Subject deleted successfully')

# # Marks Views
# @api_view(['GET'])
# def get_marks(request):
#     marks = Marks.objects.all()
#     serializer = MarksSerializer(marks, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_mark(request, pk):
#     mark = Marks.objects.get(id=pk)
#     serializer = MarksSerializer(mark, many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def add_mark(request):
#     serializer = MarksSerializer(data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()
    
#     return Response(serializer.data)

# @api_view(['PUT'])  
# def update_mark(request, pk):
#     mark = Marks.objects.get(id=pk)
#     serializer = MarksSerializer(instance=mark, data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()
    
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def delete_mark(request, pk):
#     mark = Marks.objects.get(id=pk)
#     mark.delete()
    
#     return Response('Mark deleted successfully')