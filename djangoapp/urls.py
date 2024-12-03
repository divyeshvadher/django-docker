from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_students),
    path('create/', views.add_student),
    path('read/<str:pk>/', views.get_student),
    path('update/<str:pk>/', views.update_student),
    path('delete/<str:pk>/', views.delete_student),
    
    path('subjects/', views.get_subjects),
    path('subject/<str:pk>/', views.get_subject),
    path('add-subject/', views.add_subject),
    path('update-subject/<str:pk>/', views.update_subject),
    path('delete-subject/<str:pk>/', views.delete_subject),
    
    # path('marks/', views.get_marks),
    # path('mark/<str:pk>/', views.get_mark),
    # path('add-mark/', views.add_mark),
    # path('update-mark/<str:pk>/', views.update_mark),
    # path('delete-mark/<str:pk>/', views.delete_mark),
]