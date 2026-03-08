<template>
    <div class="profile-container">
        <SideBar />
        <div class="profile-dashboard">
            <header class="profile-header">
                <h1>마이 프로필</h1>
                <p>계정 정보와 작성하신 이력서를 관리할 수 있습니다.</p>
            </header>
            <ProfileResume />
        </div>
    </div>
</template>

<script setup>
import ProfileResume from '@/components/ProfileResume.vue';
import SideBar from '@/components/SideBar.vue';


</script>

<style scoped>
.profile-container {
    display: flex;
    min-height: 100vh;
}

.profile-dashboard {
    flex: 1;
    margin-left: 280px;
    padding: 40px;
}
.profile-header { 
    margin-bottom: 30px; 
}
.profile-header h1 {
     font-size: 28px; 
     color: #1a237e; 
     margin-bottom: 8px; 
}
.profile-header p {
     color: #666; 
     margin-bottom: 40px;
}
</style>