<template>
    <div class="job-card">
        <div class="job-info">
            <h4 class="job-title">{{ job.jobs_title }}</h4>
            <p class="company-name">{{ job.company.company_name }}</p>
            <div class="tag-group">
                <span class="tag">{{ job.jobs_type }}</span>
                <span class="tag">{{ job.jobs_exp }}</span>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    job: Object,
})
</script>

<style  scoped>
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