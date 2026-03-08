import { defineStore } from "pinia";
import { ref } from 'vue';
import { useAccountStore } from "./accounts";
import axios from "axios";

export const useProfileStore = defineStore('profile', () => {
    const accountStore = useAccountStore()

    const API_URL = import.meta.env.VITE_API_URL
    const profile = ref([])
    const resumes = ref([])

    // const getProfile = function () {
    //     axios({
    //         method: 'get',
    //         url: `${API_URL}/`
    //     })
    // }

    // 이력서 조회
    const getResume = function () {
        axios({
            method: 'get',
            url: `${API_URL}/api/resumes/`,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`
            },
        })
        .then(res => {
            // console.log(res.data)
            resumes.value = res.data
        })
        .catch(err =>{
            console.log(err)
        })
    }
    // 이력서 등록 
    const postResume = function (file) {
        const formData = new FormData();

        formData.append('resume_file', file)

        axios({
            method: 'post',
            url: `${API_URL}/api/resumes/`,
            data: formData,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`,
                'Content-Type': 'multipart/form-data',
            }
        })
        .then(res => {
            // console.log('업로드 성공:', res.data);
            getResume(); // 목록 새로고침
        })
        .catch(err => {
            console.error('업로드 실패:', err);
        });
    }
    
    // 이력서 삭제
    const deleteResume = function (id) {
        axios({
            method: 'delete',
            url: `${API_URL}/api/resumes/${id}/delete/`,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`,
            }
        })
        .then(() => {
            // 삭제 성공 후 새로고침
            getResume()
        })
    }

    return {
        API_URL,
        resumes,
        getResume,
        postResume,
        deleteResume,
    }
})