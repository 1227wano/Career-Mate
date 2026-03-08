from django.contrib import admin
from .models import Resume, ResumeRecommendation # 만든 모델들 가져오기

# 관리자 페이지에 등록(Register)
admin.site.register(Resume)
admin.site.register(ResumeRecommendation)