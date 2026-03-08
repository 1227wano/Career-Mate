<template>
    <div class="post-detail-container">
        <SideBar />
        <div class="post-detail-dashboard" v-if="companyStore.company">
            <header class="post-header">
                <span class="category-tag">{{ postStore.post.category }}</span>
                <h1>{{ postStore.post.post_title }}</h1>
                <div class="post-info">
                    <span class="author">{{ postStore.post.user_info }}</span>
                    <span class="divider">|</span>
                    <span class="date">{{ new Date(postStore.post.created_at).toLocaleString('ko-KR') }}</span>
                </div>
            </header>

            <hr />
            
            <article class="post-content">
                {{ postStore.post.post_content }}
            </article>
            
            <footer class="post-footer">
                <button @click="$router.go(-1)" class="back-btn">목록으로</button>
                <div v-if="isAuthor()" class="author-actions">
                    <button @click="goToEdit" class="edit-btn">수정</button>
                    <button @click="goToDelete" class="delete-btn">삭제</button>
                </div>
            </footer>
            <hr />
            <CommentForm />
            <hr />
            <CommentItem 
            v-for="comment in postStore.post.comments"
            :key="comment.id"
            :comment="comment"/>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCompanyStore } from '@/stores/company';
import { usePostStore } from '@/stores/posts';
import SideBar from '@/components/SideBar.vue';
import CommentForm from '@/components/CommentForm.vue';
import CommentItem from '@/components/CommentItem.vue';

const route = useRoute()
const router = useRouter()
const companyStore = useCompanyStore()
const postStore = usePostStore() 

const companyId = route.params.companyId
const postId = route.params.postId
onMounted(() => {
    postStore.getPost(companyId, postId)
})

const isAuthor = function () {
    return postStore.isPostAuth
}

const goToEdit = function () {
    router.push({
        name: 'PostEditView',
        params: {
            companyId: companyId,
            postId: postId,
        }
    })
}

const goToDelete = function () {
    postStore.deletePost(companyId, postId)
}
</script>

<style scoped>
.post-detail-container{
    display: flex;
    min-height: 100vh;
}
.post-detail-dashboard{
    flex: 1;
    margin-left: 280px;
    padding: 40px;
}

/* 게시글 카드 스타일 */
.post-detail-content-wrapper {
    width: 100%;
    max-width: 900px;
    background: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* 헤더 영역 */
.post-header {
    margin-bottom: 30px;
}

.category-tag {
    display: inline-block;
    padding: 4px 12px;
    background-color: #eef2ff;
    color: #4f46e5;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 15px;
}

.post-header h1 {
    font-size: 2.2rem;
    color: #1f2937;
    margin-bottom: 20px;
    line-height: 1.3;
}

.post-info {
    display: flex;
    align-items: center;
    color: #6b7280;
    font-size: 0.95rem;
}

.author {
    font-weight: 600;
    color: #374151;
}

.divider {
    margin: 0 12px;
    color: #d1d5db;
}

/* 구분선 */
hr {
    border: 0;
    border-top: 1px solid #f1f5f9;
    margin: 30px 0;
}

/* 본문 영역 */
.post-content {
    min-height: 400px;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #4b5563;
    white-space: pre-wrap; /* 줄바꿈 및 공백 유지 */
    word-break: break-all;
}

/* 푸터 및 버튼 영역 */
.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid #f1f5f9;
}

.back-btn {
    padding: 10px 20px;
    background-color: #fff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    color: #4b5563;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.back-btn:hover {
    background-color: #f9fafb;
    border-color: #9ca3af;
}

.author-actions {
    display: flex;
    gap: 10px;
}

.edit-btn, .delete-btn {
    padding: 10px 18px;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.edit-btn {
    background-color: #fff;
    border: 1px solid #4f46e5;
    color: #4f46e5;
}

.edit-btn:hover {
    background-color: #f5f7ff;
}

.delete-btn {
    background-color: #ef4444;
    border: 1px solid #ef4444;
    color: white;
}

.delete-btn:hover {
    background-color: #dc2626;
}
</style>