from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Grade, Student, Lesson, School, SchoolClass
from .forms import GradeForm


class GradeListView(ListView):
    model = Grade
    context_object_name = 'grades'


class GradeCreateView(CreateView):
    model = Grade
    #fields = ('lesson', 'student', 'grade')
    form_class = GradeForm
    success_url = reverse_lazy('grade_list')


class GradeUpdateView(UpdateView):
    model = Grade
    form_class = GradeForm
    success_url = reverse_lazy('grade_list')


def load_students(request):
    lesson_id = request.GET.get('lesson')
    lesson = Lesson.objects.get(pk=lesson_id)
    students = Student.objects.filter(school_class__class_number=lesson.school_class,
                                      school_class__school_number=lesson.school)
    return render(request, 'diary/dropdownlist.html', {'students': students})
