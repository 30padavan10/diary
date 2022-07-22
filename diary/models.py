
from django.db import models


from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     """Предыдущий вариант ... На данный момент я в моделях Студент и Препод наследуюсь от CustomUser который
#      добавляет только 1 поле.
#      в принципе можно наследоваться сразу от AbstractUser в Студент и Препод, просто придется прописать и там и там
#      second_name, что наверно не хорошо... Но еще вопрос, если я сразу наследуюсь от просто User могу ли я добавлять
#      точно также поля в своих моделях и выводить все вместе...модель User также наследуется от AbstractUser
#       и ничего не добавляет"""
#     second_name = models.CharField("Отчество", max_length=100, blank=True)
#     # school_number = models.ForeignKey('School', on_delete=models.CASCADE, verbose_name='Номер школы', blank=True, null=True)
#     # school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE, verbose_name='Номер класса', blank=True, null=True)
#
#     def __str__(self):
#         return self.second_name
#
# # class Human(models.Model):
# #     """Базовый класс человека"""
# #     fio = models.CharField(max_length=100)
#
#
#
# class Teacher(CustomUser):
#     """Преподаватель"""
# #
# #     def __str__(self):
# #         return self.fio
# #
#     class Meta:
#         verbose_name = 'Преподаватель'
#         verbose_name_plural = 'Преподаватели'
#
#
# class Student(CustomUser):
#     school_number = models.ForeignKey('School', on_delete=models.CASCADE, verbose_name='Номер школы', blank=True, null=True)
#     school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE, verbose_name='Номер класса', blank=True, null=True)
# #     """Ученик"""
# #     school_number = models.ForeignKey('School', on_delete=models.CASCADE, verbose_name='Номер школы', default=1)
# #     school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE, verbose_name='Номер класса')
# #     # Когда school_number был в модели SchoolClass как FK и в модели Student не было, то при добавлении класса
# #     # было не понятно к какой школе он относится, поэтому такой вариант наследования неудобен.
# #
# #     def __str__(self):
# #         return self.fio
# #
#     class Meta:
#         verbose_name = 'Ученик'
#         verbose_name_plural = 'Ученики'


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    second_name = models.CharField("Отчество", max_length=100, blank=True)


class Student(models.Model):
    """Ученик"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    school_number = models.ForeignKey('School', on_delete=models.CASCADE, verbose_name='Номер школы')
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE, verbose_name='Номер класса')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.second_name}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Teacher(models.Model):
    """Преподаватель"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.second_name}'

    class Meta:
            verbose_name = 'Преподаватель'
            verbose_name_plural = 'Преподаватели'


class School(models.Model):
    """Школа"""
    school_number = models.IntegerField(verbose_name='Номер школы', unique=True)
    # чтобы при добавлении не дублировались школы и классы добавлено unique=True, но все равно остается момент,
    # что можно выбрать класс которого по факту нет в школе, и лучше фильтровать классы как студентов по урокам.

    def __str__(self):
        return str(self.school_number)

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'


class SchoolClass(models.Model):
    """Класс"""
    class_number = models.CharField(verbose_name='Номер класса', max_length=100, unique=True)
    school_number = models.ForeignKey('School', on_delete=models.CASCADE, verbose_name='Номер школы')


    def __str__(self):
        return self.class_number

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Subject(models.Model):
    """Предмет"""
    eng_name = models.CharField(default='math', max_length=100, verbose_name='Англ сокращение предмета')
    description = models.CharField(max_length=100, verbose_name='Название предмета')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Lesson(models.Model):
    """Урок"""
    #teacher = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lesson_date = models.DateTimeField()

    def __str__(self):
        return f'{self.subject.description} - {self.lesson_date}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Grade(models.Model):
    """Оценка"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    #student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.grade)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Contact(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name

