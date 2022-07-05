from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import Student, Lesson, CustomUser, Teacher


class StudentListSerializer(serializers.ModelSerializer):
    """Вывод списка студентов"""
    class Meta:
        model = Student
        fields = ("user_id", "school_class", "school_number")





class FioSerializer(serializers.ModelSerializer):
    """Вывод ФИО"""
    #category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = CustomUser
        fields = ("last_name",) # "first_name", "second_name")


class TeacherDetailSerializer(serializers.HyperlinkedModelSerializer):
    """Вывод ФИО"""
    #user = serializers.SlugRelatedField(slug_field="first_name", read_only=True) # вместо поля user можно подставлять
    # любое поле из связанной модели, но если мне нужны 3 поля для ФИО, то это не подойдет

    last_name = ReadOnlyField(source="user.last_name")
    first_name = ReadOnlyField(source="user.first_name")
    second_name = ReadOnlyField(source="user.second_name")
    fio = serializers.CharField()


    #second_name = serializers.SerializerMethodField('second_name')
    #
    # def second_name(self, customuser):
    #     return customuser.second_name

    class Meta:
        model = Teacher
        fields = ("last_name", "first_name", "second_name") # "first_name", "second_name")


class LessonDetailSerializer(serializers.ModelSerializer):
    """Вывод данных об уроке"""
    school = serializers.SlugRelatedField(slug_field="school_number", read_only=True)
    school_class = serializers.SlugRelatedField(slug_field="class_number", read_only=True)
    subject = serializers.SlugRelatedField(slug_field="description", read_only=True)
    teacher = TeacherDetailSerializer(read_only=True)
    lesson_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M") # общий формат времени задается в settings
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonListSerializer(serializers.ModelSerializer):
    """Вывод списка уроков"""
    class Meta:
        model = Lesson
        fields = ("lesson_date", "subject")
