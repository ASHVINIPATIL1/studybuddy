from django.contrib import admin
from .models import StudyMaterial, ChatMessage, MaterialFile

admin.site.register(StudyMaterial)
admin.site.register(ChatMessage)
admin.site.register(MaterialFile)