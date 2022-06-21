from django.contrib import admin

# Register your models here.
from .models import School, SchoolClass, Grade, Subject, Lesson, Student #Teacher

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm # StudentCreationForm, StudentChangeForm,
from .models import CustomUser


# class TeacherAdmin(UserAdmin):
# #     add_form = TeacherCreationForm
# #     form = TeacherChangeForm
# #     model = Teacher
# #     list_display = ['username', 'password', 'first_name', 'last_name', 'fio']
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal info"), {"fields": ("first_name", "last_name", "second_name", "email")}),
#         (
#             (("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         )),
#         (("Important dates"), {"fields": ("last_login", "date_joined")}),
#         #(("School"), {"fields": ("school_number", "school_class")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("username", "password1", "password2", "second_name"),
#             },
#         ),
#         #(("School"), {"fields": ("school_number", "school_class")}),
#     )
#
# admin.site.register(Teacher, TeacherAdmin)

class SchoolInline(admin.TabularInline):  # TabularInline - суть таже, оформление другое
    model = Student
    extra = 1
    #readonly_fields = ("school_number", "school_class")


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = CustomUser
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "second_name", "email")}),
        (
            (("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_student",
                    "is_teacher",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        )),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
        #(("School"), {"fields": ("school_number", "school_class")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_student", "is_teacher"),
            },
        ),
        #(("School"), {"fields": ("school_number", "school_class")}),
    )

    # def get_inline_instances(self, request, obj=None):
    #     return super().get_inline_instances(request)

    def get_inlines(self, request, obj):
        """Hook for specifying custom inlines.
        request.user - тот юзер который в админке
        obj - экземпляр студента который создается/редактируется
        """
        print('obj')
        print(obj)
        if obj and obj.is_student:
            if not self.inlines:
                self.inlines.append(SchoolInline)
        return self.inlines

    #inlines = [SchoolInline]
    #list_display = ['email', 'username', ]
    #list_display = ('username', 'email', 'first_name', 'last_name', 'second_name', 'school_number', 'school_class')
    #list_display = ('username', 'password', 'first_name', 'last_name', 'fio', 'school_number', 'school_class')



# class StudentAdmin(UserAdmin):
#     # add_form = StudentCreationForm
#     # form = StudentChangeForm
#     # model = Student
#     # list_display = ('username', 'password', 'first_name', 'last_name', 'fio', 'school_number', 'school_class')
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal info"), {"fields": ("first_name", "last_name", "second_name", "email")}),
#         (
#             (("Permissions"),
#              {
#                  "fields": (
#                      "is_active",
#                      "is_staff",
#                      "is_superuser",
#                      "groups",
#                      "user_permissions",
#                  ),
#              },
#              )),
#         (("Important dates"), {"fields": ("last_login", "date_joined")}),
#         # (("School"), {"fields": ("school_number", "school_class")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("username", "password1", "password2", "second_name"),
#             },
#         ),
#         # (("School"), {"fields": ("school_number", "school_class")}),
#     )
#
# admin.site.register(Student, StudentAdmin)




class AllFieldModelAdminMixin(object):
    """Класс добавляющий все поля модели в list_display кроме id """
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(AllFieldModelAdminMixin, self).__init__(model, admin_site)

admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Student, StudentAdmin)
# admin.site.register(Student)
# # admin.site.register(Teacher)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_number', 'school_class')

#admin.site.register(Student)



admin.site.register(School)

@admin.register(SchoolClass)
class SchoolClassAdmin(AllFieldModelAdminMixin, admin.ModelAdmin):
    pass
#admin.site.register(SchoolClass)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'grade')

    # варианты того как вместо всех учеников выводить фильтрованный спискок по какому то статичному параметру
    # хотел чтобы в админке выводился список учеников конкретного класса в зависимости от класса который был
    # на выбранном уроке, но данный финт не провернуть без ajax запроса, поэтому методы ниже не подходят

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(GradeAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['student'].queryset = Student.objects.filter(school_class='1')
    #     return form
    #
    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['student'].queryset = Student.objects.filter(school_class__class_number='1Б')
    #     return super(GradeAdmin, self).render_change_form(request, context, *args, **kwargs)

#admin.site.register(Grade)
admin.site.register(Subject)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_date', 'teacher', 'school', 'school_class', 'subject')

#admin.site.register(Lesson)


from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email")