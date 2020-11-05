import Vue from 'vue'
import Vuex from 'vuex'
import socket from './modules/socket';
import cookies from 'vue-cookies'
import axios from 'axios'

import router from '@/router' //index.js 까지 인데. 
// js import 할 때 뺄 수 있고 index라는 이름이 상징적이라서 폴더 이름까지만 쓰면 안써도됨
import SERVER from '@/api/drf'

import createPersistedState from "vuex-persistedstate";
import uid from './uid.js';

// const modules = {
//   uid,
// }
const plugins = [
  createPersistedState({
    paths: [
      'uid'
    ]
  })
]
Vue.use(Vuex)
const debug = process.env.NODE_ENV !== 'production';


export default new Vuex.Store({
  plugins,
  state: {
    authToken: cookies.get('auth-token')
  },
  getters: {
    isLoggedIn: state => !!state.authToken,
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.authToken = token
      cookies.set('auth-token', token)
    },
  },
  actions: {
    postAuthData({ commit, dispatch }, info) {
      axios.post(SERVER.URL + info.location, info.data)
        .then(res => {
          console.log(res)
          commit('SET_TOKEN', res.data.access_token)
          dispatch("update_uid", res.data.user.pk)
          dispatch("update_username", res.data.user.username)
          router.push({ name: 'BoardList' })
        })
        .catch(err => {
          let text = '';
          for (let a in err.response.data){
            text += a + err.response.data[a] + '\n';
          }
          alert(text);
          console.log(err.response.data);
        })
    },
    signup({ dispatch }, signupData) {
      console.log(signupData)
      const info = {
        data: signupData,
        location: SERVER.ROUTES.signup
      }
      dispatch('postAuthData', info)
    },
    login({ dispatch }, loginData) {
      const info = {
        data: loginData,
        location: SERVER.ROUTES.login
      }
      dispatch('postAuthData', info)
    },
    logout() {
      cookies.remove('auth-token');
      router.push({ name: 'Home' })
      window.location.reload();
    },
    google_login({ dispatch }, google_loginData) {
      const info = {
        data: google_loginData,
        location: SERVER.ROUTES.google_auth
      }
      dispatch('postAuthData', info)
    }
  },
  modules: {
    uid,
    socket,
  },
  strict: debug,
})
