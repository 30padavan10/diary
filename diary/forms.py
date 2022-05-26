from .models import Student, Lesson, Grade
from django import forms


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('lesson', 'student', 'grade')

    def __init__(self, *args, **kwargs):
        """в данном методе переопределяем стандартый queryset(objects.all) на пустой"""
        super().__init__(*args, **kwargs)
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
