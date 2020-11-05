<template>
  <div class="corkback">
    <div class="boardName">
      <div>{{ roomName }}</div> -
      <v-tooltip v-if="!tabMod" bottom>
        <template v-slot:activator="{ on, attrs }">
          <div @click="tabMod=true" v-on="on" v-bind="attrs">{{ tabName }}<v-icon>mdi-clipboard-edit-outline</v-icon></div>
        </template>
        <span>탭 이름 수정</span>
      </v-tooltip>
      <textarea v-if="tabMod" v-model="tabName" @keypress.enter="patchTabName"></textarea>
    </div>
    <Board :tabs="tabs" @addTab="addTab" @changeTab="changeTab"/>
  </div>
</template>

<script>
import SERVER from '@/api/drf'
import axios from 'axios'
import cookies from 'vue-cookies'
// import Chat from "../components/Chat.vue";
import Board from '@/components/Board.vue';

export default {
  data: () => {
    return {
      roomName: '',
      host: '',
      tabName: '',
      tabIdx: 0,
      tabMod: false,
      tabs: [{name:'asd'}],
    }
  },
  components: {
    Board
  },
  methods: {
    joinRoom() {
      let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.post(SERVER.URL + '/api/v1/board/' + this.$route.params.code +'/join/', null, config)
          .then(() => {
            // console.log(res.data);
          })
          .catch(err => console.log(err.response.data))
    },
    fetchRoomInfo() {
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.get(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/', config)
          .then((res) => {
            // console.log(res.data);
            this.host = res.data.admin_nickname;
            this.roomName = res.data.name;
          })
          .catch(err => {
            this.$router.push({ name: 'NoBoardFound' })
            console.log(err.response.data)
          })
    },
    patchTabName() {
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.put(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.tabIdx + '/', { name : this.tabName }, config)
          .then(() => {
            // console.log(res.data);
            this.tabMod = false;
            this.fetchTabList(false);
          })
          .catch(err => console.log(err.response.data))

    },
    changeTab(tabName, tabIdx) {
      this.tabName = tabName;
      this.tabIdx = tabIdx;
      this.tabMod = false;
    },
    addTab() {
      let config = {
        headers: {
          Authorization: 'Bearer ' + cookies.get('auth-token')
        }
      };
      axios.post(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/',{name:'tab' + (this.tabs.length + 1)},config)
        .then(() => {
          // console.log(res.data)
          this.fetchTabList();
        })
        .catch(err => console.log(err.response.data))
    },
    fetchTabList(f) {
      let config = {
        headers: {
          Authorization: 'Bearer ' + cookies.get('auth-token')
        }
      };
      axios.get(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/', config)
        .then(res => {
          // console.log(res.data)
          this.tabs = res.data;
          if (f) {
            this.tabName = this.tabs[0].name;
          }
        })
        .catch(err => console.log(err.response.data))
    },
    
  },
  created() {
    this.fetchRoomInfo();
    this.joinRoom();
    this.fetchTabList(true);
  },
}
</script>

<style scoped>
.corkback {
  background-image: url('../assets/cork_board6.jpg');
  height: 100%;
  /* background-color: #BFD9D7; */
  /* width: 100%; */
  background-size: cover;
  
  
}
.boardName {
  position: fixed;
  top: 2px;
  left: 30%;
  z-index: 2147483647;
  font-family: 'Nanum Pen Script', cursive;
  font-size: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  min-width: 300px;
}
.boardName div,
.boardName textarea {
  /* border: 1px solid rgb(216, 216, 216); */
  border-radius: 20px;
  min-width: 150px;
  text-align: center;
  height: 30px;
  margin: 0 10px 0;
}
.boardName div:hover,
.boardName textarea:hover {
  background: #eee;
  resize: none;
  outline: none;
}
</style>