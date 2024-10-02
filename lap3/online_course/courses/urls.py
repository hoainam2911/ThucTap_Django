from django.urls import path
from .views import top_scorers_view

urlpatterns = [
    path('courses/<int:course_id>/top_scorers/', top_scorers_view, name='top_scorers'),
]
