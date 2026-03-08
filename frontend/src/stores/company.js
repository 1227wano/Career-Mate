import { defineStore } from "pinia";
import { ref } from 'vue';
import { useAccountStore } from "./accounts";
import axios from "axios";

export const useCompanyStore = defineStore('company', () => {
    const API_URL = import.meta.env.VITE_API_URL
    const company = ref([])

    const getCompanyInfo = function (id) {
        axios({
            method: 'get',
            url: `${API_URL}/api/companies/${id}/`,
        })
        .then(res => {
            console.log(res.data)
            company.value = res.data
        })
    }
    return {
        API_URL,
        company,
        getCompanyInfo,
    }   
})