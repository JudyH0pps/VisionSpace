<template>
  <div class="container">
    <p>TimeMachine Debug Phase</p>
    <!-- <div class="btns">
      <v-btn class="mr-2" @click="getPaginatedList('prev')">Prev</v-btn>
      <v-btn @click="getPaginatedList('next')">Next</v-btn>
    </div> -->
    <v-container>
      <v-row>
        <v-list
          v-for="(value, idx) in time_machine_list"
          :key="idx"
          style="background-color: transparent"
        >
          <v-list-item>
            <v-list-group :value="false">
              <template v-slot:activator>
                <v-list-item-title>{{
                  dateSplit(value.created_at)["content"]
                }}</v-list-item-title>
              </template>
              <v-list
                v-for="(underValue, idx) in value.capsule_list"
                :key="idx"
                style="background-color: transparent"
              >
                <div class="note__style">
                  <div
                    v-if="underValue.type_index === 1"
                    :text="underValue.content"
                    :style="swatchStyle(underValue.color)"
                    v-html="underValue.content"
                  ></div>
                  <NoteImage
                    v-if="underValue.type_index === 2"
                    :src="imgSrc(underValue.content)"
                    :style="swatchStyle(underValue.color)"
                  />
                </div>
                <iframe
                  v-if="underValue.type_index === 3"
                  style="width: 100%"
                  :style="swatchStyle(underValue.color)"
                  :src="youtubeEmbed(underValue.content)"
                  frameborder="1"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen
                ></iframe>
              </v-list>
              <v-btn @click="requestTimeSlip(value.tm_index)" class="slipButton"
                >Time Slip</v-btn
              >
            </v-list-group>
          </v-list-item>
        </v-list>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import NoteImage from "@/components/NoteImage.vue";

export default {
  name: "TimeMachine",
  components: {
    NoteImage,
  },
  data() {
    return {};
  },
  props: {
    time_machine_list: Array,
    time_machine_prev: String,
    time_machine_next: String,
  },
  created() {
    console.log("Hello FROM TimeMachine");
    this.$emit("get-list");
  },
  destroyed() {
    console.log("BYE FROM TimeMachine");
  },
  methods: {
    imgSrc(name) {
      // console.log(name)
      return name.split(" ")[0];
    },
    youtubeEmbed(url) {
      let s = url.split("/");
      return "https://www.youtube.com/embed/" + s[s.length - 1];
    },
    dateSplit(vDate) {
      // console.log(vDate)
      const myDays = vDate.split("T"); //
      const myDate = myDays[0].split("-");
      const myYear = myDate[0];
      const myMonth = myDate[1];
      const myDay = myDate[2];
      const myTime = myDays[1].split(".")[0];
      return {
        content: `${myYear}년 ${myMonth}월 ${myDay}일 ${myTime} `,
      };
    },
    requestTimeSlip(target) {
      this.$emit("time-slip-request", target);
    },
    getPaginatedList(target) {
      console.log(target);
      if (target === "prev" && this.time_machine_prev) {
        this.$emit("page-list", this.time_machine_prev);
      } else if (target === "next" && this.time_machine_next) {
        this.$emit("page-list", this.time_machine_next);
      }
    },
    getList() {
      this.$emit("get-list");
    },
    swatchStyle(backColor) {
      if (backColor[0] == "#") {
        return {
          boxshadow: "0px 34px 36px -26px hsla(0, 0%, 0%, 0.5)",
          background: `linear-gradient(transparent 0em, ${backColor} 0) no-repeat`,
          marginLeft: "auto",
          marginRight: "auto",
          height: "220px",
          width: "220px",
          outline: "none",
          resize: "none",
          // padding: "25px 20px 25px",
          border: "none",
          /* font-family: "Nanum Pen Script", cursive; */
          fontFamily: "HangeulNuri-Bold",
          fontSize: "15px",
          marginBottom: "2em",
          alignItems: "center",
          display: "flex",
          flexDirection: "column",
        };
      } else {
        return {
          boxshadow: "0px 34px 36px -26px hsla(0, 0%, 0%, 0.5)",
          background: `linear-gradient(transparent 0em, #${backColor} 0) no-repeat`,
          marginLeft: "auto",
          marginRight: "auto",
          height: "220px",
          width: "220px",
          outline: "none",
          resize: "none",
          padding: "25px 20px 25px",
          border: "none",
          /* font-family: "Nanum Pen Script", cursive; */
          fontFamily: "HangeulNuri-Bold",
          fontSize: "15px",
          marginBottom: "2em",
          alignItems: "center",
          display: "flex",
          flexDirection: "column",
        };
      }
    },
  },
};

// {
//   "id": 40,
//   "capsule_list": [
//     {
//       "username": "asdflkj",
//       "x": 88,
//       "y": 95,
//       "z": 151,
//       "width": 220,
//       "height": 220,
//       "type_index": 2,
//       "content": "https://k3c102.p.ssafy.io/api/v1/images/267507b8db914d6ca419400d7a87421e.jpg [cloud.jpg]",
//       "color": "BADBF8"
//     },
//     {
//       "username": "asdflkj",
//       "x": 365,
//       "y": 90,
//       "z": 153,
//       "width": 220,
//       "height": 220,
//       "type_index": 1,
//       "content": "여행가고 싶다~",
//       "color": "DBBAF8"
//     },
//     {
//       "username": "asdflkj",
//       "x": 687,
//       "y": 82,
//       "z": 155,
//       "width": 220,
//       "height": 220,
//       "type_index": 3,
//       "content": "https://youtu.be/nGCs8HuNrB0",
//       "color": "BFF8BA"
//     }
//   ],
//   "tab_index": 0,
//   "tm_index": 7,
//   "created_at": "2020-11-14T22:26:14.068465+09:00",
//   "board_pk": 4
// }

///////////////////////////////

// { "username": "asdflkj", "x": 88, "y": 95, "z": 151, "width": 220, "height": 220, "type_index": 2, "content": "https://k3c102.p.ssafy.io/api/v1/images/267507b8db914d6ca419400d7a87421e.jpg [cloud.jpg]", "color": "BADBF8" }
// { "username": "asdflkj", "x": 365, "y": 90, "z": 153, "width": 220, "height": 220, "type_index": 1, "content": "여행가고 싶다~", "color": "DBBAF8" }
// { "username": "asdflkj", "x": 687, "y": 82, "z": 155, "width": 220, "height": 220, "type_index": 3, "content": "https://youtu.be/nGCs8HuNrB0", "color": "BFF8BA" }
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: unset !important;
}
.date__button {
  color: white;
  margin-top: 2em;
}
.container {
  overflow-y: auto !important;
  overflow-x: hidden !important;
}
.slipButton {
  align-items: center;
}
.v-list-group__items {
  align-items: center !important;
  display: flex !important;
  flex-direction: column !important;
}
</style>