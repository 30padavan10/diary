from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import Student, Lesson, CustomUser, Teacher, Grade

from django.db import models


class StudentListSerializer(serializers.ModelSerializer):
    """Вывод списка студентов"""
    class Meta:
        model = Student
        fields = ("user_id", "school_class", "school_number")





# class StuSerializer(serializers.ModelSerializer):
#     fi = TrackListingField(many=True)
#
#     class Meta:
#         model = Teacher
#         fields = ['user', 'fi']


class FioField(serializers.RelatedField):
    def to_representation(self, value):
        return '%s %s' % (value.last_name, value.first_name)


class FioSerializer(serializers.ModelSerializer):
    """Вывод ФИО"""
    #category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = CustomUser
        fields = ("last_name",) # "first_name", "second_name")


# class TeacherDetailSerializer(serializers.HyperlinkedModelSerializer):
#     """Вывод ФИО"""
#     #user = serializers.SlugRelatedField(slug_field="first_name", read_only=True) # вместо поля user можно подставлять
#     # любое поле из связанной модели, но если мне нужны 3 поля для ФИО, то это не подойдет
#
#     last_name = ReadOnlyField(source="user.last_name")
#     first_name = ReadOnlyField(source="user.first_name")
#     second_name = ReadOnlyField(source="user.second_name")
#     #
#     #
#     class Meta:
#         model = Teacher
#         fields = ("last_name", "first_name", "second_name")



class TeacherDetailSerializer(serializers.BaseSerializer):
    """Вывод ФИО"""

    def to_representation(self, value):
        print('!!')
        print(value.user.last_name)
        print(self)
        return '%s %s %s' % (value.user.last_name, value.user.first_name, value.user.second_name)


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


# class GradeListStudentSerializer(serializers.ModelSerializer):
#     """Вывод списка уроков(id) и оценки"""
#     class Meta:
#         model = Grade
#         fields = ("lesson", "grade")


class LessonDetailForGradeSerializer(serializers.ModelSerializer):
    """Вывод данных об уроке"""
    subject = serializers.SlugRelatedField(slug_field="description", read_only=True)
    #lesson_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M") # общий формат времени задается в settings
    class Meta:
        model = Lesson
        #fields = ['subject', 'lesson_date']
        fields =["subject"]


# class GradeListStudentWithDescLesonSerializer(serializers.ModelSerializer):
#     """Вывод списка уроков c оценками для конкретного студента, в таком варианте могут выводиться только стандартные
#      поля, кастомное поле не
#      объявить вывод такой
#         {
#             "lesson": {
#                 "subject": "Русский язык"
#             },
#             "grade": 4
#         },"""
#
#     lesson = LessonDetailForGradeSerializer(read_only=True)
#
#     class Meta:
#         model = Grade
#         fields = ("lesson", "grade")


class AllGradesAutorizedStudentSerializer(serializers.ModelSerializer):
    """Вывод списка уроков c оценками для конкретного студента, в таком варианте можно объявить кастомное поле, вообще
     строим весь вывод самостоятельно как захотим
     вывод такой
     {
        "grade": 4,
        "lesson": "Русский язык"
    },
    """
    def to_representation(self, instance):
        return {
            'grade': instance.grade,
            'lesson': instance.lesson.subject.description,
            'lesson_date': instance.lesson.lesson_date.strftime(format="%d-%m-%Y %H:%M")
        }

    class Meta:
        model = Grade



# class StudentDetailSerializer(serializers.HyperlinkedModelSerializer):
class StudentDetailSerializer(serializers.ModelSerializer):
    """Данный сериалайзер выводит поля с данными о студенте. Поле grades это поле связанной дочерней модели, поэтому оно
    позволяет вывести все связанный записи для данного студента, но как отфильтровать эти все записи чтобы выводилась
    только их части (например фильтровать по предмету и т.д.) я так пока и не понял"""
    #user = serializers.SlugRelatedField(slug_field="first_name", read_only=True) # вместо поля user можно подставлять
    # любое поле из связанной модели, но если мне нужны 3 поля для ФИО, то это не подойдет

    last_name = ReadOnlyField(source="user.last_name")
    first_name = ReadOnlyField(source="user.first_name")
    second_name = ReadOnlyField(source="user.second_name")

    # также есть другие варианты как отобразить related_name поле в документации Serializer relations
    grades = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='grade'
    )

    middle_grade = serializers.FloatField()
    count_grade = serializers.IntegerField()
    #serializers.FloatField()
    # student = Student.objects.filter(user=2).annotate(
    #     middle_grade=models.Count("grades")  # models.Avg('grades__grade')
    # )
    # print('!!student!!')
    # print(student[0].middle_grade)
    class Meta:
        model = Student
        fields = ("last_name", "first_name", "second_name", "grades", "count_grade", "middle_grade")
