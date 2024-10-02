from django.shortcuts import render
from .models import Course, Student

def top_scorers_view(request, course_id):
    course = Course.objects.get(id=course_id)
    top_scorers = Student.objects.top_scorers(course)
    
    context = {
        'course': course,
        'top_scorers': top_scorers
    }
    return render(request, 'top_scorers.html', context)
