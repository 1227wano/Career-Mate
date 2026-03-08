from django.urls import path
from . import views

urlpatterns = [
    # 1. 목록 조회(GET) & 업로드(POST)를 한 곳에서 해결!
    # 주소: /api/resumes/
    path('', views.ResumeList.as_view(), name='resume_list'),

    # 2. 삭제 (DELETE)
    # 주소: /api/resumes/1/delete/
    path('<int:pk>/delete/', views.ResumeDetail.as_view(), name='delete_resume'),
]