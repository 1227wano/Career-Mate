import { defineStore } from "pinia";
import { ref } from 'vue';
import axios from "axios";

export const useJobStore = defineStore('job', () => {
    const API_URL = import.meta.env.VITE_API_URL
    const jobs = ref([])
    const job = ref([])

    // 채용정보 리스트 가져오기
    const getJobs = function () {
        axios({
            method: 'get',
            url: `${API_URL}/api/recruit/list/`,
        })
        .then(res => {
            console.log(res.data)
            jobs.value = res.data
        })
    }

    // 채용정보 상세 페이지
    const getDetailJob = function (id) {
        axios({
            method: 'get',
            url: `${API_URL}/api/recruit/${id}/`
        })
        .then(res => {
            console.log(res.data)
            job.value = res.data
        })
    }

    return {
        jobs,
        job,
        getJobs,
        getDetailJob,
    }

})