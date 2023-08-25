from django.urls import path
from . import views

urlpatterns = [
    path("add-student", views.register , name="register"),
    path("", views.login, name="login"),
    path("dashboard/<str:pk>/", views.dashboard, name='dashboard'),
    path("all-student", views.all_student, name="all-student"),
    path("student-details/<int:pk>", views.student_details, name='student-details')
]
