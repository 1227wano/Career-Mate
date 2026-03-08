<template>
  <div class="signup-container">
    <!-- Left Sidebar -->
    <div class="sidebar">
      <div class="logo">
        <h2>Career Mate</h2>
        <p>커리어 매칭 플랫폼</p>
      </div>
      
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
      <div class="signup-box">
        <div class="welcome-section">
          <h1>환영합니다! 👋</h1>
          <p class="subtitle">Career Mate와 함께 커리어를 시작하세요</p>
        </div>

        <!-- Progress Steps -->
        <div class="progress-steps">
          <div 
            class="step" 
            :class="{ active: currentStep >= 1, completed: currentStep > 1 }"
          >
            <div class="step-number">1</div>
            <span>기본 정보</span>
          </div>
          <div class="step-line" :class="{ active: currentStep > 1 }"></div>
          <div 
            class="step" 
            :class="{ active: currentStep >= 2, completed: currentStep > 2 }"
          >
            <div class="step-number">2</div>
            <span>추가 정보</span>
          </div>
          <div class="step-line" :class="{ active: currentStep > 2 }"></div>
          <div 
            class="step" 
            :class="{ active: currentStep >= 3 }"
          >
            <div class="step-number">3</div>
            <span>완료</span>
          </div>
        </div>

        <!-- Step 1: Basic Information -->
        <form v-if="currentStep === 1" @submit.prevent="nextStep" class="signup-form">
          <div class="form-row">
            <div class="form-group">
              <label for="name">이름 *</label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                placeholder="이름을 입력하세요"
                required
              />
            </div>
          </div>
          <div class="form-group">
            <label for="username">아이디 *</label>
            <input 
              id="username"
              v-model="formData.username" 
              type="text" 
              placeholder="아이디를 입력하세요"
              required 
              @input="validateId"/>
          </div>
          <div class="form-group">
            <label for="email">이메일 *</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="example@email.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">비밀번호 *</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              placeholder="8자 이상 입력하세요"
              required
              @input="validatePassword"
            />
            <div class="password-strength">
              <div class="strength-bar" :class="passwordStrength"></div>
            </div>
            <span class="hint">영문, 숫자, 특수문자 포함 8자 이상</span>
          </div>

          <div class="form-group">
            <label for="confirmPassword">비밀번호 확인 *</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              placeholder="비밀번호를 다시 입력하세요"
              required
            />
            <span v-if="passwordMismatch" class="error-message">비밀번호가 일치하지 않습니다</span>
          </div>

          <button type="submit" class="next-button">
            다음 단계
          </button>
        </form>

        <!-- Step 2: Additional Information -->
        <form v-if="currentStep === 2" @submit.prevent="nextStep" class="signup-form">
          <div class="form-group">
            <label for="phone">전화번호</label>
            <input
              id="phone"
              v-model="formData.phone"
              type="tel"
              placeholder="숫자만 입력하세요"
            />
          </div>

          <div class="form-group">
            <label for="birthdate">생년월일</label>
            <input
              id="birthdate"
              v-model="formData.birthdate"
              type="date"
            />
          </div>


          <div class="form-actions">
            <button type="button" @click="prevStep" class="back-button">
              이전
            </button>
            <button type="submit" class="next-button">
              다음 단계
            </button>
          </div>
        </form>

        <!-- Step 3: Terms and Completion -->
        <form v-if="currentStep === 3" @submit.prevent="handleSignup" class="signup-form">
          <div class="terms-section">
            <h3>약관 동의</h3>
            
            <label class="checkbox-item all-agree">
              <input type="checkbox" v-model="allAgree" @change="toggleAllAgree" />
              <span class="bold">전체 동의</span>
            </label>

            <div class="divider-line"></div>

            <label class="checkbox-item">
              <input type="checkbox" v-model="formData.terms.service" required />
              <span>서비스 이용약관 동의 (필수)</span>
              <a href="#" class="view-link">보기</a>
            </label>

            <label class="checkbox-item">
              <input type="checkbox" v-model="formData.terms.privacy" required />
              <span>개인정보 처리방침 동의 (필수)</span>
              <a href="#" class="view-link">보기</a>
            </label>

            <label class="checkbox-item">
              <input type="checkbox" v-model="formData.terms.marketing" />
              <span>마케팅 정보 수신 동의 (선택)</span>
              <a href="#" class="view-link">보기</a>
            </label>

            <label class="checkbox-item">
              <input type="checkbox" v-model="formData.terms.age" required />
              <span>만 14세 이상입니다 (필수)</span>
            </label>
          </div>

          <div class="form-actions">
            <button type="button" @click="prevStep" class="back-button">
              이전
            </button>
            <button type="submit" class="signup-button" :disabled="!canSubmit">
              회원가입 완료
            </button>
          </div>
        </form>

        <!-- Social Signup (Only on Step 1) -->
        <!-- <div v-if="currentStep === 1" class="social-section">
          <div class="divider">
            <span>또는</span>
          </div>

          <div class="social-signup">
            <button type="button" class="social-button google">
              <span>Google로 시작하기</span>
            </button>
            <button type="button" class="social-button kakao">
              <span>Kakao로 시작하기</span>
            </button>
          </div>
        </div> -->

        <div class="login-link">
          <p>이미 계정이 있으신가요? <a href="/login">로그인</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, watch, ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts';

  const accountStore = useAccountStore()
  
  // 1. 상태 관리
  const currentStep = ref(1)
  const allAgree = ref(false)
  const passwordStrength = ref('')
  const idValid = ref('')
  
  const formData = ref({
    username: '',
    email: '',
    name: '',
    password: '',
    confirmPassword: '',
    birthdate: '',
    phone: '',
    terms: {
      service: false,
      privacy: false,
      marketing: false,
      age: false
    }
  })

  // 2. 유효성 검사
  const passwordMismatch = computed(() => {
    return formData.value.confirmPassword && 
          formData.value.password !== formData.value.confirmPassword
  })

  const canSubmit = computed(() => {
    const { service, privacy, age } = formData.value.terms
    return service && privacy && age
  })

  // 3. 로직 
  const validatePassword = function () {
    const pw = formData.value.password
    const hasLetter = /[a-zA-Z]/.test(pw)
    const hasNumber = /[0-9]/.test(pw)
    const hasSpecial = /[!@#$%^&*]/.test(pw)
    const isLongEnough = pw.length >= 8
  
    if (!isLongEnough) {
      passwordStrength.value = 'weak'
    } else if (hasLetter && hasNumber && hasSpecial) {
      passwordStrength.value = 'strong'
    } else if ((hasLetter && hasNumber) || (hasLetter && hasSpecial) || (hasNumber && hasSpecial)) {
      passwordStrength.value = 'medium'
    } else {
      passwordStrength.value = 'weak'
    }
  }

  const validateId = function (event) {
    const regex = /[^a-zA-Z0-9]/g; // 영문과 숫자만 허용
    const filterValue = event.target.value.replace(regex, '');

    formData.value.username = filterValue;
    event.target.value = filterValue;
  }

  const toggleAllAgree = function () {
    const val = allAgree.value
    formData.value.terms.service = val
    formData.value.terms.privacy = val
    formData.value.terms.marketing = val
    formData.value.terms.age = val
  }

  const nextStep = function () {
    if (currentStep.value === 1) {
      if (passwordMismatch.value) return alert('비밀번호가 일치하지 않습니다.')
      if (passwordStrength.value === 'weak') return alert('더 강력한 비밀번호를 사용해주세요.') 
    }
    currentStep.value++
  }

  const prevStep = function() {
    this.currentStep--
  }

  // 4. 최종 회원가입 제출 (store 호출)
  const handleSignup = function() {
    if (!canSubmit.value) {
      alert('필수 약관에 동의해주세요.')
      return
    }

    console.log('회원가입 데이터:', formData)
    
    // payload 구성하기
    const payload = {
      username: formData.value.username,
      email: formData.value.email,
      password1: formData.value.password,
      password2: formData.value.confirmPassword,
      name: formData.value.name,
      birthdate: formData.value.birthdate,
      phone: formData.value.phone,
    }
    accountStore.signUp(payload)
  }

  // 5. watcher (전체 동의 체크박스 상태 동기화)
  watch(() => formData.value.terms, (newTerms) => {
    allAgree.value = newTerms.service && newTerms.privacy && newTerms.marketing && newTerms.age
  }, {deep: true})
</script>

<style scoped>
.signup-container {
  display: flex;
  min-height: 100vh;
  font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.signup-box {
  background: white;
  border-radius: 16px;
  padding: 48px;
  width: 100%;
  max-width: 600px;
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

/* Progress Steps */
.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
  padding: 0 20px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e5e7eb;
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s;
}

.step.active .step-number {
  background: #4f46e5;
  color: white;
}

.step.completed .step-number {
  background: #10b981;
  color: white;
}

.step span {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 500;
}

.step.active span {
  color: #4f46e5;
}

.step-line {
  width: 80px;
  height: 2px;
  background: #e5e7eb;
  margin: 0 8px;
  margin-bottom: 24px;
  transition: all 0.3s;
}

.step-line.active {
  background: #4f46e5;
}

/* Form */
.signup-form {
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  /* grid-template-columns: 1fr 1fr; */
  gap: 16px;
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

.form-group input,
.form-group select {
  width: 90%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.error-message {
  display: block;
  margin-top: 6px;
  font-size: 13px;
  color: #ef4444;
}

.hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #9ca3af;
}

/* Password Strength */
.password-strength {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.strength-bar {
  height: 100%;
  width: 0;
  transition: all 0.3s;
}

.strength-bar.weak {
  width: 33%;
  background: #ef4444;
}

.strength-bar.medium {
  width: 66%;
  background: #f59e0b;
}

.strength-bar.strong {
  width: 100%;
  background: #10b981;
}

/* Checkbox Group */
.checkbox-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  position: relative;
}

.checkbox-item input {
  margin-right: 8px;
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.checkbox-item.all-agree {
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 16px;
}

.checkbox-item .bold {
  font-weight: 600;
  color: #1a2b5f;
}

.view-link {
  margin-left: auto;
  font-size: 13px;
  color: #6b7280;
  text-decoration: underline;
}

/* Terms Section */
.terms-section {
  margin-bottom: 24px;
}

.terms-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a2b5f;
  margin-bottom: 20px;
}

.terms-section .checkbox-item {
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.divider-line {
  height: 1px;
  background: #e5e7eb;
  margin: 16px 0;
}

/* Buttons */
.next-button,
.signup-button {
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

.next-button:hover,
.signup-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(79, 70, 229, 0.3);
}

.signup-button:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  transform: none;
}

.back-button {
  padding: 14px 32px;
  background: white;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.back-button:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.form-actions {
  display: flex;
  gap: 12px;
}

.form-actions .next-button,
.form-actions .signup-button {
  flex: 1;
}

/* Social Section
.social-section {
  margin-top: 24px;
}

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

.social-signup {
  display: flex;
  flex-direction: column;
  gap: 12px;
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
} */

/* Login Link */
.login-link {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
  margin-top: 24px;
}

.login-link a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .main-content {
    padding: 24px;
  }

  .signup-box {
    padding: 32px 24px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .checkbox-group {
    grid-template-columns: 1fr;
  }

  .progress-steps {
    padding: 0;
  }

  .step span {
    font-size: 10px;
  }

  .step-line {
    width: 40px;
  }
}
</style>