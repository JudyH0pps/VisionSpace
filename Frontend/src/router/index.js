import Vue from 'vue'
import VueRouter from 'vue-router'
// import DashBoard from '../views/DashBoard.vue'
import Home from '../views/Home.vue'
// import store from '../store/index'
import cookies from 'vue-cookies'
// user
import SignupForm from '../views/user/SignupForm.vue'
import RoomList from '../components/RoomList.vue'
import ElectronEX from '../views/ElectronEX'
Vue.use(VueRouter)

const requireAuth = () => (to, from, next) => {
  if (cookies.isKey('auth-token')) {
    return next();
  }
  next('/loginplz')
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/board/:code',
    name: 'board',
    component: () => import(/* webpackChunkName: "about" */ '../views/Space.vue'),
    beforeEnter: requireAuth()
  },
  {
    path: '/boardlist',
    name: 'BoardList',
    component: RoomList,
    beforeEnter: requireAuth()
  },
  {
    path: '/login',
    name: 'SignupForm',
    component: SignupForm
  },
  // {
  //   path: '/chat-room/:username',
  //   name : 'ChatRoom',
  //   component: ChatRoom,
  // },
  {
    path: '/loginplz',
    name: 'loginplz',
    component: () => import('@/views/LoginPlz.vue')
  },
  {
    path: '/ex',
    name: 'ElectronEX',
    component: ElectronEX
  },
  {
    path: '/dad',
    name: 'drag',
    component: () => import('@/components/draganddrop.vue')
  },
  {
    path: '/google-login',
    name: 'Google-Login-Handler',
    component: () => import('@/views/user/GoogleLoginHandler.vue')
  },
  {
    path: '/noBoardFound',
    name: 'NoBoardFound',
    component: () => import('@/views/noBoardFound.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
