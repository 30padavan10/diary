from . import views
from django.urls import path

urlpatterns = [
    path('', views.GradeListView.as_view(), name='grade_list'),
    path('add/', views.GradeCreateView.as_view(), name='grade_add'),
    path('<int:pk>/', views.GradeUpdateView.as_view(), name='grade_change'),
    path('ajax/load-students/', views.load_students, name='ajax_load_students'),
]