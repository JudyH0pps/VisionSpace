<template>
  <div>
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
      <img src="@/assets/main.png" alt="">
    </div> -->
    <!-- <v-container class="lighten-5">
      <v-row>
        <v-col cols="4"> -->
    <!-- <h1 class="mt-10 mb-5 introduce">
            스크랩보드 기반 프리미엄 화상회의를 제공해주는 Vision Space입니다.
          </h1>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2> -->
    <!-- <v-row>
            <v-col cols="4" class="codeinput">
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
          <hr />
          <p>
            계정이 없으신가요? 지금
            <router-link to="login" class="router-link">무료로 가입</router-link
            >하세요.
          </p>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row> -->
    <!-- <hr class="mt-5">
      <div>
        <p class="center-text">Vision Space 주요 기능</p>
      </div> -->
    <!-- <v-row>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            나중에 완성 거의 다 됐을 때, 기능별로 정리할게요.
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/board.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row> -->
    <!-- <v-row>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            안전하게 사용할 수 있는 Vision Space
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
      </v-row> -->
    <!-- <v-row>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            스크랩보드 기반 프리미엄 화상회의를 제공해주는 Vision Space입니다.
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row> -->
    <!-- <v-row>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            안전하게 사용할 수 있는 Vision Space
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
      </v-row> -->
    <!-- </v-container> -->
    <v-container class="white lighten-5">
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

            <RoomList />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SERVER from '@/api/drf'
import axios from 'axios'
import cookies from 'vue-cookies'

export default {
  data() {
    return {
      boardCode: '',
    }
  },
  methods: {
    toBoard() {
      this.fetchRoomInfo();
    },
    fetchRoomInfo() {
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.get(SERVER.URL + '/api/v1/board/' + this.boardCode + '/', config)
          .then((res) => {
            this.$router.push({ name: 'board', params: {code:this.boardCode}})
            this.host = res.data.admin_nickname;
            this.roomName = res.data.name;
          })
          .catch(err => {
            this.$router.push({ name: 'NoBoardFound' })
            console.log(err.response.data)
            })
    },
  }
};
</script>

<style scoped>
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
</style>