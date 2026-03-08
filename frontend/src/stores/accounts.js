import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
    const API_URL = import.meta.env.VITE_API_URL
    const token = ref(null)
    const refresh = ref(null)
    const user = ref(null)

    const router = useRouter()

    const signUp = function ({
        username, email, password1, password2, name, birthdate, phone
    }) {
        axios({
            method: 'post',
            url: `${API_URL}/accounts/signup/`,
            data: {
                username, email, password1, password2, name, birthdate, phone
            }
        })
        .then(res => {
            alert('회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.')
            router.push({ name: 'LoginView' })
        })
        .catch(err => console.log(err))
    }
    const login = function ({ username, password }) {
        axios({
            method: 'post',
            url: `${API_URL}/accounts/login/`,
            data: {
                username, password
            }
        })
        .then(res => {
            // console.log('로그인이 완료되었습니다.')
            token.value = res.data.access // 토큰 저장
            refresh.value = res.data.refresh // refresh token 저장 
            user.value = res.data.user
            console.log(user.value)
            router.push({ name: 'MainView' })
        })
        .catch(err => {
            alert('아이디 혹은 비밀번호를 확인해주세요.')
        })
    }
    const refreshAccessToken = function () {
        return axios({
        method: 'post',
        url: `${API_URL}/accounts/token/refresh/`,
        data: {
            refresh: refresh.value,
        }
        })
        .then(res => {
            // console.log(res)
            token.value = res.data.access
            return true
        })
        .catch(err => {
            console.log(err)
            return false
        })
    }
    const logout = function () {
        axios({
        method: 'post',
        url: `${API_URL}/accounts/logout/`,
        headers: {
            Authorization: `Bearer ${token.value}`
        }
        })
        .then(res => {
            token.value = null
            refresh.value = null
            user.value = null
            alert('로그아웃 되었습니다.')
            router.push({ name: 'MainView' })
        })
        .catch(err => console.log(err))
    }
    const isLogin = computed(() => {
        return token.value ? true : false
    })

    return {
        API_URL,
        token,
        refresh,
        user,
        isLogin,
        signUp,
        login,
        refreshAccessToken,
        logout,
    }

})