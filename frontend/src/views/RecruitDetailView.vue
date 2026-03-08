<template>
    <div class="job-detail-container">
        <SideBar />
        <div class="job-detail-dashboard">
            <button class="back-btn" @click="$router.go(-1)">
              <font-awesome-icon icon="fa-solid fa-arrow-left"></font-awesome-icon>
            </button>            
            <div class="job-header">
              <h2>{{ jobStore.job.jobs_title }}</h2>
            </div>
            
            <div class="job-content">
              <div class="content-section">
                <h3>근무 조건</h3>
                <p>고용 형태 : {{ jobStore.job.jobs_type }}</p>
              </div>
              
              <div class="content-section">
                <h3>자격 요건</h3>
                <p>학력 : {{ jobStore.job.jobs_edu }}</p>
                <p>경력 : {{ jobStore.job.jobs_exp }}</p>
              </div>
              
              <div class="content-section">
                <h3>접수 방법</h3>
                <p v-if="isAlwaysOpen">
                  상시채용
                </p>
                <p v-else>{{ new Date(jobStore.job.jobs_date).toLocaleDateString('ko-KR') }} 까지</p>
              </div>
              <div class="action-area">
                <a :href="jobStore.job.jobs_link" target="_blank" class="apply-btn">
                  리크루트에서 지원하기
                </a>
              </div>
            </div>
            <RecruitCompanyInfo 
            v-if="jobStore.job"
            :company="jobStore.job.company"/>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useJobStore } from '@/stores/jobs';
import SideBar from '@/components/SideBar.vue';
import RecruitCompanyInfo from '@/components/RecruitCompanyInfo.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const jobStore = useJobStore()
const route = useRoute()

const props = defineProps({
    jobId: Number 
})

onMounted(() => {
    const id = route.params.jobId
    jobStore.getDetailJob(id)
})

const isAlwaysOpen = computed(() => {
  if (!jobStore.job?.jobs_date) return false;
  
  const year = new Date(jobStore.job.jobs_date).getFullYear();
  return year === 9999;
});
</script>

<style scoped>
.job-detail-container{
    display: flex;
    min-height: 100vh;
}
.job-detail-dashboard{
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
/* 헤더 스타일링 */
.job-header {
  border-bottom: 2px solid #eee;
  padding-bottom: 30px;
  margin-bottom: 40px;
}

.job-header h2 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 10px;
}

.company-name {
  font-size: 1.2rem;
  color: #666;
  font-weight: 500;
}

/* 콘텐츠 섹션 */
.content-section {
  margin-bottom: 40px;
}

.content-section h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  border-left: 4px solid #0046ff;
  padding-left: 15px;
}

.content-section p {
  line-height: 1.8;
  color: #444;
  white-space: pre-wrap; /* 줄바꿈 허용 */
}

/* 지원하기 버튼 영역 */
.action-area {
  margin-top: 50px;
  text-align: center;
}

.apply-btn {
  display: inline-block;
  padding: 18px 60px;
  background-color: #0046ff;
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  transition: transform 0.2s, background-color 0.2s;
}

.apply-btn:hover {
  background-color: #0035cc;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 70, 255, 0.3);
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.2rem;
  color: #666;
}
</style>