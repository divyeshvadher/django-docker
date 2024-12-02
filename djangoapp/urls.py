from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_students),
    path('create/', views.add_student),
    path('read/<str:pk>/', views.get_student),
    path('update/<str:pk>/', views.update_student),
    path('delete/<str:pk>/', views.delete_student),
]