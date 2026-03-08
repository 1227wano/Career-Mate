<template>
    <div class="post-list-wrapper">
        <div v-if="!accountStore.isLogin" class="login-overlay">
            <div class="overlay-card">
                <div class="lock-icon">🔒</div>
                <h3>멤버십 전용 콘텐츠입니다</h3>
                <p>로그인하고 현직자의 생생한 면접 후기와<br>기업 이야기를 확인해보세요!</p>
                <button @click="goToLogin" class="overlay-login-btn">
                로그인하고 전체보기
                </button>
            </div>
            </div>

            <div :class="['post-list', { 'is-blurred': !accountStore.isLogin }]">
            <div 
            v-for="post in postStore.filteredPosts"
            :key="post.id" 
            @click="goToDetail(post.company, post.id)"
            class="post-card">
                <div class="post-info">
                <span class="post-tag">{{ post.category }}</span>
                <h3 class="post-title">{{ post.post_title }}</h3>
                <p class="post-excerpt">{{ post.post_content }}</p>
                <div class="post-meta">
                    <span>작성자: {{ post.user_info }}</span>
                    <span>{{ new Date(post.created_at).toLocaleString('ko-KR') }}</span>
                </div>
                </div>
                <div class="post-stats">
                <span class="comment-count">💬 {{ post.comments?.length || 0 }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAccountStore } from '@/stores/accounts';
import { usePostStore } from '@/stores/posts';

const accountStore = useAccountStore()
const postStore = usePostStore()
const router = useRouter()
const route = useRoute()

onMounted(() => {
  const companyId = route.params.companyId;
  postStore.getPosts(companyId)
});

const goToLogin = function () {
  router.push({ 
    name: 'LoginView'
  })
}

const goToDetail = function (companyId, postId) {
  router.push({
    name: 'PostDetailView',
    params: {
      companyId: companyId,
      postId: postId,
    }
  })
}

</script>

<style scoped>
/* 게시글 리스트를 감싸는 부모 */
.post-list-wrapper {
  position: relative;
  min-height: 400px;
}

/* 블러 효과 클래스 */
.is-blurred {
  filter: blur(8px);
  pointer-events: none; /* 클릭 방지 */
  user-select: none;    /* 텍스트 선택 방지 */
  opacity: 0.7;
}

/* 중앙 오버레이 레이어 */
.login-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 너무 아래 있지 않게 상단 정렬 후 패딩 */
  padding-top: 100px;
  z-index: 5;
  background: rgba(244, 247, 250, 0.3); /* 배경과 어울리는 투명도 */
}

.overlay-card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  max-width: 400px;
  border: 1px solid #eee;
}

.lock-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.overlay-card h3 {
  font-size: 1.4rem;
  color: #1a1a1a;
  margin-bottom: 15px;
}

.overlay-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
}

.overlay-login-btn {
  background-color: #0046ff;
  color: white;
  border: none;
  padding: 14px 40px;
  border-radius: 10px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.overlay-login-btn:hover {
  background-color: #0035cc;
}


/* 게시글 카드 스타일 */
.post-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.post-tag {
  color: #0046ff;
  font-size: 0.8rem;
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
}

.post-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #1a1a1a;
}

.post-excerpt {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 15px;
}

.post-meta {
  color: #999;
  font-size: 0.85rem;
}

.post-meta span {
  margin-right: 15px;
}

.post-stats {
  font-size: 1rem;
  color: #0046ff;
  font-weight: bold;
}
</style>