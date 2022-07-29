from django.db import models
from django.db.models import Q
from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import SubjectFilter, SubjectFilterFromStudent
from .models import Grade, Student, Lesson, School, SchoolClass, Teacher
from .forms import GradeForm
from .serializers import (
    StudentListSerializer,
    LessonListSerializer,
    LessonDetailSerializer,
    TeacherDetailSerializer,
    # GradeListStudentSerializer,
    AllGradesAutorizedStudentSerializer, StudentDetailSerializer
)


class GradeListView(ListView):
    model = Grade
    context_object_name = 'grades'

    def get(self, request, *args, **kwargs):
        print('////')
        print(request.user.username)
        return super().get(self, request, *args, **kwargs)



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


from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import CustomUser


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('grade_list')


class TeacherSignUpView(CreateView):
    model = CustomUser
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    # def get_context_data(self, **kwargs):
    #     kwargs['user_type'] = 'teatcher'
    #     return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('grade_list')


from .models import Contact
from .forms import ContactForm
from .service import send
from .tasks import send_spam_email

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = "diary/contact.html"

    def form_valid(self, form):
        form.save()
        # send(form.instance.email)  # данная функция отправляет письмо
        print(form.instance.email)
        send_spam_email.delay(form.instance.email) # если запустить саму функцию send_spam_email, то она будет
        # выполняться как обычная функция и будет ждать ответа, а вот метод delay как раз говорит о том что это таска
        # и не нужно ждать ответа, а двигаться дальше
        return super().form_valid(form)



class StudentListView(generics.ListAPIView):
    """Вывод списка студентов с помощью generics класса"""
    serializer_class = StudentListSerializer
    queryset = Student.objects.all()



class LessonListView(generics.ListAPIView):
    """Вывод списка уроков с помощью generics класса"""
    queryset = Lesson.objects.all()
    serializer_class = LessonListSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonDetailView(generics.RetrieveAPIView):
    """Вывод данных об уроке с помощью generics класса"""
    #queryset = Lesson.objects.all()
    queryset = Lesson.objects.select_related('subject', 'school', 'school_class', 'teacher')
    serializer_class = LessonDetailSerializer


class TeacherDetailView(generics.RetrieveAPIView):
    """Вывод данных об уроке с помощью generics класса"""
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailSerializer


class GradeListStudentView(generics.ListAPIView):
    """Вывод списка всех оценок ученика"""
    #queryset = Grade.objects.filter(student=)
    #serializer_class = GradeListStudentSerializer
    serializer_class = AllGradesAutorizedStudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Добавление фильтрации
    #filterset_fields = ['lesson__subject']  # для простых фильтров по id можно обойтись без создания класса фильтра,
    # а фильтровать по полю или по связанному полю, если указать просто lesson, то будет фильтроваться по конкретному
    # уроку здесь, а я через поле lesson добираюсь до предмета и фильтруется по id предмета, чтобы фильтровать по
    # названию, нужен класс фильтра. В модели предметов сейчас только поле в котором предметы называются по русски,
    # нужно доп поле чтобы было по английски и без пробелов.
    # в url добавляется /?lesson__subject=2

    filterset_class = SubjectFilter

    def get_queryset(self):
        """Независимо от того как реализован сериалайзер кверисет не меняется
        http://localhost:8000/grades/?subject=rus"""
        print("!!!")
        print(self.request.query_params.get('subject'))
        grades = Grade.objects.filter(student__user=self.request.user).select_related('lesson', 'lesson__subject')
        return grades


class StudentDetailView(generics.ListAPIView):
    """Вывод данных ученика. Вывод дополнительных полей получилось сделать только используя serializer_class и
     переопределенный метод get_queryset с помощью ListAPIView. RetrieveAPIView тут не подходит, т.к. он ждет в
     адресной строке pk, а у нас пользователь не знает номер под которым зарегистрирован(хотя можно было вместо pk
     поробовать передавать например поле с именем пользователя как слаг в мувис) Пытался переопределить метод get для
      APIView он всегда ругался на то что в queryset нет поля которое я хочу добавить так решение и не нашел.

      Не нашел решения для фильтрации оценок через студента, подробнее в сериализаторе"""
    #queryset = Student.objects.all()
    #serializer_class = GradeListStudentSerializer
    serializer_class = StudentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_class = SubjectFilterFromStudent
    # def get(self, request):
    #     student = Student.objects.filter(user=self.request.user)
    #     #     .annotate(
    #     #     middle_grade=models.Count('grades')
    #     # )
    #     print("!!!")
    #     print(request.user)
    #     serializer = StudentDetailSerializer(student)
    #     return Response(serializer.data)

    def get_queryset(self):
        """Если в доп. поле в Count или Avg добавить filter=Q(grades__lesson__subject__eng_name='rus' и заходить без
        параметров http://localhost:8000/private/ а в SubjectFilterFromStudent subject = filters.CharFilter(field_name='grades__grade')
        то и среднее значение и количетво отображаются корректно, если добавить в запрос ?subject=rus то появляется
        ошибка что какое-то поле grade ждет int, а получает rus. Если я в SubjectFilterFromStudent пишу
        subject = filters.CharFilter(field_name='grades__lesson__subject__eng_name') то все отрабатывает, но тогда
        становится некорректным поле middle_grade в вместо значения 2 выводится значение 4"""
        if self.request.query_params.get('subject'):
            subject_param = self.request.query_params.get('subject')
            student = Student.objects.filter(user=self.request.user).annotate(
                middle_grade=models.Avg('grades__grade', filter=Q(grades__lesson__subject__eng_name=subject_param))).annotate(
                count_grade=models.Count('grades', filter=Q(grades__lesson__subject__eng_name=subject_param))
            )
        else:
            student = Student.objects.filter(user=self.request.user).annotate(
                middle_grade=models.Avg('grades__grade')).annotate(
                count_grade=models.Count('grades')
            )
        return student


