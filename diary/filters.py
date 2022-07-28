from django_filters import rest_framework as filters
from .models import Grade, Student

class CharFilterInFilter(filters.CharFilter): #filters.BaseInFilter:
    """
    Чтобы использовать lookup_expr='in' нужен класс BaseInFilter. lookup_expr определяет каким образом фильтровать.
    Жанры это поле М2М и в таблице связывающей фимьм - жанр используются id, а искать нужно по названию, поэтому
    потребуется CharFilter. По умолчанию фильтрация идет по id.
    """
    pass


class SubjectFilter(filters.FilterSet):
    """Данный класс позволяет сделать фильтр по названию предмета. Модель в мета должна быть точно такой же как и в
     queryset. CharFilterInFilter тут не нужен т.к. у меня не М2М поле"""
    subject = filters.CharFilter(field_name='lesson__subject__eng_name')
    #year = filters.RangeFilter()  # диапазон дат от мин до мах

    class Meta:
        model = Grade
        fields = ['subject']


class SubjectFilterFromStudent(filters.FilterSet):
    """Данный класс позволяет сделать фильтр по названию предмета. Модель в мета должна быть точно такой же как и в
     queryset. CharFilterInFilter тут не нужен т.к. у меня не М2М поле"""
    #subject = filters.CharFilter(field_name='grades__lesson__subject__eng_name')
    subject = filters.CharFilter(field_name='grades__grade')
    #year = filters.RangeFilter()  # диапазон дат от мин до мах

    class Meta:
        model = Student
        fields = ['subject']