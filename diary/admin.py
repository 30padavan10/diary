from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, School, SchoolClass, Grade, Subject, Lesson

admin.site.register(Teacher)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fio', 'school_class',)

#admin.site.register(Student)



admin.site.register(School)
admin.site.register(SchoolClass)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'grade')

#admin.site.register(Grade)
admin.site.register(Subject)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_date', 'teacher', 'school', 'school_class', 'subject')

#admin.site.register(Lesson)