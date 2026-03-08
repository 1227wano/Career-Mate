<template>
  <div class="resume-container">
    <SideBar />
    
    <div class="resume-dashboard">
      <header class="resume-header">
        <h1>AI 이력서 분석 & 매칭</h1>
        <p>분석할 이력서를 선택하면, AI가 딱 맞는 채용공고를 찾아줍니다.</p>
      </header>

      <div class="resume-content">
        
        <div v-if="isLoading" class="status-msg">
            <div class="spinner-small"></div>
            <p>이력서 목록을 불러오고 있습니다...</p>
        </div>

        <div v-else-if="resumes.length === 0" class="status-msg no-data">
            <div class="icon-placeholder">📂</div>
            <p>😥 불러온 이력서가 없습니다.</p>
            <p class="sub">왼쪽 메뉴의 '내 프로필'에서 이력서를 먼저 등록해주세요.</p>
        </div>

        <div v-else class="resume-grid">
            <div 
              v-for="resume in resumes" 
              :key="resume.id" 
              class="resume-card"
            >
                <div class="card-icon">📄</div>
                <div class="card-info">
                    <h3 :title="resume.original_name">
                        {{ resume.original_name || '제목 없는 이력서' }}
                    </h3>
                    <p>등록일: {{ formatDate(resume.created_at) }}</p>
                </div>
                <button class="btn-analyze" @click="openAnalysisModal(resume)">
                    🚀 AI 분석하기
                </button>
            </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div v-if="isAnalysisLoading" class="analysis-loading">
          <div class="spinner"></div>
          <h2>AI가 이력서를 분석하고 있습니다</h2>
          <p>{{ loadingMessage }}</p>
        </div>

        <div v-else class="analysis-result">
          <div class="result-header">
            <h2>🎉 AI 추천 결과</h2>
            <button class="btn-close-x" @click="closeModal">×</button>
          </div>
          
          <div v-if="recommendations.length > 0" class="jobs-wrapper">
             <div 
              v-for="rec in recommendations" 
              :key="rec.job_id" 
              class="job-card"
              @click="goToJobDetail(rec.job_id)"
            >
              <div class="job-header">
                <span class="company-name">{{ rec.company_name }}</span>
                <span class="ai-badge">Match!</span>
              </div>
              <h3 class="job-title">{{ rec.job_title }}</h3>
              <div class="reason-box">
                <p>{{ rec.match_reason }}</p>
              </div>
            </div>
          </div>
          <div v-else class="no-result">
              <p>추천된 공고가 없습니다.</p>
          </div>
          
          <div class="modal-footer">
            <button class="btn-close" @click="closeModal">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import SideBar from '@/components/SideBar.vue';
import { useAccountStore } from '@/stores/accounts';

const router = useRouter();
const accountStore = useAccountStore();

// 상태 변수
const resumes = ref([]);
const isLoading = ref(true);
const showModal = ref(false);
const isAnalysisLoading = ref(false);
const loadingMessage = ref('');
const selectedResume = ref(null);
const recommendations = ref([]);

// ✅ 이력서 목록 가져오기
const fetchResumes = async () => {
    isLoading.value = true;
    try {
        const token = accountStore.token;
        if (!token) {
            alert("로그인이 필요합니다.");
            router.push('/login');
            return;
        }

        // ⭐ 수정한 주소로 요청 (list/ 없음)
        const res = await axios.get('http://127.0.0.1:8000/api/resumes/', {
            headers: { Authorization: `Bearer ${token}` }
        });

        // 데이터 형식 대응 (Pagination 유무 상관없이)
        if (Array.isArray(res.data)) {
            resumes.value = res.data;
        } else if (res.data.results) {
            resumes.value = res.data.results;
        } else {
            resumes.value = [];
        }

    } catch (error) {
        console.error('❌ 이력서 로딩 실패:', error);
    } finally {
        isLoading.value = false;
    }
};

// 화면 켜질 때 실행
onMounted(() => {
    fetchResumes();
});

// AI 분석 요청
const openAnalysisModal = async (resume) => {
    selectedResume.value = resume;
    showModal.value = true;
    isAnalysisLoading.value = true;
    recommendations.value = [];
    loadingMessage.value = "이력서 내용을 읽는 중...";

    setTimeout(() => { if(isAnalysisLoading.value) loadingMessage.value = "채용공고와 매칭하는 중..."; }, 1500);

    try {
        const token = accountStore.token;
        // 분석 요청 주소 (recommendations 앱)
        const res = await axios.post(`http://127.0.0.1:8000/api/recommendations/recommend/${resume.id}/`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        recommendations.value = res.data;
    } catch (error) {
        alert('분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
        console.error(error);
        showModal.value = false;
    } finally {
        isAnalysisLoading.value = false;
    }
};

const closeModal = () => showModal.value = false;

const goToJobDetail = (jobId) => {
    // 상세 페이지 라우터 이름이 맞는지 확인 필요
    router.push({ name: 'RecruitDetailView', params: { jobId: jobId } });
};

const formatDate = (dateStr) => {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString();
};
</script>

<style scoped>
.resume-container { display: flex; min-height: 100vh; background-color: #f8f9fa; }
.resume-dashboard { flex: 1; margin-left: 280px; padding: 40px; }
.resume-header { margin-bottom: 30px; }
.resume-header h1 { font-size: 26px; color: #1a237e; margin-bottom: 10px; font-weight: 700; }
.resume-header p { color: #666; font-size: 16px; }

/* 리스트 스타일 */
.resume-content { min-height: 300px; }
.status-msg { text-align: center; padding: 60px; color: #666; }
.spinner-small { 
    border: 3px solid #f3f3f3; border-top: 3px solid #1a237e; border-radius: 50%; 
    width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto 15px; 
}
.icon-placeholder { font-size: 50px; margin-bottom: 15px; opacity: 0.5; }
.resume-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }

/* 카드 스타일 */
.resume-card {
    background: white; padding: 25px; border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center;
    transition: all 0.2s; border: 1px solid #eee; display: flex; flex-direction: column;
}
.resume-card:hover { transform: translateY(-5px); border-color: #1a237e; box-shadow: 0 8px 20px rgba(26, 35, 126, 0.1); }
.card-icon { font-size: 40px; margin-bottom: 15px; }
.card-info { flex: 1; }
.card-info h3 { 
    font-size: 18px; margin-bottom: 5px; color: #333; 
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; 
}
.card-info p { font-size: 13px; color: #888; margin-bottom: 20px; }
.btn-analyze {
    width: 100%; padding: 12px; background: #1a237e; color: white;
    border: none; border-radius: 8px; font-weight: bold; cursor: pointer;
    transition: background 0.2s;
}
.btn-analyze:hover { background: #0d1b60; }

/* 모달 스타일 */
.modal-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.6); z-index: 1000;
    display: flex; justify-content: center; align-items: center;
    backdrop-filter: blur(3px);
}
.modal-content {
    background: white; width: 90%; max-width: 900px;
    padding: 30px; border-radius: 16px; min-height: 500px; max-height: 90vh;
    display: flex; flex-direction: column; overflow-y: auto;
}
.analysis-loading { text-align: center; margin-top: 100px; }
.spinner {
    border: 5px solid #f3f3f3; border-top: 5px solid #1a237e;
    border-radius: 50%; width: 60px; height: 60px;
    animation: spin 1s linear infinite; margin: 0 auto 25px;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.btn-close-x { background: none; border: none; font-size: 28px; cursor: pointer; color: #999; }
.jobs-wrapper { display: flex; gap: 15px; flex-wrap: wrap; }
.job-card {
    flex: 1 1 250px; background: #fff; border: 1px solid #ddd; border-radius: 12px;
    padding: 20px; cursor: pointer; transition: all 0.2s;
}
.job-card:hover { border-color: #1a237e; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.job-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
.company-name { font-weight: bold; color: #666; font-size: 14px; }
.ai-badge { background: #e8eaf6; color: #1a237e; font-size: 11px; padding: 4px 8px; border-radius: 20px; font-weight: bold;}
.job-title { font-size: 16px; font-weight: bold; margin-bottom: 12px; color: #333; line-height: 1.4; }
.reason-box { background: #f8f9fa; padding: 12px; border-radius: 8px; font-size: 13px; color: #555; line-height: 1.5; }
.modal-footer { margin-top: auto; padding-top: 20px; text-align: center; }
.btn-close { padding: 10px 40px; background: #eee; color: #333; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
.btn-close:hover { background: #e0e0e0; }
</style>