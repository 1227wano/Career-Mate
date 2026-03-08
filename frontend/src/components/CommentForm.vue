<template>
  <div class="comment-form">
    <textarea 
      v-model="commentContent" 
      placeholder="댓글을 남겨보세요."
      @keyup.enter="submitComment"
    ></textarea>
    <div class="form-footer">
      <button @click="submitComment">등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router'; 
import { usePostStore } from '@/stores/posts';

const route = useRoute()
const companyId = route.params.companyId
const postId = route.params.postId

const postStore = usePostStore()
const commentContent = ref('')

const submitComment = function () {
    postStore.createComment(
      commentContent.value, companyId, postId
    )
    commentContent.value = ''
}
</script>

<style scoped>
.comment-form { 
    margin-top: 20px; 
}
textarea {
  width: 100%; 
  height: 80px; 
  padding: 12px;
  border: 1px solid #ddd; 
  border-radius: 8px; 
  resize: none;
}
.form-footer { 
    display: flex; 
    justify-content: flex-end; 
    margin-top: 8px; 
}
button { padding: 8px 16px; 
    background: #4f46e5; 
    color: white; 
    border: none; 
    border-radius: 4px; 
    cursor: pointer; 
}
button:disabled { 
    background: #ccc; 
}
</style>