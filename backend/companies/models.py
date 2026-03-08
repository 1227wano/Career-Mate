from django.db import models
from django.conf import settings

# Create your models here.
# 기업 테이블
class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_addr = models.CharField(max_length=1000)

    def __str__(self):
        return self.company_name

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='community_posts')

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment_content[:10]