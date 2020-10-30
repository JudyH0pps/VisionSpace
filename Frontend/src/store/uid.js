const state = {
  uid: '',
  username: ''
 }
 
 const getters = {
   'get_uid': state => state.uid
 }
 
 const mutations = {
   UPDATE_UID(state, ids) {
     state.uid = ids
   },
   UPDATE_USERNAME(state, ids) {
     state.username = ids
   }
 }
 
 const actions = {
   update_uid({commit}, data) {
     commit('UPDATE_UID', data);
   },
   update_username({commit}, data) {
     commit('UPDATE_USERNAME', data)
   }
 }
 
 export default {
   strict: process.env.NODE_ENV !== 'production',
   state: {
     ...state
   },
   getters,
   mutations,
   actions
 }