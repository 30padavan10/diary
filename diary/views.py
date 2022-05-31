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
    """Для данного метода cкрипт создающий ajax запрос находится в grade_form.html"""
    lesson_id = request.GET.get('lesson')
    lesson = Lesson.objects.get(pk=lesson_id)
    students = Student.objects.filter(school_class__class_number=lesson.school_class,
                                      school_number__school_number=lesson.school.school_number)
    return render(request, 'diary/dropdownlist.html', {'students': students})




def filter_students_by_lesson(request):
    """Данный метод дублирует метод load_students, нужен для описания процесса добавления фильтра в админку
    1. Находим шаблон change_form.html в файлах админки джанго, он находится по пути
    venv/Lib/site-packages/django/contrib/admin/templates/admin/change_form.html
    2. Копируем по пути templates/admin/diary/grade/change_form.html папка templates должна быть добавлена
    в settings TEMPLATES DIRS os.path.join(BASE_DIR, 'templates')
    3. Добавляем скрипт, который будет отвечать за обновление селекта select_students.js по пути
    static/admin/js/admin/select_students.js
    4. В шаблон change_form.html добавляем <script src="{% static 'admin/js/admin/select_students.js' %}"></script>
    5. В urls добавляем путь на данный view.
    Скрипт select_students.js при изменении значения в поле Урок отправляет ajax запрос на бекенд на данный view
    со значением id урока. Данный view на основе id урока формирует queryset учеников и рендерит его с помощью
    шаблона diary/dropdownlist.html  dropdownlist для поля ученик отображает переданный список учеников"""
    lesson_id = request.GET.get('lesson')
    print('!!')
    print(request.GET)


    lesson = Lesson.objects.get(pk=lesson_id)
    print('!!')
    print(type(lesson.school_class))
    print(type(lesson.school))
    students = Student.objects.filter(school_class__class_number=lesson.school_class,
                                      school_number__school_number=lesson.school.school_number)
    # в lesson.school_class и lesson.school хранятся экземпляры классов SchoolClass и School
    # когда фильтруем учеников, то для соответствия полю school_number нужно обращаться к lesson.school.school_number
    # а для class_number не обязательно писать lesson.school_class.class_number достаточно только lesson.school_class
    # однозначного ответа нет но разница есть в том что school_class - поле типа CharField, а school_number - поле типа
    # IntegerField
    print('!!!!')
    print(students)
    #return JsonResponse({x.id: str(x) for x in students})
    return render(request, 'diary/dropdownlist.html', {'students': students})