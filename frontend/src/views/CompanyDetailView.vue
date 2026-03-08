<template>
  <div class="company-community-container">
    <SideBar />
    <div class="company-community-dashboard" v-if="companyStore.company">
      <header class="company-banner">
        <div class="banner-content">
          <!-- <span class="category-tag">{{ companyStore.company.company_industry }}</span> -->
          <h1>{{ companyStore.company.company_name }}</h1>
          <p class="company-meta">
            <i class="location-icon">📍</i> {{ companyStore.company.company_addr }}
          </p>
        </div>
      </header>

      <CommunityTabs v-model="postStore.currentTab"/>

      <section class="post-section">
        <div class="post-header">
          <span class="post-count">총 <strong>{{ postStore.totalPostCount }}</strong>개의 글</span>
          <button class="write-btn" @click="goToWrite">글쓰기</button>
        </div>
        <PostItem />
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCompanyStore } from '@/stores/company';
import { useAccountStore } from '@/stores/accounts';
import { usePostStore } from '@/stores/posts';
import SideBar from '@/components/SideBar.vue';
import PostItem from '@/components/PostItem.vue';
import CommunityTabs from '@/components/CommunityTabs.vue';

const router = useRouter();
const route = useRoute();
const company = ref(null);
const posts = ref([]); // 나중에 백엔드에서 가져올 게시글들
const accountStore = useAccountStore()
const companyStore = useCompanyStore()
const postStore = usePostStore()

onMounted(() => {
  const id = route.params.companyId;
  companyStore.getCompanyInfo(id)
});

// 2. 현재 선택된 탭 상태 관리
const currentTab = ref('전체글');

const goToWrite = () => {
  router.push({ 
    name: 'CompanyPostCreateView', 
    params: { companyId: companyStore.company.id } 
  });
};

</script>

<style scoped>
.company-community-container{
    display: flex;
    min-height: 100vh;
}
.company-community-dashboard{
    flex: 1;
    margin-left: 280px;
    padding: 40px;
}

/* 상단 기업 배너 */
.company-banner {
  background: linear-gradient(135deg, #0046ff 0%, #002db3 100%);
  color: white;
  padding: 60px 40px;
}

.banner-content {
  max-width: 1000px;
  margin: 0 auto;
}

.category-tag {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  margin-bottom: 15px;
  display: inline-block;
}

.company-banner h1 {
  font-size: 2.2rem;
  margin: 10px 0;
}

.company-meta {
  opacity: 0.9;
  font-size: 1rem;
}

/* 게시판 영역 */
.post-section {
  max-width: 1000px;
  margin: 30px auto;
  padding: 0 20px;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.write-btn {
  background-color: #0046ff;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
</style>