<template>
    <div class="main-container">
        <SideBar />
        <div class="main-dashboard">
            <header class="welcome-header">
                <h1>좋은 아침이에요, <strong>김메이트</strong>님! 👋</h1>
                <p>오늘도 당신의 커리어를 위한 새로운 기회들이 기다리고 있어요.</p>
            </header>
            <ResumeBanner />
            <RecommendJob />
        </div>
    </div>
</template>

<script setup>
import RecommendJob from '@/components/RecommendJob.vue';
import ResumeBanner from '@/components/ResumeBanner.vue';
import SideBar from '@/components/SideBar.vue';


</script>

<style scoped>
.main-container{
    display: flex;
    min-height: 100vh;
}
.main-dashboard{
    flex: 1;
    margin-left: 280px;
    padding: 40px;
}

/* 헤더 스타일 */
.welcome-header h1 {
  font-size: 28px;
  color: #1a237e;
  margin-bottom: 8px;
}
.welcome-header p {
  color: #666;
  margin-bottom: 40px;
}

</style>