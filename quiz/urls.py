from django.urls import path
from . import views

urlpatterns = [
    path('take/<int:material_id>/', views.take_quiz, name='take_quiz'),
    path('submit/<int:material_id>/', views.submit_quiz, name='submit_quiz'),
    path('flashcards/<int:material_id>/', views.flashcards_view, name='flashcards'),
    path('retry/<int:material_id>/', views.retry_wrong, name='retry_wrong'),
]