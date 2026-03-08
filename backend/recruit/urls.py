from django.urls import path
from . import views


urlpatterns = [
    path('update/', views.update_recruit_db),
    path('', views.job_list),
    path('<int:job_id>/', views.job_detail),
]
