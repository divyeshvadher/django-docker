from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenRefreshView

# Create your views here.

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Log or handle the refresh token usage
        print(f"Token refreshed for user: {request.user}")
        return response

def get_tokens_for_user(student):
    refresh = RefreshToken.for_user(student)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login(request):
    roll = request.data.get('roll')
    password = request.data.get('password')

    if not roll or not password:
        return Response({'error': 'Roll number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(roll=roll)

        if check_password(password, student.password):
            tokens = get_tokens_for_user(student)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()

    # Build a response including subjects and marks for each student
    data = []
    for student in students:
        # Fetch all subjects and their associated marks for the student
        subjects_data = []
        for subject in student.subjects.all():
            # Fetch marks using the relationship
            marks_obj = subject.marks.filter(student=student).first()
            marks = marks_obj.marks if marks_obj else 0  # Default to 0 if no marks found

            # Append subject and marks
            subjects_data.append({subject.subject: marks})

        # Combine student and subject information
        student_data = {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "roll": student.roll,
            "subjects": subjects_data,  # Include subjects and marks here
        }
        data.append(student_data)

    return Response(data, status=200)



# get single student
@api_view(['GET'])
def get_student(request, pk):
    try:
        # Fetch the student by primary key
        student = Student.objects.get(id=pk)

        # Initialize student data
        data = {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "roll": student.roll,
            "subjects": []  # List to store subject and marks
        }

        # Fetch all subjects and their associated marks for the student
        for subject in student.subjects.all():
            # Fetch marks using the reverse relationship
            marks_obj = subject.marks.filter(student=student).first()
            marks = marks_obj.marks if marks_obj else 0  # Default to 0 if no marks found

            # Append subject and marks to the subjects list
            data["subjects"].append({subject.subject: marks})

        return Response(data, status=200)

    except Student.DoesNotExist:
        return Response({'error': 'Student not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


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

@api_view(['GET'])
def get_subject(request, pk):
    try:
        # Retrieve the specific subject by its ID (primary key)
        subject = Subject.objects.get(id=pk)
        
        # Serialize the subject using the SubjectSerializer
        serializer = SubjectSerializer(subject, many=False)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_subject(request):
    try:
        student_id = request.data.get('student_id')
        name = request.data.get('name')

        if not student_id or not name:
            return Response(
                {"error": "Both student_id and subject_name are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the student exists
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the subject already exists for the student
        if Subject.objects.filter(student=student, subject=name).exists():
            return Response(
                {"error": "This subject already exists for the student."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the subject
        subject = Subject.objects.create(student=student, subject=name)

        # Serialize the created subject
        serializer = SubjectSerializer(subject)
        return Response(
            {"message": "Subject added successfully.", "subject": serializer.data},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_subject(request, pk):
    try:
        # Retrieve the subject by its ID (primary key)
        subject = Subject.objects.get(id=pk)

        # Create a serializer instance with the existing subject and new data from the request
        serializer = SubjectSerializer(instance=subject, data=request.data)
        
        # Check if the new data is valid
        if serializer.is_valid():
            # Save the updated subject
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_subject(request, pk):
    try:
        # Retrieve the subject by its ID (primary key)
        subject = Subject.objects.get(id=pk)

        # Delete the subject
        subject.delete()
        
        # Return success response
        return Response({'message': 'Subject deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
    except Subject.DoesNotExist:
        # Return error if subject not found
        return Response({'error': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Catch other exceptions and return error
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Marks Views

@api_view(['GET'])
def get_marks(request):
    try:
        student_id = request.query_params.get('student_id')
        subject_name = request.query_params.get('subject_name')
        
        if student_id and subject_name:
            # Filter by student_id and subject_name
            marks = Marks.objects.filter(student__id=student_id, subject__subject=subject_name)
        elif student_id:
            # Filter by student_id
            marks = Marks.objects.filter(student__id=student_id)
        elif subject_name:
            # Filter by subject_name
            marks = Marks.objects.filter(subject__subject=subject_name)
        else:
            # If neither student_id nor subject_name is provided, get all marks
            marks = Marks.objects.all()

        serializer = MarksSerializer(marks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_mark(request, pk):
    try:
        # Get the mark by id (primary key)
        mark = Marks.objects.get(id=pk)

        # If you want to check if the student is the correct one:
        student_id = request.query_params.get('student_id')
        if student_id and mark.student.id != int(student_id):
            return Response({'error': 'Mark not found for this student.'}, status=status.HTTP_404_NOT_FOUND)

        # Return the mark details
        serializer = MarksSerializer(mark, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Marks.DoesNotExist:
        return Response({'error': 'Mark not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_mark(request):
    try:
        # Extract input data
        roll_number = request.data.get('roll_number')
        subject_name = request.data.get('subject_name')
        marks_value = request.data.get('marks')

        if not roll_number or not subject_name or marks_value is None:
            return Response({'error': 'Roll number, subject name, and marks are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the student using the roll number
        student = Student.objects.get(roll=roll_number)
        
        # Check if the subject exists for this student
        subject = Subject.objects.filter(student=student, subject=subject_name).first()
        if not subject:
            return Response({'error': 'Subject does not exist for this student.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if marks for this subject already exist
        if Marks.objects.filter(student=student, subject=subject).exists():
            return Response({'error': 'Marks for this subject already exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the mark entry
        marks = Marks.objects.create(student=student, subject=subject, marks=marks_value)
        marks.save()

        return Response({'message': 'Marks added successfully!'}, status=status.HTTP_201_CREATED)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Student.DoesNotExist:
        return Response({'error': 'Student with the given roll number not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found for the given student.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_mark(request, pk):
    try:
        mark = Marks.objects.get(id=pk)

        # Optional: Validate student_id to ensure it's the correct student
        student_id = request.data.get('student_id')
        if student_id and mark.student.id != int(student_id):
            return Response({'error': 'Mark does not belong to the specified student.'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the data and update the mark
        serializer = MarksSerializer(instance=mark, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Marks.DoesNotExist:
        return Response({'error': 'Mark not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_mark(request, pk):
    try:
        mark = Marks.objects.get(id=pk)

        # Optional: Validate student_id to ensure it's the correct student
        student_id = request.query_params.get('student_id')
        if student_id and mark.student.id != int(student_id):
            return Response({'error': 'Mark does not belong to the specified student.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the mark
        mark.delete()
        return Response({'message': 'Mark deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    except Marks.DoesNotExist:
        return Response({'error': 'Mark not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
