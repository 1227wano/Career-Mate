from rest_framework import serializers
from .models import Resume, ResumeRecommendation
from recruit.models import Job

# 1. 이력서 조회용
class ResumeSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['user', 'original_name', ]

    def get_file_url(self, obj):
        if obj.resume_file:
            return obj.resume_file.url
        return None

# 2. 추천된 채용공고의 상세 정보를 보여주기 위한 시리얼라이저
class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        # 프론트엔드 카드 UI에 띄워줄 핵심 정보만 선택
        fields = ['id', 'company', 'jobs_title', 'jobs_date'] 

# 3. AI 분석 결과(추천 내역) 조회용
class ResumeRecommendationSerializer(serializers.ModelSerializer):
    # Job 모델의 단순 ID가 아니라, 위에서 정의한 JobDetail 정보가 통째로 들어감
    job = JobDetailSerializer(read_only=True)

    class Meta:
        model = ResumeRecommendation
        fields = ['id', 'job', 'match_reason', 'created_at']