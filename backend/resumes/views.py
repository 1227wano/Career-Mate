from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer

# ✅ 이력서 목록 조회 및 업로드 (표준 클래스형 뷰 사용)
class ResumeList(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 내 이력서만 최신순으로 가져오기
        return Resume.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # 파일 업로드 시 파일 원본 이름(original_name)과 작성자(user) 자동 저장
        file_obj = self.request.FILES.get('resume_file')
        serializer.save(
            user=self.request.user,
            original_name=file_obj.name if file_obj else "unknown.pdf"
        )

# ✅ 이력서 상세 조회 및 삭제
class ResumeDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 내 이력서 중에서만 삭제 가능
        return Resume.objects.filter(user=self.request.user)