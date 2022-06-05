from .models import Student, Lesson, Grade, CustomUser
from django import forms

from django.contrib.auth.models import User


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('lesson', 'student', 'grade')

    def __init__(self, *args, **kwargs):
        """в данном методе переопределяем стандартый queryset(objects.all) на пустой"""
        super().__init__(*args, **kwargs)
        print('!!!!')
        print(self.fields['student'].queryset)
        self.fields['student'].queryset = Student.objects.none()

        if 'lesson' in self.data:
            try:
                lesson_id = int(self.data.get('lesson'))
                lesson = Lesson.objects.get(pk=lesson_id)
                self.fields['student'].queryset = Student.objects.filter(school_class__class_number=lesson.school_class)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['student'].queryset = self.instance.lesson.school_class.student_set.order_by('fio')


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from .models import Teacher, Student

# class TeacherCreationForm(UserCreationForm):
#
#     class Meta:
#         model = Teacher
#         fields = ('username', 'password', 'first_name', 'last_name', 'fio')
#
# class TeacherChangeForm(UserChangeForm):
#
#     class Meta:
#         model = Teacher
#         fields = ('username', 'password', 'first_name', 'last_name', 'fio')
#
#
# class StudentCreationForm(UserCreationForm):
#
#     class Meta:
#         model = Student
#         fields = ('username', 'password', 'first_name', 'last_name', 'fio', 'school_number', 'school_class')
#
# class StudentChangeForm(UserChangeForm):
#
#     class Meta:
#         model = Student
#         fields = ('username', 'password', 'first_name', 'last_name', 'fio', 'school_number', 'school_class')


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        #fields = ('username', 'email')
        fields = ('username', 'email', 'first_name', 'last_name', 'second_name')  #'school_number', 'school_class'
        #fields = ('username', 'password', 'first_name', 'last_name', 'fio', 'school_number', 'school_class')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        #fields = ('username', 'email')
        fields = ('username', 'email', 'first_name', 'last_name', 'second_name')
        #fields = ('username', 'password', 'first_name', 'last_name', 'fio', 'school_number', 'school_class')


from django.db import transaction

from .models import Student, School, SchoolClass

class StudentSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(      # пример множественного выбора
    #     queryset=Subject.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )
    school_number = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(), empty_label=None)
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all(), widget=forms.Select(), empty_label=None)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'first_name', 'second_name', 'last_name')

    @transaction.atomic  # позволяет выполнять в одну транзакцию к БД
    def save(self):
        print('!!!')
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user, school_number=self.cleaned_data.get('school_number'), school_class=self.cleaned_data.get('school_class'))
        # student.school_number.add(*self.cleaned_data.get('school_number')) # не работает в моем случае, т.к.
        # при создании студента поля школы и класса не могут быть null
        # student.school_class.add(*self.cleaned_data.get('school_class'))
        return user


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user