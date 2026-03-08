from django.db import models
from django.conf import settings
from recruit.models import Job

# 기존 이력서 모델
class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resume/')
    original_name = models.CharField(max_length=100) # 원본 파일명
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

# AI 직무 추천 결과 저장 모델
class ResumeRecommendation(models.Model):
    # 어떤 이력서를 분석했는지 연결
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='recommendations')
    
    # 어떤 채용공고를 추천했는지 연결 (Job 모델의 ID를 저장)
    # 이렇게 하면 job.title, job.company, job.url 등을 다 가져올 수 있음
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommended_resumes')
    
    # AI가 분석한 매칭 사유 (상세 텍스트)
    match_reason = models.TextField(help_text="AI가 분석한 이 공고 추천 사유")
    
    # 분석 시점
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # 최신 추천순 정렬

    def __str__(self):
        return f"[추천] {self.resume.user.username} -> {self.job.company} ({self.job.title})"