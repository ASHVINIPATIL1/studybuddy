from django.db import models
from django.contrib.auth.models import User

class StudyMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MaterialFile(models.Model):
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='materials/')
    filename = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

class ChatMessage(models.Model):
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']