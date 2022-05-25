from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Grade

# class PersonListView(ListView):
#     model = Person
#     context_object_name = 'people'


class GradeListView(ListView):
    model = Grade
    context_object_name = 'grades'


# class PersonCreateView(CreateView):
#     model = Person
#     fields = ('name', 'birthdate', 'country', 'city')
#     success_url = reverse_lazy('person_changelist')


class GradeCreateView(CreateView):
    model = Grade
    fields = ('lesson', 'student', 'grade')
    success_url = reverse_lazy('grade_list')

# class PersonUpdateView(UpdateView):
#     model = Person
#     fields = ('name', 'birthdate', 'country', 'city')
#     success_url = reverse_lazy('person_changelist')
