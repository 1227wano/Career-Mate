<template>
    <section class="resume-banner">
      <div class="banner-content">
        <h2>내 이력서는 얼마나 경쟁력이 있을까?</h2>
        <p>AI 분석을 통해 합격률을 높이는 맞춤형 피드백을 받아보세요.</p>
        <router-link :to="{ name: 'ResumeAnalysisView' }" class="banner-btn">
          이력서 분석 시작하기
        </router-link>
      </div>
      <div class="banner-icon">
        <font-awesome-icon icon="fa-solid fa-file-shield" />
      </div>
    </section>
</template>

<script setup>

</script>

<style scoped>
/* 이력서 배너 스타일 */
.resume-banner {
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
  border-radius: 20px;
  padding: 40px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50px;
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.15);
}
.banner-content h2 { 
    font-size: 22px; 
    margin-bottom: 10px; 
}
.banner-content p { 
    margin-bottom: 25px; 
    opacity: 0.9; 
}
.banner-btn {
  background: white;
  color: #4f46e5;
  padding: 12px 24px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: bold;
  display: inline-block;
}
</style>