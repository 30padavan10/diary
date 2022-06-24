from django.contrib import admin

from .models import School, SchoolClass, Grade, Subject, Lesson, Student, Teacher

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

# для пробы
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import transaction

class SignUpForm(UserCreationForm):
    """Вообще не получилось воспользоваться сохранением в данных формах SignUpForm и SignUpChangeForm, потому что во
    views сохранение в таблицу и преподавателя и ученика происходит вручную в UserCreationForm, а я хотел добиться
    чтобы сохранение в админке было через Inline в UserChangeForm"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'second_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        print('def save')
        print(self)
        print(user)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SignUpChangeForm(UserChangeForm):
    """Объяснение выше"""
    class Meta:
        model = CustomUser
        fields = "__all__"


class TeacherInline(admin.StackedInline):
    """Данный класс нужен чтобы добавить поля модели преподаватель, из которых есть только поле ФК пользователя в форму
    редактирования пользователя UserChangeForm, по задумке должна была создаваться запись и в таблице преподавателей,
    как в случае с учениками, но так не работает, даже если указать fields = ("user",)
    Не используется оставил на память
    """
    model = Teacher
    fields = ("user",)
    extra = 1


class SchoolInline(admin.TabularInline):
    """Данный класс нужен чтобы добавить поля модели ученик в форму редактирования пользователя UserChangeForm"""
    model = Student
    extra = 1


class CustomUserAdmin(UserAdmin):
    """Новый класс на основе UserAdmin чтобы можно было менять поля на странице создания пользователя в админке
    inlines = [SchoolInline]  - вместо такого определения используется get_inlines
    list_display = ('username', 'email', 'first_name', 'last_name', 'second_name', 'school_number', 'school_class')
    вместо list_display используется fieldsets и add_fieldsets
    add_fieldsets - это поля которые выводятся на странице создания пользователя(логин, пароль) за это отвечает
    UserCreationForm
    fieldsets - это поля которые выводятся на странице изменения пользователя(все остальные поля) за это отвечает
    UserChangeForm
    Суть такая - в UserAdmin стандартные формы add_form = UserCreationForm и form = UserChangeForm. При создании
    пользователя сначала отрабатывает UserCreationForm и показывает (логин, пароль), при нажатии сохранить, пользователь
    сохраняется в БД и происходит перенаправление на UserChangeForm которая показывает остальные поля для заполнения.
    Также для редактирование в дальнейшем используется UserChangeForm.
    Пытался написать свои add_form и form для управления SignUpForm и SignUpChangeForm, но работа в этом направлении
    не пошла, т.к. если для создания пользователя из views я использовал формы, то там у меня были отдельные формы для
    ученика и преподавателя, то в админке не понял это определить в рамках одной формы
    """
    # add_form = SignUpForm
    # form = SignUpChangeForm
    model = CustomUser
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

    def save_model(self, request, obj, form, change):
        """Т.к. через get_inlines не удалось добиться сохранения связанной модели учителя, т.к. в нем нет
        дополнительных полей которые можно было бы выбрать. В данном методе если объект это пользователь учитель, то
        сохраняем модель пользователя и вручную создаем связанную модель учителя и сохраняем его, тогда inline для
        учетеля совсем не потребуется"""
        if form.is_valid():
            if obj.is_teacher:
                user = form.save()
                teacher = Teacher()
                teacher.user = user
                teacher.save()
        super().save_model(request, obj, form, change)

    def get_inlines(self, request, obj):
        """Hook for specifying custom inlines.
        request.user - тот юзер который в админке
        obj - экземпляр студента который создается/редактируется
        данный метод нужен: т.к. при добавлении стандарного inlines = [AnythingInline,] на страницу будет добавляться
        связанная модель, но т.к. у меня модель пользователя с вариантами (ученик, учитель), то для учетеля мне не
        нужен inlines модели School, поэтому переопредел этот метод чтобы в зависимости от того какой будет
        пользователь добавлять или не добавлять нужный inline, изначально был только SchoolInline и не было модели
        учитель, когда модель учитель появилась добавился TeacherInline, но потом заметил, что при создании
        пользователя учитель, не добавляется запись в связанную таблицу учителей и если у пользователя ученик не
        выбирать значения полей связанной модели School, то запись ученик тоже не создается. По итогу так и не нашел
        то место где определяется добавление/недобавления записи в связанную таблицу.
        """
        self.inlines = []
        if obj and obj.is_student:
            #if not self.inlines:
            self.inlines.append(SchoolInline)
        elif obj and obj.is_teacher:
            #if not self.inlines:
            self.inlines.append(TeacherInline)
        return self.inlines

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        В процессе поиска места где будет определяться сохранять/несохранять модель inlines нашел данный метод. Здесь:
        form - это html-текст всей страницы
        formset - это html-текст полей inline
        change - True если данные в полях менялись
        """
        super().save_formset(request, form, formset, change)



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

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)

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