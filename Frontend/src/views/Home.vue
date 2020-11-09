<template>
  <div>
    <div id="con">
      <div class="mycontent">
          <h2>VISION SPACE</h2>
          <input placeholder="코드를 입력해주세요" v-model="boardCode" class="roomCodeInput">
          <a @click="toBoard">보드 참가</a>
          <p @click="$router.push({name:'SignupForm'})">계정이 없으신가요? 비전 스페이스는 간편하게 가입하여 이용가능합니다.</p>
      </div>
    </div>
    <!-- <div class="left">
      <v-form>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                outlined
                label="회의 코드 입력"
                prepend-inner-icon="mdi-keyboard"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </div>
    <div>
      <img src="@/assets/mmain.jpg" alt="">
    </div> -->
    <v-container class="lighten-5">
      <!-- Stack the columns on mobile by making one full-width and the other half-width -->
      <!-- Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop -->

      <!-- Columns are always 50% wide, on mobile and desktop -->
      <v-row>
        <v-col cols="6"
          ><h1 class="mt-10 mb-5 introduce">
            스크랩보드 기반 화상회의 <br/> Vision Space
          </h1>
          <h2 class="mb-5 introduce2">
            포스트잇으로 스크랩 보드를 채우면서 서로의 비전을 공유해요.
          </h2>
          <!-- <v-row>
            <v-col cols="6" class="codeinput">
              <v-text-field
                outlined
                label="회의 코드 입력"
                prepend-inner-icon="mdi-keyboard"
                v-model="boardCode"
              ></v-text-field></v-col
            ><v-col cols="3"
              ><v-btn class="mr-4 mt-2" @click="toBoard"> 참가 </v-btn></v-col
            ></v-row
          >
          <hr /> -->
          <!-- <p>계정이 없으신가요? 지금 <router-link to="login" class="router-link">무료로 가입</router-link>하세요.</p> -->
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row>
      <hr class="mt-5">
      <div>
        <p class="center-text">Vision Space 주요 기능</p>
      </div>
      <v-row>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            실시간 아이디어 공유
          </h2>
          <h2 class="mb-5 introduce2">
            화상회의를 하면서. 자신의 아이디어를 포스트잇을 통해 실시간으로 공유할 수 있어요
          </h2>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/conference.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6"
          ><img src="@/assets/chatting.jpg" alt="" class="mt-10 mmain" />
        </v-col>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            채팅을 통한 소통
          </h2>
          <h2 class="mb-5 introduce2">
            마이크를 사용할 수 없는 상황이라면 
            채팅을 통해 대화하세요.
          </h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            화상회의를 제공해주는 Vision Space입니다.
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row>
      
    </v-container>

    <!-- <v-container class="white lighten-5">
      <v-row justify="space-around">
        <v-col sm="5">
          <v-card class="pa-2" outlined tile>
            <v-row justify="space-around">
              <v-btn class="home-btn" rounded color="primary" dark
                ><span class="material-icons" > desktop_windows </span></v-btn
              >
              <v-btn class="home-btn" rounded color="primary" dark>
                <span class="material-icons"> keyboard_voice </span></v-btn
              >
            </v-row>
            <v-row>
              <v-col cols="8" class="codeinput">
                <v-text-field
                  outlined
                  label="회의 코드 입력"
                  prepend-inner-icon="mdi-keyboard"
                ></v-text-field></v-col
              ><v-col cols="4"
                ><v-btn class="mr-4 mt-2" @click="toBoard"> 참가 </v-btn></v-col
              ></v-row
            >
          </v-card>
        </v-col>
        <v-col sm="5">
          <v-card class="mx-auto" max-width="400">
            <v-img
              class="white--text align-end"
              height="200px"
              src="@/assets/cork_board.jpg"
            >
              <v-card-title>
                <div>
                  <h1 class="time">04:29 PM</h1>
                  <p>2020년 11월 3일 화요일</p>
                </div>
              </v-card-title>
            </v-img>
          </v-card>
        </v-col>
      </v-row>
    </v-container> -->
  </div>
</template>

<script>
import SERVER from "@/api/drf";
import axios from "axios";
import cookies from "vue-cookies";

export default {
  data() {
    return {
      boardCode: "",
    };
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
          this.host = res.data.admin_nickname;
          this.roomName = res.data.name;
        })
        .catch(() => {
          this.$router.push({ name: "NoBoardFound" });
          console.log('err');
        });
    },
  },
};
</script>

<style scoped>
#con{
    /* position: absolute; */
    /* top: 5%;
    left: 5%;
    right: 5%;
    bottom: 5%; */
    width: 100%;
    height: 600px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: url('../assets/space.jpg') #151729;
    background-size: 100%;
    box-shadow: 0 15px 30px rgba(0, 0, 0, .5);
    z-index: 10000;
    background-repeat: no-repeat;
    background-size: cover;
}

.left {
  float: left;
}
.introduce {
  font-size: 48px;
  font-weight: 400;
  letter-spacing: -0.5px;
  line-height: 56px;
}
.introduce2 {
  color: #6a6e74;
  font-size: 20px;
  font-weight: 400;
  letter-spacing: initial;
  line-height: 28px;
}
.codeinput {
  /* padding: 0; */
}
.mmain {
  max-width: 100%;
  height: auto;
}
hr {
  border: solid #dadce0;
  border-width: 1px 0 0;
  clear: both;
  height: 0;
  margin-bottom: 19px;
}
.router-link {
  text-decoration: none;
}
.introduce3 {
  font-size: 36px;
  font-weight: 400;
  letter-spacing: -0.25px;
  line-height: 44px;
}
.center-text {
  text-align: center;
}
.time {
  text-align: center;
}
.home-btn {
  width: 80px;
  height: 80px !important;
  padding: 0px !important;
}
.material-icons {
  font-size: 40px !important;
}
#con .mycontent{
    max-width: 800px;
    text-align: center;
}
#con .mycontent h2{
    font-size: 60px;
    color: #fff;
    line-height: 1em;
    margin-bottom: 20px;
}
#con .mycontent h4{
    position: relative;
    font-size: 1.5em;
    margin-bottom: 20px;
    color: #111;
    background: #fff;
    font-weight: 300;
    padding: 10px 20px;
    display: inline-block;
}
#con .mycontent p{
    color: #fff;
    font-size: 1em;
    margin-top: 40px;
    cursor: pointer;
    
}
#con .mycontent p:hover{
  text-decoration: underline;
}
#con .mycontent a{
    position: relative;
    display: block;
    padding: 10px 25px;
    background: #ff0562;
    color: #fff;
    text-decoration: none;
    margin-top: 25px;
    border-radius: 25px;
    border-bottom: 4px solid #d00d56;
    margin-left: auto;
    margin-right: auto;
    width: 180px;
}
.roomCodeInput {
    position: relative;
    font-size: 1.5em;
    margin-bottom: 20px;
    color: #111;
    background: #fff;
    font-weight: 300;
    padding: 10px 20px;
    display: inline-block;
    outline: none;
}
</style>