<template>
  <div class="comment-item">
    <div class="comment-header">
      <span class="author">{{ comment.user_info }}</span>
      <span class="date">{{ new Date(comment.created_at).toLocaleDateString() }}</span>
    </div>
    <div class="comment-body">
      <div v-if="isEditing">
        <textarea v-model="editContent" class="edit-textarea"></textarea>
        <div class="edit-actions">
          <button @click="submitUpdate">저장</button>
          <button @click="toggleEdit">취소</button>
        </div>
      </div>
      <div v-else>
        <p class="content">{{ comment.comment_content }}</p>
        <div v-if="isAuthor(comment.user)" class="comment-actions">
          <button @click="editComment">수정</button>
          <button @click="deleteComment" class="delete-btn">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePostStore } from '@/stores/posts'
import { useRoute } from 'vue-router'

const postStore = usePostStore()
const route = useRoute()

const props = defineProps({
  comment: Object,
})
const companyId = route.params.companyId
const postId = route.params.postId
const isEditing = ref(false) 
const editContent = ref(props.comment.comment_content)

const isAuthor = function (commentUserId) {
    return postStore.isCommentAuth(commentUserId)
}

const deleteComment = function () {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    postStore.deleteComment(companyId, postId, props.comment.id)
  }
}

const editComment = function () {
  isEditing.value = true
}
// 수정 모드 전환
const toggleEdit = () => {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    editContent.value = props.comment.comment_content // 취소 시 원래 내용으로 복구
  }
}

// 수정 서버 전송
const submitUpdate = () => {
  if (!editContent.value.trim()) return
  postStore.editComment(
    companyId, 
    postId, 
    props.comment.id, 
    editContent.value
  )
  isEditing.value = false // 완료 후 일반 모드로 변경
}
</script>

<style scoped>
.comment-item { 
    padding: 15px 0; 
    border-bottom: 1px solid #eee; 
}
.comment-header { 
    font-size: 0.9rem; 
    margin-bottom: 5px; 
}
.author { 
    font-weight: bold; 
    margin-right: 10px; 
}
.date { 
    color: #888; 
}
.content { 
    line-height: 1.5; 
    margin: 5px 0; 
}

/* 버튼 공통 스타일 */
.comment-actions, .edit-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

button {
  padding: 4px 12px;
  font-size: 0.85rem;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

/* 수정 버튼 */
.edit-btn, button:contains("저장") {
  background-color: #f0f0f0;
  color: #555;
}

.edit-btn:hover {
  background-color: #e0e0e0;
}

/* 삭제 버튼 */
.delete-btn {
  background-color: transparent;
  color: #ff4d4f;
  border-color: #ffccc7;
}

.delete-btn:hover {
  background-color: #fff1f0;
  border-color: #ff4d4f;
}

/* 저장 버튼 (강조) */
button:nth-child(1) { /* 수정 모드에서의 첫 번째 버튼(저장) */
  background-color: #4caf50;
  color: white;
}

button:nth-child(1):hover {
  background-color: #45a049;
}

/* 취소 버튼 */
button:nth-child(2) { /* 수정 모드에서의 두 번째 버튼(취소) */
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

/* 수정 모드 - 텍스트 입력창 */
.edit-textarea {
  width: 100%;
  min-height: 80px;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.9rem;
  resize: vertical; /* 세로 크기 조절 허용 */
  margin-bottom: 0.5rem;
}

.edit-textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.1);
}
</style>