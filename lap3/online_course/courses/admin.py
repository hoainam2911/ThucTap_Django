from django.contrib import admin
from .models import Instructor, Course, Student, Exam, ExamResult

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(ExamResult)
