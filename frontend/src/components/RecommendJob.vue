<template>
    <section class="jobs-section">
      <div class="section-header">
        <h3>추천 채용 공고</h3>
        <router-link to="/jobs" class="view-all">전체보기 〉</router-link>
      </div>

      <div class="jobs-grid">
        <div v-for="i in 4" :key="i" class="job-card">
          <div class="company-logo">LOGO</div>
          <div class="job-info">
            <h4 class="job-title">시니어 프론트엔드 개발자</h4>
            <p class="company-name">테크메이트 컴퍼니</p>
            <div class="tag-group">
              <span class="tag">Vue.js</span>
              <span class="tag">TypeScript</span>
            </div>
          </div>
        </div>
      </div>
    </section>
</template>

<script setup>

</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section-header h3 { 
    font-size: 20px; 
    color: #333; 
}
.view-all { 
    text-decoration: none; 
    color: #666; 
    font-size: 14px; 
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.job-card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #eee;
  display: flex;
  gap: 15px;
  transition: transform 0.2s;
  cursor: pointer;
}
.job-card:hover { 
    transform: translateY(-5px); 
    box-shadow: 0 5px 15px rgba(0,0,0,0.05); 
}

.company-logo {
  width: 50px;
  height: 50px;
  background: #eee;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
}

.job-title { 
    font-weight: bold; 
    margin-bottom: 4px; 
}
.company-name { 
    font-size: 14px; 
    color: #888; 
    margin-bottom: 12px; 
}

.tag-group { 
    display: flex; 
    gap: 8px; 
}
.tag {
  background: #f0f2ff;
  color: #4f46e5;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}
</style>