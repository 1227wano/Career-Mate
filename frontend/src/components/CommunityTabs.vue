<template>
  <nav class="community-tabs">
    <button 
      v-for="tab in tabs" 
      :key="tab"
      :class="['tab-btn', { active: modelValue === tab }]"
      @click="$emit('update:modelValue', tab)"
    >
      {{ tab }}
    </button>
  </nav>
</template>

<script setup>
defineProps({
  modelValue: String // 부모의 현재 선택된 탭 값
});

defineEmits(['update:modelValue']);

const tabs = ['전체글', '취업 Q&A', '면접후기', '현직자이야기'];
</script>

<style scoped> 
/* 탭 메뉴 스타일 */
.community-tabs {
  background: white;
  display: flex;
  justify-content: center;
  border-bottom: 1px solid #e1e4e8;
  position: sticky;
  top: 0;
  z-index: 10;
}

.tab-btn {
  padding: 20px 30px;
  border: none;
  background: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  font-weight: 500;
  border-bottom: 3px solid transparent;
}

.tab-btn.active {
  color: #0046ff;
  border-bottom-color: #0046ff;
}
</style>