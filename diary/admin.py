from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, School, SchoolClass, Grade, Subject, Lesson

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(School)
admin.site.register(SchoolClass)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Lesson)