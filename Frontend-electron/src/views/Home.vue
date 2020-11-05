<template>
  <div class="top">
    <v-container class="white lighten-5 container">
      <v-row class="main my-auto" justify="space-around">
        <v-col sm="5" class="col btn_list">
          <v-card class="pa-2 left-card" outlined tile>
            <v-row justify="space-around">
              <v-col class="col">
                <v-btn class="home-btn" color="primary" rounded dark
                  ><span class="material-icons"> voice_chat </span></v-btn
                >
                <p class="btn-text">새 회의</p>
              </v-col>
              <v-col class="col">
                <v-btn class="home-btn" color="blue-grey" rounded dark>
                  <span class="material-icons"> today </span></v-btn
                >
                <p class="btn-text">예약</p>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="8" class="codeinput">
                <v-text-field
                  outlined
                  label="회의 코드 입력"
                  prepend-inner-icon="mdi-keyboard"
                  v-model="boardCode"
                  style="
                    width: 219.99px;
                    height: 110px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                  "
                ></v-text-field></v-col
              ><v-col cols="4"
                ><v-btn @click="toBoard"> 참가 </v-btn></v-col
              ></v-row
            >
          </v-card>
        </v-col>
        <v-col sm="5" class="col">
          <v-card class="mx-auto" max-width="400">
            <v-img
              class="white--text align-end"
              height="200px"
              src="@/assets/main-space.jpg"
            >
              <v-card-title>
                <div>
                  <h1 class="time">04:29 PM</h1>
                  <p>2020년 11월 3일 화요일</p>
                </div>
              </v-card-title>
            </v-img>
            <div v-if="isLoggedIn">
              <RoomList />
            </div>
            <div v-else>
              <p class="mt-5" style="text-align:center;">로그인이 필요한 서비스입니다.</p>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SERVER from "@/api/drf";
import axios from "axios";
import cookies from "vue-cookies";
import RoomList from "@/components/RoomList.vue";
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      boardCode: "",
    };
  },
  components: {
    RoomList,
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
  methods: {
    toBoard() {
      if (!this.boardCode) {
        alert("회의 코드를 입력해주세요.");
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
          this.$router.push({
            name: "board",
            params: { code: this.boardCode },
          });
          this.host = res.data.admin_nickname;
          this.roomName = res.data.name;
        })
        .catch((err) => {
          this.$router.push({ name: "NoBoardFound" });
          console.log(err.response.data);
        });
    },
  },
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
  margin-top: 28px;
  display: grid;
  justify-content: center;
  align-items: center;
  vertical-align: middle;
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
  /* color:#6a6e74; */
  display: grid;
  width: 80px;
  height: 80px !important;
  padding: 0px !important;
  justify-content: center !important;
  align-content: center;
}
.material-icons {
  font-size: 40px !important;
  /* justify-content: center !important;
  align-content: center; */
}
.col {
  justify-content: center !important;
  display: grid;
  align-content: center;
}
.btn-text {
  margin-top: 10px;
  text-align: center;
  font-size: 14px;
}
.left-card {
  border: none;
  /* width: 322.4px; */
  /* height: 288.8px; */
}
.container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  vertical-align: middle;
}
.main {
  height: 100%;
}
.top {
  height: 100%;
}
</style>