<template>
  <div class="corkback">
    <Board/>
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
    }
  },
  created() {
    this.joinRoom();
  },
}
</script>

<style scoped>
.corkback {
  /* background-image: url('../assets/cork_board4.png'); */
  height: 100%;
  background-color: #BFD9D7;
  /* width: 100%; */
  /* background-size: 100%; */
  
}
.line{
    /* width: 100%; */
    /* height: 35px; */
    position: absolute;
    fill: rgb(255, 0, 0); 
    transform: rotate(10deg) translateX(-50%) translateY(-15px);
    cursor: pointer;
    margin-left: auto;
    left: 50%;
}
.line:hover{
  fill: rgb(252, 76, 76); 
}
.note {
  box-shadow: 0px 34px 36px -26px hsla(0, 0%, 0%, 0.5);
  background: linear-gradient(transparent 0em, #fff9c8 0) no-repeat;
  margin-left: auto;
  margin-right: auto;
  height:220px;
  width:220px;
  outline: none;
  resize: none;
  padding: 25px 10px 25px;
  border: none;
}
.vdr {
  box-shadow: 0px 34px 36px -26px rgba(0,0,0,.5);
  background: linear-gradient(-55deg, transparent 1.5em, #ffea4b 0) no-repeat;
  border: none;
}
.vdr::after{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  display: inline-block;
  /* background: linear-gradient(-135deg, transparent 1.5em, rgb(239, 248, 106) 0) no-repeat; */
  border-bottom-left-radius: 5px;
  background-repeat: no-repeat;
  height: 3em;
  width: 1.35em;
  transform: translate(-3px, 175px) rotate(59.5deg);
  background: linear-gradient(to left bottom, transparent 50%, #cec365 0, #e9faab 27px, #d1b562);
  box-shadow: 0 6px 4px -4px #112429;
}
.content {
  padding: 25px 10px 25px;
  height: 100%;
  width: 100%;
  display:flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 2em;
}
.v-btn {
  position: absolute;
  top: 50%;
  right: 0px;
  translate: linear;
}
.open {
  transform: translateX(-255px) rotate(180deg);
}
</style>