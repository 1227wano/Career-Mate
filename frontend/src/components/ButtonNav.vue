<template>
    <router-link :to="to" class="info-item" v-slot="{ isActive }">
        <div class="nav-menu" :class="{ active: isActive }">
            <font-awesome-icon :icon="icon" class="icon"/>
            <span class="label">{{ label }}</span>
        </div>
    </router-link>
</template>

<script setup>
defineProps({
    label: String,
    icon: String,
    to: Object,
})
</script>

<style scoped>
.info-item{
    text-decoration: none;
    display: block;
}
.nav-menu {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #fff;
  border-radius: 12px;
  transition: all 0.2ms ease;
  padding: 12px 16px;
}
.label {
  font-size: 1.1rem;
}
.nav-menu .icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}
/* 마우스 올렸을 때 */
.nav-menu:hover:not(.active) {
  background-color: rgba(255, 255, 255, 0.1);
}
.nav-menu.active {
  background-color: #ffffff;
  color: #1a237e;
  font-weight: bold;
}
</style>