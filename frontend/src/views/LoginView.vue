<template>
  <div class="login-container">
    <!-- Left Sidebar -->
    <div class="sidebar">
      <div class="logo">
        <h2>Career Mate</h2>
        <p>커리어 제작 프로젝트</p>
      </div>
      <!-- Stats Preview (Optional) -->
      <div class="sidebar-info">
        <div class="info-item">
          <span class="icon">📊</span>
          <div>
            <h4>248개</h4>
            <p>무료 제공 자료</p>
          </div>
        </div>
        <div class="info-item">
          <span class="icon">⭐</span>
          <div>
            <h4>34개</h4>
            <p>평가자 내용</p>
          </div>
        </div>
        <div class="info-item">
          <span class="icon">✅</span>
          <div>
            <h4>92%</h4>
            <p>사용자 만족도</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="login-box">
        <div class="welcome-section">
          <h1>좋은 아침이에요, 환영합니다 👋</h1>
          <p class="subtitle">로그인하여 커리어 메이트를 시작하세요</p>
        </div>

        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="username">아이디</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="아이디를 입력하세요"
              required
              @input="validateId"
            />
          </div>

          <div class="form-group">
            <label for="password">비밀번호</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="비밀번호를 입력하세요"
              required
              />
            </div>

          <button type="submit" class="login-button">
            로그인
          </button>
        </form>

        <!-- <div class="divider">
          <span>또는</span>
        </div>

        <div class="social-login">
          <button class="social-button google">
            <span>Google로 계속하기</span>
          </button>
          <button class="social-button kakao">
            <span>Kakao로 계속하기</span>
          </button>
        </div> -->

        <div class="signup-link">
          <p>계정이 없으신가요? <a href="/signup">회원가입</a></p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/accounts';

const accountStore = useAccountStore()
const username = ref(null)
const password = ref(null)

const validateId = function (event) {
  const regex = /[^a-zA-Z0-9]/g;
  const filtered = event.target.value.replace(regex, '');
  
  // 1. 변수 업데이트
  username.value = filtered; 
  // 2. 화면(input창) 강제 업데이트 (중요!)
  event.target.value = filtered;
}
  

const login = function () {
  const payload = {
    username: username.value,
    password: password.value,
  }

  accountStore.login(payload)
}
</script>

<style scoped>

.login-container {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #1a2b5f 0%, #0f1937 100%);
  padding: 32px 24px;
  color: white;
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
  gap: 24px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.info-item .icon {
  font-size: 32px;
}

.info-item h4 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.info-item p {
  font-size: 13px;
  opacity: 0.8;
}

/* Main Content */
.main-content {
  flex: 1;
  background: #f5f7fa;
  padding: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.login-box {
  background: white;
  border-radius: 16px;
  padding: 48px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.welcome-section {
  margin-bottom: 32px;
  text-align: center;
}

.welcome-section h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a2b5f;
  margin-bottom: 12px;
}

.subtitle {
  color: #6b7280;
  font-size: 15px;
}

/* Form */
.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
}

.checkbox-container input {
  margin-right: 8px;
  cursor: pointer;
}

.forgot-password {
  font-size: 14px;
  color: #4f46e5;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(79, 70, 229, 0.3);
}

.login-button:active {
  transform: translateY(0);
}

/* Divider */
.divider {
  text-align: center;
  margin: 24px 0;
  position: relative;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #e5e7eb;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background: white;
  padding: 0 16px;
  color: #9ca3af;
  font-size: 14px;
}

/* Social Login */
.social-login {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.social-button {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.social-button:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.social-button.google {
  color: #374151;
}

.social-button.kakao {
  background: #fee500;
  border-color: #fee500;
  color: #000000;
}

.social-button.kakao:hover {
  background: #fdd835;
}

/* Signup Link */
.signup-link {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
}

.signup-link a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
}

.signup-link a:hover {
  text-decoration: underline;
}

/* Stats Preview */
.stats-preview {
  display: flex;
  gap: 16px;
  margin-top: 32px;
  max-width: 480px;
  width: 100%;
}

.stat-card {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 24px;
}

.stat-info h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1a2b5f;
  margin-bottom: 4px;
}

.stat-info p {
  font-size: 12px;
  color: #6b7280;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .main-content {
    padding: 24px;
  }

  .login-box {
    padding: 32px 24px;
  }

  .stats-preview {
    flex-direction: column;
  }
}
</style>