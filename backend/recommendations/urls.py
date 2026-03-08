from django.urls import path
from . import views

urlpatterns = [
    path('recommend/<int:resume_id>/', views.recommend_jobs, name='recommend_jobs'),
]