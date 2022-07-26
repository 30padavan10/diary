from . import views
from django.urls import path

urlpatterns = [
    path('', views.GradeListView.as_view(), name='grade_list'),
    path('add/', views.GradeCreateView.as_view(), name='grade_add'),
    path('<int:pk>/', views.GradeUpdateView.as_view(), name='grade_change'),
    path('ajax/load-students/', views.load_students, name='ajax_load_students'),
    path('filter_students_by_lesson/', views.filter_students_by_lesson),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('student/', views.StudentListView.as_view()),
    path('private/', views.StudentDetailView.as_view()),
    path('lesson/', views.LessonListView.as_view()),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetailView.as_view()),
    path('grades/', views.GradeListStudentView.as_view()),
]
