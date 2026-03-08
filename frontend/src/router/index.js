import { useAccountStore } from '@/stores/accounts'
import CompanyDetailView from '@/views/CompanyDetailView.vue'
import CompanyPostCreateView from '@/views/CompanyPostCreateView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import PostDetailView from '@/views/PostDetailView.vue'
import PostEditView from '@/views/PostEditView.vue'
import ProfileView from '@/views/ProfileView.vue'
import RecruitDetailView from '@/views/RecruitDetailView.vue'
import RecruitView from '@/views/RecruitView.vue'
import ResumeAnalysisView from '@/views/ResumeAnalysisView.vue'
import SignUpView from '@/views/SignUpView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
    },
    {
      path: '/resume-analysis',
      name: 'ResumeAnalysisView',
      component: ResumeAnalysisView,
    },
    {
      path: '/jobs',
      name: 'RecruitView',
      component: RecruitView,
    },
    {
      path: '/jobs/:jobId',
      name: 'RecruitDetailView',
      component: RecruitDetailView,
      props: true,
    },
    {
      path: '/company/:companyId',
      name: 'CompanyDetailView',
      component: CompanyDetailView,
      props: true,
    },
    {
      path: '/company/:companyId/write',
      name: 'CompanyPostCreateView',
      component: CompanyPostCreateView,
      props: true,
    },
    {
      path: '/company/:companyId/posts/:postId',
      name: 'PostDetailView',
      component: PostDetailView,
      props: true,
    },
    {
      path: '/company/:companyId/posts/:postId/edit',
      name: 'PostEditView',
      component: PostEditView,
      props: true,
    },
    
  ],
})


router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore()

  // 1. 로그인 필요한 페이지 접근 시 (Profile, ResumeAnalysis 등)
  const authRequiredPages = ['ProfileView', 'ResumeAnalysisView']
  
  if (authRequiredPages.includes(to.name) && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    next({ name: 'LoginView' }) // 오타 수정: LogInView -> LoginView
    return 
  }

  // 2. 이미 로그인했는데 로그인/회원가입 페이지로 가려는 경우
  if ((to.name === 'LoginView' || to.name === 'SignUpView') && accountStore.isLogin) {
    next({ name: 'MainView' })
    return
  }

  next() // 위 조건에 해당하지 않으면 정상 이동
})


export default router
