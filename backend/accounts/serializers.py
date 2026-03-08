from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import UserTerms

class CustomRegisterSerializer(RegisterSerializer):
    # 이미지에 정의된 추가 필드 정의
    name = serializers.CharField(max_length=100)
    birthdate = serializers.DateField()
    phone = serializers.CharField(max_length=100)

    def get_cleaned_data(self):
        # 기본 필드 데이터(username, email, password 등) 가져오기
        data = super().get_cleaned_data()
        # 추가 필드 데이터 주입
        data['name'] = self.validated_data.get('name')
        data['birthdate'] = self.validated_data.get('birthdate')
        data['phone'] = self.validated_data.get('phone')
        return data

    def save(self, request):
        # 유저 객체 생성 (기본 필드 저장)
        user = super().save(request)
        # 커스텀 필드 저장
        user.name = self.validated_data.get('name')
        user.birthdate = self.validated_data.get('birthdate')
        user.phone = self.validated_data.get('phone')
        user.save()

        # 약관 동의 내역 저장 로직
        terms_data = request.data.get('terms', {})
        UserTerms.objects.create(
            user=user,
            service_agreed=terms_data.get('service', False),
            privacy_agreed=terms_data.get('privacy', False),
            marketing_agreed=terms_data.get('marketing', False)
        )
        return user