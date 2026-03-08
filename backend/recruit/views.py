from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404

from django.shortcuts import render
from .utils import save_jobs_to_db
from .models import Job
from .serializers import JobSerializer

@api_view(['GET'])
def job_list(request):
    # save_jobs_to_db()
    jobs = get_list_or_404(Job)
    serializers = JobSerializer(jobs, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    serializers = JobSerializer(job)
    return Response(serializers.data)

# 채용공고 업데이트
@api_view(['GET'])
def update_recruit_db(request):
    try:
        # RSS 데이터를 가져와서 DB에 저장하는 함수 실행
        save_jobs_to_db()
        return JsonResponse({'message': '채용공고 업데이트 성공!', 'status': 'success'})
    except Exception as e:
        return JsonResponse({'message': f'에러 발생: {str(e)}', 'status': 'error'}, status=500)

