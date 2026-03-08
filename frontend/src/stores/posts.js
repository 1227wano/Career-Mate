import { defineStore } from "pinia";
import { computed, ref } from 'vue';
import axios from "axios";
import { useRouter } from "vue-router";
import { useAccountStore } from "./accounts";

export const usePostStore = defineStore('post', () => {
    const API_URL = import.meta.env.VITE_API_URL
    const accountStore = useAccountStore()
    const router = useRouter()
    const posts = ref([])
    const post = ref([])
    const currentTab = ref('전체글')

    // 여러개의 게시글을 가져옴 
    const getPosts = function (companyId) {
        posts.value = []

        axios({
            method: 'get',
            url: `${API_URL}/api/companies/${companyId}/posts/`,
        })
        .then(res => {
            posts.value = res.data
        })
        .catch(err => {
            console.error('게시글 로드 실패:', err)
            posts.value = [] // 에러 발생 시에도 비워주는 것이 안전합니다.
        })
    }
    
    // 단일 게시글 가져옴
    const getPost = function (companyId, postId) {
        axios({
            method: 'get',
            url: `${API_URL}/api/companies/${companyId}/posts/${postId}/`,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`
            },
        })
        .then((res) => {
            console.log(res.data)
            post.value = res.data
        })
    }

    // 게시글 생성 
    const createPost = function (postData) {
        axios({
            method: 'post',
            url: `${API_URL}/api/companies/${postData.company}/write/`,
            data: postData,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`
            },
        })
        .then(
            router.push({ name: 'CompanyDetailView', params: { companyId: postData.company}})
        )
    
    }
    // 게시글 수정
    const editPost = function (editData, companyId, postId) {
        axios({
            method: 'put',
            url: `${API_URL}/api/companies/${companyId}/posts/${postId}/edit/`,
            data: editData,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`
            },
        })
        .then(
            router.push({ name: 'PostDetailView', params: { companyId, postId } })
        )
    }
    
    // 게시글 삭제
    const deletePost = function (companyId, postId) {
        axios({
            method: 'delete',
            url: `${API_URL}/api/companies/${companyId}/posts/${postId}/`,
            headers: {
                'Authorization': `Bearer ${accountStore.token}`
            },
        })
        .then(() => {

            alert('게시글이 삭제되었습니다.')
            router.push({ name: 'CompanyDetailView', params: { companyId, postId } })
        })
    }

    // 댓글 등록
    const createComment = function (commentContent, companyId, postId) {
        axios({
            method: 'post',
            url: `${API_URL}/api/companies/${companyId}/posts/${postId}/comment/`,
            data: {
                comment_content: commentContent
            },
            headers: {
                'Authorization': `Bearer ${accountStore.token}`
            },
        })
        .then(res => {
            post.value.comments.push(res.data)
        })
    }
    // 댓글 삭제
    const deleteComment = function (companyId, postId, commentId) {
        axios({
            method: 'delete',
            url: `${API_URL}/api/companies/${companyId}/posts/${postId}/comment/${commentId}/`,
            headers: {
                Authorization: `Bearer ${accountStore.token}`
            }
        })
        .then(() => {
            post.value.comments = post.value.comments.filter(c => c.id !== commentId)
            alert('댓글이 삭제되었습니다.')
        })
    }
    // 댓글 수정
    const editComment = function (companyId, postId, commentId, commentContent) {
        axios({
            method: 'put',
            url: `${API_URL}/api/companies/${companyId}/posts/${postId}/comment/${commentId}/`,
            data: { 
                comment_content: commentContent 
            },
            headers: { 
                Authorization: `Bearer ${accountStore.token}` 
            }
        })
        .then((res) => {
            // 화면의 댓글 목록에서 수정된 댓글만 찾아 교체
            const index = post.value.comments.findIndex(c => c.id === commentId)
            if (index !== -1) {
                post.value.comments[index] = res.data
            }
            alert('댓글이 수정되었습니다.')
        })
    }

    // 게시글 필터링
    // 1. 현재 선택된 카테고리에 맞는 게시글들만 필터링
    const filteredPosts = computed(() => {
        if (currentTab.value === '전체글') {
            return posts.value
        }
        return posts.value.filter(post => post.category === currentTab.value)
    })
    // 전체 게시글 수 계산
    const totalPostCount = computed(() => filteredPosts.value.length)

    // 본인 게시글 & 댓글 여부 확인 로직
    const isPostAuth = computed(() => {
        console.log('게시글 작성자 ID:', post.value?.user)
        console.log('내 ID:', accountStore.user?.pk)
        return post.value?.user === accountStore.user?.pk
    })

    const isCommentAuth = computed(() => {
        return (commentUserId) => {
            return accountStore.user && accountStore.user?.pk === commentUserId
        }
    })

    return {
        API_URL,
        currentTab,
        post,
        posts,
        filteredPosts,
        totalPostCount,
        isPostAuth,
        isCommentAuth,
        getPost,
        getPosts,
        createPost,
        editPost,
        deletePost,
        createComment,
        deleteComment,
        editComment,
    }
})