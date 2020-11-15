<template>
  <div class="back">
    <v-row class="title">
      <p style="font-family: 'Montserrat', sans-serif;font-size:30px;">My Boards</p>
    </v-row>
    <!-- <v-row>
      <input placeholder="다른 룸의 코드를 공유받았다면 입력해주세요" class="roomCodeInput">
    </v-row> -->
    <div>
    <v-row dense>
        <v-col cols="2">
          <v-card class="pyong" @click="newRoomDialog = true" height="150" width="150" style="display:flex;justify-content:center;align-items:center;border:3px dashed #2f87eb;">
            <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 20 20">
              <title>
                add
              </title>
              <path d="M16 9h-5V4H9v5H4v2h5v5h2v-5h5V9z"/>
            </svg>
          </v-card>
          <v-dialog
          v-model="newRoomDialog"
          width="500"
          >
            <v-card style="background:rgba(255,255,255,0.8);">
              <v-card-title class="headline grey lighten-2" style="background:rgba(255,255,255,0.5);" >
                <p style="margin:0;">새 보드 생성</p>
              </v-card-title>

              <v-card-text class="input__box">
                
              </v-card-text>
              <v-card-text>
                <input placeholder="  생성할 보드의 이름을 입력해주세요" class="roomNameInput" v-model="newRoomName" @keydown.enter="addRoom">
              </v-card-text>
              <!-- <v-divider></v-divider> -->

              <v-card-actions>
                <v-spacer></v-spacer>
                  <v-btn
                  color="primary"
                  @click="addRoom"
                  >
                  CREATE
                  </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
        <v-col v-for="(room, index) in rooms" :key="room.title" cols="2">
          <v-card class="boardEnter pyong" height="150" width="150" @click="moveToBoard(room.session_id)">
              <div class="onBadge" v-if="roomOn[index] == 1">on</div>
              <v-card-title><p>{{ room.name }}</p></v-card-title>
              <p style="position:absolute;color:gray;bottom:0;right:0;margin:15px;font-size:12px;">Host: {{ room.admin_username }}</p>
          </v-card>
        </v-col>
    </v-row>
    </div>
  </div>
</template>

<script>
import SERVER from '@/api/drf'
import axios from 'axios'
import cookies from 'vue-cookies'

export default {
  data: () => ({
    newRoomDialog: false,
    newRoomName: '',
    rooms: [
        // { name: 'Board 1', admin_nickname: 'kong', session_id: 'abced' },
    ],
    boardCode: "",
    roomCodeList: [],
    roomOn: [],
  }),
  watch: {
    newRoomDialog() {
      this.newRoomName = '';
    }
  },
  methods: {
    toBoard() {
      if (this.boardCode == '') {
        alert('코드를 입력해주세요')
        return;
      }
      this.fetchRoomInfo();
    },
    fetchRoomInfo() {
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      axios
        .get(SERVER.URL + "/api/v1/board/" + this.boardCode + "/", config)
        .then((res) => {
          // console.log('@@@@@@@@')
          // console.log(res.data);
          this.$router.push({
            name: "board",
            params: { code: this.boardCode },
          });
          this.host = res.data.admin_username;
          this.roomName = res.data.name;
        })
        .catch(() => {
          // this.$router.push({ name: "NoBoardFound" });
          alert('코드를 다시 확인해 주세요')
          console.log('err');
        });
    },
    moveToBoard(_code) {
      this.$router.push({ name: 'board', params: {code:_code}})

    },
    fetchRoomList() {
      let config = {
        headers: {
          Authorization: 'Bearer ' + cookies.get('auth-token')
        }
      };
      axios.get(SERVER.URL + '/api/v1/board/', config)
        .then(res => {
          // console.log(res.data.results)
          this.rooms = res.data.results;
          for (let i=0; i < this.rooms.length; i++) {
            this.roomCodeList.push(this.rooms[i].session_id);
          }
          // console.log(this.roomCodeList)
          this.$socket.emit("rooms", this.roomCodeList);
        })
        .catch(err => console.log(err.response.data))
    },
    addRoom() {
      if ((this.newRoomName === '') && (this.boardCode === '')) {
        alert('생성할 보드 혹은 코드를 입력해주세요');
        return
      } else if (this.boardCode === '') {
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.post(SERVER.URL + '/api/v1/board/', {name:this.newRoomName} ,config)
          .then(() => {
            this.fetchRoomList();
            this.$socket.emit("rooms", this.roomCodeList);
          })
          .catch(err => console.log(err.response.data))
        // let newRoom = {};
        // newRoom.name = this.newRoomName;
        // newRoom.code = 'random';
        // this.rooms.unshift(newRoom);
        this.newRoomDialog = false;
        } else {
          this.fetchRoomInfo();
        }
    }
  },
  created() {
    this.fetchRoomList();
    this.$socket.on("chkRoomList", () => {
      this.$socket.emit("rooms", this.roomCodeList);
    })
    this.$socket.on("a", (data)=>{
      this.roomOn = data.answer;
    });
  }
};
</script>

<style scoped>
* {
  font-family: 'HangeulNuri-Bold';
}
.back {
  background-image: url('../assets/rooms-back.jpg');
  height: 100%;
  width: 100%;
  background-size: cover;
  background-repeat: no-repeat;
  padding: 50px 150px;
}

.plus {
  width: 80%;
  padding: auto auto;
  margin: 50px;
  margin-left: auto;
  margin-right: auto;
}
.text {
  text-align: center;
  /* background-color: yellow; */
  position: absolute;
  top: 40%;
	left: 40%;
  /* transform: translate( -50%, -50% ); */
}
.roomCodeInput {
  border: 1px solid rgb(0, 0, 0);
  border-radius: 0;
  width: 20%;
  height: 40px;
  outline: none;
  background: rgba(255,255,255,.5);
  margin: 0 auto 0;
}
.roomCodeInput:focus {
  outline:2px solid #7a9fc2;
}
.roomNameInput {
  /* font-family: 'Nanum Pen Script', cursive; */
  /* font-family: 'Nanum Myeongjo', serif; */
  font-family: 'HangeulNuri-Bold';
  background: rgb(247, 245, 245);
  border: 1px solid rgb(184, 184, 184);
  border-radius: 0;
  width: 100%;
  height: 50px;
  font-size: 25px;
  /* display: flex; */
  /* justify-content: center; */
}
.roomNameInput:focus {
  outline:2px solid #7a9fc2;
}
.v-card__title {
  font-size: 15px;
  z-index: 2;
  background: white;
  height: 100%;
}

.v-card {
  border-radius: 0px;
  z-index: 2;
}

.boardEnter::before {
  z-index: 5;
}
.boardEnter::after{
  position: absolute;
  content: '';
  width: 100%;
  height: 100%;
  background:  #2f87eb;
  z-index: -999;
  top: 5px;
  left: 5px;
  transform: rotate(2deg);
  transition: ease .15s;
}
.boardEnter:hover .v-card__title {
  color: #2f87eb;
}
.boardEnter:hover::after{
  transform: rotate(10deg) translateX(5px);
}
.input__box{
  display: flex;
  align-items: center;
  /* justify-content: center; */
  margin: 0;
  padding: 0px 1em !important;
  height: 2em;
}
v-card{
  padding: 0px;
  margin: 0;
}

.v-card:hover svg {
  transform: rotate(720deg);
  transition: 1s;
}

.pyong {
  animation: pyong 1s;
}

@keyframes pyong {	
	0% {
    opacity: 0;
		transform: scale(.5);
	}
  25% {
    transform: scale(1);
  }
	100% {
    opacity: 1;
	}
}
.onBadge {
  position:absolute;
  top:15px;
  left:10px;
  border-radius: 15px !important;
  width: 50px;
  background: rgb(92,179,67);
  background: linear-gradient( rgba(92,179,67,1) 0%, rgba(111,237,197,1) 100%, rgba(92,179,67,1) 100%);
  color: white;
  text-align: center;
  animation: jump 2s infinite;
}

@keyframes jump {	
	0% {
		transform: translateY(-2px);
	}
  25% {
    transform: translateY(2px);
  }
  50% {
    transform: translateY(-2px);
  }
  75% {
    transform: translateY(2px);
  }
	100% {
		transform: translateY(-2px);
	}
}
</style>