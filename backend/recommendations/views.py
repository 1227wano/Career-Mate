from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# 모델 import (경로가 다를 경우 수정 필요)
from resumes.models import Resume, ResumeRecommendation
from recruit.models import Job 
from .ai_service import GeminiRecommender

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_jobs(request, resume_id):
    """
    이력서(resume_id) 내용을 분석하여 적합한 채용공고를 추천합니다.
    결과는 DB에 저장되고, 프론트엔드에는 회사명과 공고제목이 포함된 상세 데이터를 반환합니다.
    """
    
    # 1. 이력서 가져오기
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # 2. 채용공고 가져오기 (마감일이 지나지 않은 공고)
    now = timezone.now()
    active_jobs = Job.objects.filter(jobs_date__gte=now).select_related('company').order_by('jobs_date')
    
    # (테스트용) 만약 조회된 공고가 없으면 전체 공고 가져오기
    if not active_jobs.exists():
        active_jobs = Job.objects.select_related('company').all()

    if not active_jobs.exists():
        return Response({"error": "분석할 채용공고가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 3. AI에게 보낼 텍스트 데이터 생성
    job_text_list = ""
    for job in active_jobs:
        # ✅ [수정] 사용자가 알려준 컬럼명 적용 (company_name, jobs_title)
        c_name = job.company.company_name if job.company else "회사명미상"
        title = job.jobs_title
        exp = getattr(job, 'jobs_exp', '경력무관')
        
        # AI가 참고할 텍스트
        job_text_list += f"ID:{job.id}|회사:{c_name}|제목:{title}|조건:{exp}\n"

    # 4. Gemini AI 서비스 호출
    try:
        recommender = GeminiRecommender()
        # 이력서 파일 경로와 공고 목록 텍스트 전달
        ai_result = recommender.get_recommendations(resume.resume_file.path, job_text_list)
    except Exception as e:
        return Response({"error": f"AI 분석 중 오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 5. AI 응답 검증
    if "error" in ai_result:
        return Response({"error": ai_result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 6. 결과 DB 저장 및 응답 데이터 구성
    # 기존 추천 결과 삭제 (새로운 분석으로 갱신)
    ResumeRecommendation.objects.filter(resume=resume).delete()
    
    final_response_data = [] # 프론트엔드에 보낼 최종 리스트

    for item in ai_result.get("recommendations", []):
        try:
            job_id = int(item['job_id'])
            
            # ✅ [최적화] 회사 정보까지 한 번에 가져오기 (select_related)
            target_job = Job.objects.select_related('company').get(id=job_id)
            
            # 6-1. DB에 저장 (추천 기록)
            ResumeRecommendation.objects.create(
                resume=resume,
                job=target_job,
                match_reason=item.get('match_reason', 'AI 추천')
            )
            
            # 6-2. 프론트엔드용 데이터 만들기 (✅ ID 대신 텍스트 넣기!)
            final_response_data.append({
                "job_id": target_job.id,
                "company_name": target_job.company.company_name,  # 👈 회사명 (텍스트)
                "job_title": target_job.jobs_title,               # 👈 공고 제목 (텍스트)
                "match_reason": item.get('match_reason'),         # 추천 사유
                "jobs_date": target_job.jobs_date,                # 마감일
                "jobs_edu": getattr(target_job, 'jobs_edu', ''),  # 학력 (필요시)
            })
            
        except (Job.DoesNotExist, ValueError):
            continue 

    # 7. 최종 결과 반환 (Serializer 안 쓰고 커스텀 리스트 반환)
    return Response(final_response_data, status=status.HTTP_201_CREATED)