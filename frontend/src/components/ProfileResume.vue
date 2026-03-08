<template>
    <section class="resume-manage-card">
        <div class="card-header">
          <h3>내 이력서 관리</h3>
          <!-- <span class="count">총 {{ resumes.length }}개</span> -->
        </div>
        
        <p v-if="profileStore.resumes.length === 0" class="resume-item">나의 이력서가 없습니다.</p>
        <ul class="resume-list">
            <li 
            v-for="resume in profileStore.resumes" 
            :key="resume.id" 
            class="resume-item">
                <div class="resume-info"
                @click="openViewer(resume.file_url)">
                <font-awesome-icon icon="fa-solid fa-file-lines" class="file-icon" />
                <div>
                    <span class="resume-title">{{ resume.original_name }}</span>
                    <span class="resume-date">{{ new Date(resume.created_at).toLocaleString('ko-KR') }}</span>
                </div>
                </div>
                <div class="resume-actions">
                <button class="action-btn delete" @click="confirmDelete(resume.id)">삭제</button>
                </div>
            </li>
        </ul>
        <input 
            type="file" 
            ref="fileInput" 
            @change="handleFileUpload" 
            accept=".pdf,.doc,.docx" 
            style="display: none" 
        />
        <button class="add-resume-btn" @click="triggerFileUpload">+ 새 이력서 불러오기</button>
    </section>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useProfileStore } from '@/stores/profile';
    import axios from 'axios';

    const fileInput = ref(null)

    const profileStore = useProfileStore() 

    // 1. 이력서 가져오기
    // 컴포넌트가 로드되자마자 실행
    onMounted(() => {
        profileStore.getResume()
    })

    // 2. 파일 선택창 열기
    const triggerFileUpload = () => {
        fileInput.value.click();
    };

    // 3. 파일 업로드
    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            // 스토어의 함수에 '실제 파일 객체'를 전달합니다.
            profileStore.postResume(file);
            
            // 업로드 후 같은 파일을 다시 올릴 수 있도록 초기화해줍니다.
            event.target.value = '';
        }
    }

    // 4. 파일 뷰어
    const openViewer = (file_url) => {
        if (!file_url) return;
        window.open(`http://localhost:8000${file_url}`, '_blank');
    }

    // 5. 파일 삭제
    const confirmDelete = (id) => {
        if (confirm("정말 삭제하시겠습니까?")) {
            profileStore.deleteResume(id);
        }
    }
</script>

<style scoped>
.resume-list { 
    list-style: none; 
    padding: 0; 
    margin-bottom: 20px; 
}
.resume-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}
.resume-info { 
    display: flex; 
    align-items: center; 
    gap: 12px; 
}
.file-icon { 
    color: #4f46e5; 
    font-size: 20px; 
}
.resume-title { 
    display: block; 
    font-weight: 600; 
    color: #333; 
}
.resume-date { 
    font-size: 12px; 
    color: #999; 
}
.action-btn { 
    background: none; 
    border: none; 
    color: #4f46e5; 
    cursor: pointer; 
    margin-left: 10px; 
}
.action-btn.delete { 
    color: #ff5252; 
}
.add-resume-btn {
  width: 100%;
  padding: 12px;
  border: 2px dashed #ddd;
  background: none;
  border-radius: 12px;
  color: #666;
  cursor: pointer;
}
</style>