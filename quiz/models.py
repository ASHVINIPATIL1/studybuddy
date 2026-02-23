from django.db import models
from django.contrib.auth.models import User
from materials.models import StudyMaterial

class Question(models.Model):
    DIFFICULTY_CHOICES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    TYPE_CHOICES = [('mcq', 'MCQ'), ('flashcard', 'Flashcard')]

    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=300, blank=True)
    option_b = models.CharField(max_length=300, blank=True)
    option_c = models.CharField(max_length=300, blank=True)
    option_d = models.CharField(max_length=300, blank=True)
    correct_answer = models.CharField(max_length=300)
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='mcq')

    def __str__(self):
        return self.question_text[:50]

class Flashcard(models.Model):
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()

    def __str__(self):
        return self.front[:50]