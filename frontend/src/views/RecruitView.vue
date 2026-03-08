<template>
  <div class="recruit-container">
    <SideBar />

    <div class="recruit-dashboard">
      <header class="welcome-header">
        <h1><strong>김메이트</strong>님을 위한 채용공고</h1>
        <p>오늘도 당신의 커리어를 위한 새로운 기회들이 기다리고 있어요.</p>
      </header>

      <div v-if="isLoading" class="loading-state">
        <p>최신 채용 정보를 불러오는 중입니다...</p>
      </div>

      <div v-else class="jobs-grid">
        <RecruitItem 
          v-for="job in recruits" 
          :key="job.id" 
          :job="job"
          @click="$router.push({ name: 'RecruitDetailView', params: { jobId: job.id } })"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import RecruitItem from '@/components/RecruitItem.vue'
import SideBar from '@/components/SideBar.vue'
// import { useRouter } from 'vue-router' // 라우터 사용 시 필요

// const router = useRouter()
const recruits = ref([])
const isLoading = ref(false)

// 1. DB 업데이트 및 데이터 가져오기 함수
const fetchRecruits = async () => {
  isLoading.value = true
  try {
    // (1) RSS 데이터 최신화 요청 (Django API)
    // 데이터 양에 따라 시간이 소요될 수 있습니다.
    await axios.get('http://127.0.0.1:8000/api/recruit/update/')
    
    // (2) 업데이트 완료 후 DB 목록 재조회
    const response = await axios.get('http://127.0.0.1:8000/api/recruit/')
    recruits.value = response.data
    
  } catch (error) {
    console.error('채용공고 업데이트 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 2. 페이지 로드 시 실행
onMounted(() => {
  fetchRecruits()
})
</script>

<style scoped>
.recruit-container {
  display: flex;
  min-height: 100vh;
}

.recruit-dashboard {
  flex: 1;
  margin-left: 280px; /* SideBar 너비만큼 여백 */
  padding: 40px;
  background-color: #f8f9fa; /* 배경색 살짝 추가 (선택사항) */
}

/* 헤더 스타일 */
.welcome-header h1 {
  font-size: 28px;
  color: #1a237e;
  margin-bottom: 8px;
}

.welcome-header p {
  color: #666;
  margin-bottom: 40px;
}

/* 로딩 상태 스타일 */
.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}

/* 그리드 레이아웃 */
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>