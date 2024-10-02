from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max

class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ManyToManyField(Instructor, related_name="courses")

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.ForeignKey(Course, related_name="students", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Exam(models.Model):
    course = models.ForeignKey(Course, related_name="exams", on_delete=models.CASCADE)
    date = models.DateField()
    max_score = models.IntegerField()

    def __str__(self):
        return f"Exam for {self.course.name} on {self.date}"

class ExamResult(models.Model):
    student = models.ForeignKey(Student, related_name="exam_results", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name="results", on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        # Đảm bảo rằng mỗi sinh viên chỉ có thể tham gia một bài kiểm tra một lần
        constraints = [
            models.UniqueConstraint(fields=['student', 'exam'], name='unique_exam_result')
        ]

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.exam.course.name} Exam on {self.exam.date}: {self.score}"

# Custom Manager cho model Student
class StudentManager(models.Manager):
    def top_scorers(self, course):
        return self.filter(course=course).annotate(max_score=Max('exam_results__score')).order_by('-max_score')

# Gán custom Manager cho model Student
Student.objects = StudentManager()
