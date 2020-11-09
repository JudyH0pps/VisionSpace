import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import VueDraggableResizable from 'vue-draggable-resizable'
import 'vue-draggable-resizable/dist/VueDraggableResizable.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

import Directives from './plugins/directives'
import VueMaterial from 'vue-material'

import './plugins/socketPlugin';

// import VuePeerJS from 'vue-peerjs';
// import Peer from 'peerjs';
// Vue.use(VuePeerJS, new Peer({}));


// Vue.prototype.$socket = socket;
Vue.use(Directives)
Vue.use(VueMaterial)
Vue.component('vue-draggable-resizable', VueDraggableResizable)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
