<template>
    <div class="company-section">
        <div class="section-header">
            <h3>기업정보</h3>
        </div>
        
        <div v-if="company" class="company-card">
            <div class="company-name-side">
            <h4
            @click="$router.push({ name: 'CompanyDetailView', params: { companyId: company.id } })"
            class="clickable-title"
            >{{ company.company_name }}</h4>
            </div>

            <div class="company-info-grid">
            <div class="info-item">
                <span class="label">업종</span>
                <span class="value">-</span>
            </div>
            <div class="info-item">
                <span class="label">주소</span>
                <span class="value">{{ company.company_addr }}</span>
            </div>
            <div class="info-item">
                <span class="label">기업규모</span>
                <span class="value">-</span>
            </div>
            <div class="info-item">
                <span class="label">홈페이지</span>
                <span class="value">
                <a target="_blank">방문하기</a>
                </span>
            </div>
            </div>
        </div>
        
    </div>
</template>

<script setup>
defineProps({
    company: Object,
})

</script>

<style scoped>
/* 회사정보 섹션 */
.company-section {
  margin-top: 60px;
  border-top: 1px solid #eee;
  padding-top: 40px;
}

.section-header h3 {
  font-size: 1.2rem;
  margin-bottom: 20px;
  font-weight: bold;
}

.company-card {
  display: flex;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.clickable-title {
  cursor: pointer;
  color: #1a1a1a;
  transition: color 0.2s;
}

.clickable-title:hover {
  color: #0046ff; /* 마우스 올리면 파란색으로 강조 */
  text-decoration: underline;
}

.company-name-side {
  flex: 0 0 250px;
  padding: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-right: 1px solid #f0f0f0;
}

.company-name-side h4 {
  font-size: 1.1rem;
  font-weight: bold;
  text-align: center;
}

.company-info-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr; /* 2열 구조 */
  padding: 20px;
  gap: 15px;
  background-color: #fafafa;
}

.info-item {
  display: flex;
  align-items: flex-start;
}

.label {
  width: 80px;
  color: #888;
  font-size: 0.9rem;
}

.value {
  flex: 1;
  color: #333;
  font-size: 0.95rem;
  word-break: keep-all;
}

.value a {
  color: #0046ff;
  text-decoration: none;
}
</style>