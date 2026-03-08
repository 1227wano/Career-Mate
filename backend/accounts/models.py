from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=1, default='N')

class UserTerms(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='terms_agreement')
    service_agreed = models.BooleanField(default=False)    # 서비스 이용약관
    privacy_agreed = models.BooleanField(default=False)    # 개인정보 처리방침
    marketing_agreed = models.BooleanField(default=False)  # 마케팅 수신 동의
    agreed_at = models.DateTimeField(auto_now_add=True)    # 동의 시점 기록

    def __str__(self):
        return f"{self.user.username} - Terms Agreement"