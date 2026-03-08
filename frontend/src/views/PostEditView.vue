<template>
  <div class="edit-container">
      <SideBar />
      <div class="edit-dashboard">
          <button class="back-btn" @click="$router.go(-1)">
              <font-awesome-icon icon="fa-solid fa-arrow-left"></font-awesome-icon>
          </button>
          <header class="edit-header">
              <h2>게시글 수정</h2>
          </header>

          <form @submit.prevent="submitPost" class="edit-form">
              <div class="form-group">
                  <label>카테고리</label>
                  <select v-model="editData.category" class="select-category">
                    <option value="취업 Q&A">취업 Q&A</option>
                    <option value="면접후기">면접후기</option>
                    <option value="현직자이야기">현직자이야기</option>
                  </select>
              </div>

              <div class="form-group">
                  <input 
                      v-model="editData.post_title" 
                      type="text" 
                      placeholder="제목을 입력하세요" 
                      class="title-input"
                      required
                  />
              </div>

              <div class="form-group">
                  <textarea 
                      v-model="editData.post_content" 
                      placeholder="내용을 입력하세요. 기업에 대한 솔직한 이야기를 들려주세요." 
                      class="content-textarea"
                      required
                  ></textarea>
              </div>

              <div class="form-actions">
                  <button type="button" class="cancel-btn" @click="$router.go(-1)">취소</button>
                  <button type="submit" class="submit-btn">수정완료</button>
              </div>
          </form>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompanyStore } from '@/stores/company'
import { usePostStore } from '@/stores/posts' 
import SideBar from '@/components/SideBar.vue';

const route = useRoute()
const router = useRouter()
const companyStore = useCompanyStore()
const postStore = usePostStore()

const props = defineProps({
    companyId: Number,
    postId: Number,
})

const editData = ref({
  post_title: '',
  post_content: '',
  category: '',
  company: props.companyId
})

onMounted(() => {
    postStore.getPost(props.companyId, props.postId)

    if (postStore.post) {
        editData.value = {
            post_title: postStore.post.post_title,
            post_content: postStore.post.post_content,
            category: postStore.post.category,
        }
    }
})


const submitPost = function () {
    console.log(editData.value)
    postStore.editPost(editData.value, props.companyId, props.postId)
}

</script>

<style scoped>
.edit-container{
    display: flex;
    min-height: 100vh;
}
.edit-dashboard{
    flex: 1;
    margin-left: 280px;
    padding: 40px;
}
/* 뒤로가기 */
.back-btn {
  background: none;
  border: none;
  font-size: 1.5rem; /* 아이콘 크기 */
  color: #333;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  margin-bottom: 20px; /* 아래 요소와 간격 */
  border-radius: 50%; /* 호버 시 원형 배경을 위해 */
  width: 40px;
  height: 40px;
}

.back-btn:hover {
  background-color: #f0f0f0; /* 마우스 올렸을 때 연한 회색 배경 */
  color: #0046ff; /* Career Mate 테마색으로 변경 */
  transform: translateX(-3px); /* 왼쪽으로 살짝 움직이는 효과 */
}

/* 게시글 작성 */
.edit-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #333;
}

select, .title-input, .content-textarea {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.title-input {
  font-size: 1rem;
}

.content-textarea {
  min-height: 400px;
  resize: vertical;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.cancel-btn {
  padding: 12px 25px;
  background: #eee;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.submit-btn {
  padding: 12px 35px;
  background: #0046ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.submit-btn:hover {
  background: #0035cc;
}
</style>