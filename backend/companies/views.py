from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from django.shortcuts import render
from .models import Company, Post, Comment
from .serializers import CompanySerializer, PostSerializer, CommentSerializer


# Create your views here.
# 회사 상세 정보 가져오기
@api_view(['GET'])
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    serializers = CompanySerializer(company)
    return Response(serializers.data)

# 회사 커뮤니티 게시글 조회
@api_view(['GET'])
def get_posts(request, company_id):
    posts = get_list_or_404(Post, company=company_id)
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data)

# 회사 커뮤니티 내 게시글 생성 
@api_view(['POST'])
def create_post(request, company_id):
    serializers = PostSerializer(data=request.data)
    if serializers.is_valid(raise_exception=True):
        serializers.save(user=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    
# 회사 커뮤니티 상세 게시글 조회, 삭제 
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_post(request, company_id, post_id):
    post = get_object_or_404(Post, company=company_id, id=post_id)
    if request.method == 'GET':
        serializers = PostSerializer(post)
        return Response(serializers.data)
    
    elif request.method == 'DELETE':
        if post.user != request.user:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 내 게시글 수정 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_post(request, company_id, post_id):
    post = get_object_or_404(Post, company=company_id, id=post_id)
    if post.user != request.user:
        return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)

# 댓글 생성 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, company_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    serializers = CommentSerializer(data=request.data)
    if serializers.is_valid(raise_exception=True):
        serializers.save(user=request.user, post=post)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def delete_edit_comment(request, company_id, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'DELETE':
        # 본인 확인
        if comment.user != request.user:
            return Response({'detail': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PUT':
        # 본인 확인
        if request.user != comment.user:
            return Response({'detail': '권한이 없습니다.'}, status=403)
            
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data)
