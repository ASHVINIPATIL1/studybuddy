from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_material, name='upload'),
    path('material/<int:pk>/', views.material_detail, name='material_detail'),
    path('material/<int:pk>/delete/', views.delete_material, name='delete_material'),
    path('material/<int:pk>/chat/', views.chat_view, name='chat'),
    path('material/<int:pk>/generate/', views.generate_content, name='generate_content'),
]