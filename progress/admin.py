from django.contrib import admin
from .models import QuizAttempt, AttemptAnswer

admin.site.register(QuizAttempt)
admin.site.register(AttemptAnswer)