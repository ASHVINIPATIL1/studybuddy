from django.db import models
from django.contrib.auth.models import User
from materials.models import StudyMaterial
from quiz.models import Question
from django.utils import timezone
from datetime import timedelta

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100)

class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)