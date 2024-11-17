from django.urls import path
from .views import chatbot, home, get_unanswered_questions, submit_answers

urlpatterns = [
    path('', home, name='home'),
    path('chat/', chatbot, name='chatbot'),
    path('unanswered/', get_unanswered_questions, name='get_unanswered_questions'),
    path('submit-answers/', submit_answers, name='submit_answers'),
]
