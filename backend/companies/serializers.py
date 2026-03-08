from rest_framework import serializers
from .models import Company, Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_info = serializers.ReadOnlyField(source='user.name')
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'post',)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' 

class PostSerializer(serializers.ModelSerializer):
    # 조회용
    user_info = serializers.ReadOnlyField(source='user.name')
    company_info = CompanySerializer(source='company', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    # 저장은 field에 company가 포함되어 있기 때문에 id 값이 저장됨
    class Meta:
        model = Post
        fields = (
            'id', 'user', 'user_info', 'post_title', 'post_content', 
            'category', 'company', 'company_info', 'created_at', 
            'comments' 
        )
        read_only_fields = ('user', )


        