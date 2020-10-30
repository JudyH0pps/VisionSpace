const state = {
  uid: ''
 }
 
 const getters = {
   'get_uid': state => state.uid
 }
 
 const mutations = {
   UPDATE_UID(state, ids) {
     state.uid = ids
   }
 }
 
 const actions = {
   update_uid({commit}, data) {
     commit('UPDATE_UID', data);
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