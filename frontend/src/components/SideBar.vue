<template>
  <!-- Left Sidebar -->
  <div class="sidebar">
    <div class="top-content">
        <div class="logo">
            <h2>Career Mate</h2>
            <p>커리어 제작 프로젝트</p>
        </div>
        <!-- 네비게이터 -->
        <nav class="sidebar-info">
            <ButtonNav 
            v-for="menu in menus"
            :key="menu.id"
            :label="menu.label"
            :icon="menu.icon"
            :to="menu.to"
            :is-active="activeMenu === menu.id"
            />
        </nav>
    </div>
    <!-- 버튼 -->
    <div class="bottom-content">
        <button class="action-btn">
            <font-awesome-icon icon="fa-solid fa-gear" />
            <span>설정</span>
        </button>
        <button v-if="accountStore.isLogin" @click="confirmLogout" class="action-btn logout">
          <font-awesome-icon icon="fa-solid fa-right-from-bracket" />
          <span>로그아웃</span>
        </button>

        <router-link v-else :to="{ name: 'LoginView' }" class="action-btn login-link">
          <font-awesome-icon icon="fa-solid fa-right-to-bracket" />
          <span>로그인</span>
        </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ButtonNav from './ButtonNav.vue';
import { useAccountStore } from '@/stores/accounts';
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()
const router = useRouter()
const activeMenu = ref('home')

const confirmLogout = () => {
  if (confirm('로그아웃 하시겠습니까?')) {
    // Store에 이미 정의된 logout 로직 실행
    accountStore.logout() 
  }
}

const menus = [
  { id: 'home', label: '홈', icon: 'fa-solid fa-home', to: {name: 'MainView'} },
  { id: 'resume', label: '이력서 분석', icon: 'fa-solid fa-file-lines', to: {name: 'ResumeAnalysisView'} },
  { id: 'jobs', label: '채용공고', icon: 'fa-solid fa-briefcase', to: {name: 'RecruitView'} },
  { id: 'profile', label: '프로필', icon: 'fa-solid fa-user', to: {name: 'ProfileView'} },
];

</script>

<style scoped>
/* Sidebar */
.sidebar {
  width: 280px;
  height: 100vh;
  background: linear-gradient(180deg, #1a2b5f 0%, #0f1937 100%);
  padding: 40px 20px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 상단과 하단을 양 끝으로 밀어냄 */
  position: fixed; /* 사이드바 고정 */
  left: 0;
  top: 0;
}

.logo h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.logo p {
  font-size: 1rem;
  opacity: 0.8;
  margin-bottom: 48px;
}

.sidebar-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 하단 버튼 스타일 */
.bottom-content {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
}
.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 1rem;
}
.action-btn:hover {
  color: white;
}
.logout {
  color: #ff8a8a;
}
</style>