<template>
  <div style="display: flex; flex-direction: row; height: 100%; width: 100%">
    <div style="display: flex; flex-direction: column; background: #eee">
      <div style="width: 60px; height: 100%">
        <v-tooltip right v-for="(tab, index) in tabs" :key="tab.tab_index">
          <template v-slot:activator="{ on, attrs }">
            <div
              class="tabBtn"
              v-bind="attrs"
              v-on="on"
              :class="{ active: tab.tab_index == activatedTab }"
              @click="changeTab(tab.tab_index)"
            >
              <div
                class="tabcolor"
                :style="{ background: colors[index] }"
              ></div>
              <div class="tab"></div>
              <p style="position: absolute; margin-left: 5px; width: 100%">
                {{ tab.name }}
              </p>
            </div>
          </template>
          <span>{{ tab.name }}</span>
        </v-tooltip>
        <v-tooltip class="asd" right v-if="tabs.length < 15">
          <template v-slot:activator="{ on, attrs }">
            <div class="tabBtn" v-bind="attrs" v-on="on" @click="addTab">
              <div class="tabcolor" :style="{ background: 'white' }">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="30"
                  height="30"
                  viewBox="0 0 20 20"
                >
                  <title>add</title>
                  <path d="M16 9h-5V4H9v5H4v2h5v5h2v-5h5V9z" />
                </svg>
              </div>
              <div class="tab"></div>
            </div>
          </template>
          <span>Add New Tab</span>
        </v-tooltip>
      </div>
      <div
        class="exitBtn"
        style="
          margin-top: auto;
          margin-bottom: 40px;
          text-align: center;
          height: 50px;
        "
        @click="exitdialog = true"
      >
        <v-icon style="font-size: 40px">mdi-exit-run</v-icon>
      </div>
    </div>
    <div class="cork" style="width: 100%; height: 100%">
      <BoardDrawer
        :host="host"
        :history="history"
        :activatedTab="activatedTab"
        :members="members"
        :restore_list="restore_list"
        :restore_prev="restore_prev"
        :restore_next="restore_next"
        @addNote="addNote"
        @backToHistory="backToHistory"
        @refresh="fetchNoteList"
        @tmpTimeSlip="tmpTimeSlip"
        @tmpTimeSlipend="tmpTimeSlipend"
      />
      <!-- <Note v-for="(note) in notes[activatedTab]" :key="note.no"/> -->
      <vue-draggable-resizable
        v-for="(note, index) in notes"
        :key="note.note_index"
        :class="[
          note.color,
          {
            smooth: note.note_index != activatedNote,
            zend: note.note_index == activatedNote,
            zend: isZend == note.note_index,
          },
        ]"
        :w="220"
        :h="220"
        :x="note.x"
        :y="note.y"
        @dragging="onDrag"
        :resizable="false"
        :parent="true"
        :drag-handle="'.line'"
        :style="[
          {
            'z-index': note.z,
          },
          swatchStyle(note.color),
        ]"
      >
        <svg
          @mousedown="
            activatedNote = note.note_index;
            activatedNoteOrder = index;
          "
          @mouseover="isZend = note.note_index"
          @mouseup="patchNote(note.note_index)"
          class="line"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          version="1.1"
          width="40"
          height="40"
          viewBox="0 0 24 24"
        >
          <path
            d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z"
          />
        </svg>
        <!-- {{ note }} -->
        <div
          class="content"
          @mouseover="isZend = note.note_index"
          @mouseout="isZend = -1"
        >
          <div v-if="(note.type_pk.id == 1) | (note.type_index == 1)">
            <p v-for="(line, index) in lines(note.content)" :key="index">
              {{ line }}
            </p>
          </div>
          <NoteIamge v-if="note.type_pk.id == 2" :src="imgSrc(note.content)" />
          <iframe
            v-if="note.type_pk.id == 3"
            style="width: 100%"
            :src="youtubeEmbed(note.content)"
            frameborder="1"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
          <div v-if="note.type_pk.id == 5">
            {{ getVideoUrl(note.content) }}
          </div>
        </div>
        <!-- {{ note.note_index }} -->
        <div
          @mouseover="isZend = note.note_index"
          style="
            position: absolute;
            left: 5px;
            bottom: 5px;
            display: flex;
            flex-direction: row;
          "
        >
          <v-icon
            v-if="note.username == $store.state.uid.username"
            class="del_btn"
            @click="delNote(note.note_index)"
            >mdi-trash-can-outline</v-icon
          >
          <p
            style="color: gray; margin: 5px 15px 0; font-size: 10px"
            v-show="note.note_index == isZend"
          >
            작성자 : {{ note.username }}
          </p>
        </div>
        <!-- {{ note.note_index }} -->
      </vue-draggable-resizable>
    </div>
    <v-dialog
      v-model="exitdialog"
      width="550"
      height="600"
      style="z-index: 20000000000000000"
    >
      <v-card>
        <v-card-title class="headline grey lighten-2">
          보드에서 나가시겠습니까?
        </v-card-title>

        <v-card-text style="font-size: 20px">
          <p>현재 보드를 나가고 나의 보드 목록에서 삭제합니다.</p>
          <p>링크를 공유받으면 다시 접속하실 수 있습니다.</p>
          취소하시려면 바깥 아무곳이나 클릭하세요
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn depressed color="error" @click="exitBoard">
            보드에서 나가기
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import SERVER from "@/api/drf";
import axios from "axios";
import cookies from "vue-cookies";
import moment from "moment";
import BoardDrawer from "@/components/BoardDrawer.vue";
import NoteIamge from "@/components/NoteImage.vue";
import "@/plugins/socketPlugin";

export default {
  name: "Board",
  data: () => {
    return {
      sessionId: null,
      activatedTab: 0,
      activatedNote: -1,
      activatedNoteOrder: -1,
      userLiveNoteIndex: null,
      colors: [
        "#0984e3",
        "red",
        "#20bf6b",
        "#eb3b5a",
        "#fed330",
        "#3498db",
        "#a55eea",
        "#0984e3",
        "#a29bfe",
        "pink",
        "#e17055",
        "#B7E3E4",
        "rgb(29, 127, 255)",
        "red",
        "gray",
      ],
      notes: [],
      tmpnotes: [],
      isZend: -1,
      history: [],
      // pickColor: "292803",
      dialog: true,
      exitdialog: false,
      restore_prev: null,
      restore_next: null,
      restore_list: null,
    };
  },
  props: {
    tabs: Array,
    host: String,
    members: Array,
  },
  watch: {
    // activatedNote() {
    //   alert(this.activatedNote);
    // }
    // isZend() {
    //   alert(this.isZend);
    // }
  },
  methods: {
    swatchStyle(backColor) {
      if (backColor[0] == "#") {
        return {
          // boxshadow: "0px 34px 36px -26px hsla(0, 0%, 0%, 0.5)",
          background: `linear-gradient(-55deg, transparent 1.5em, ${backColor} 0) no-repeat`,
          // border: "none",
          /* font-family: "Nanum Pen Script", cursive; */
        };
      } else {
        return {
          background: `linear-gradient(-55deg, transparent 1.5em, #${backColor} 0) no-repeat`,
        };
      }
    },
    maxZ() {
      let maxz = -1;
      for (let i = 0; i < this.notes.length; i++) {
        let note = this.notes[i];
        if (note.z > maxz) maxz = note.z;
      }
      // alert(maxz);
      return maxz;
    },
    lines(text) {
      // console.log(text.split('\n'));
      return text.split("\n");
    },
    imgSrc(name) {
      // console.log(name)
      return name.split(" ")[0];
    },
    addVideoStream(video, stream) {
      video.srcObject = stream;
      video.addEventListener("loadedmetadata", () => {
        video.play();
      });
    },
    async changeTab(tabIdx) {
      if (this.userLiveNoteIndex) {
        await this.delNote(this.userLiveNoteIndex);
        this.userLiveNoteIndex = null;
      }

      this.activatedTab = tabIdx;
      this.$emit("changeTab", this.tabs[tabIdx].name, tabIdx);
      this.history = [];
      this.fetchNoteList();
    },
    // onResize(x, y, width, height) {
    //   this.x = x

    //   this.y = y
    //   this.width = width
    //   this.height = height
    // },
    onDrag(x, y) {
      // console.log(x,y,this.activatedNote)
      this.notes[this.activatedNoteOrder].x = x;
      this.notes[this.activatedNoteOrder].y = y;
    },
    patchNote(noteIdx) {
      this.activatedNote = -1;
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      let patchingNote = new FormData();
      patchingNote.append("x", this.notes[this.activatedNoteOrder].x),
        patchingNote.append("y", this.notes[this.activatedNoteOrder].y),
        patchingNote.append("z", this.maxZ() + 1);
      axios
        .patch(
          SERVER.URL +
            "/api/v1/board/" +
            this.$route.params.code +
            "/tab/" +
            this.activatedTab +
            "/note/" +
            noteIdx +
            "/",
          patchingNote,
          config
        )
        .then(() => {
          // console.log(res)
          // this.fetchNoteList(); // 왜 쓰는거지?? 일단 history 하면서 뺸 거예요
          this.$socket.emit("moveNote", {
            tab: this.activatedTab,
            note: this.activatedNote,
            x: this.notes[this.activatedNoteOrder].x,
            y: this.notes[this.activatedNoteOrder].y,
          });
        })
        .catch((err) => console.log(err.response.data));
    },
    addTab() {
      this.$emit("addTab");
    },
    addNote(type, text, color) {
      let new_note = new FormData();
      new_note.append("width", 220);
      new_note.append("height", 220);
      new_note.append("x", 150);
      new_note.append("y", 150);
      new_note.append("z", this.maxZ() + 1);
      new_note.append("content", text);
      new_note.append("type", type);
      new_note.append("color", color);
      // alert(text)
      // this.notes[this.activatedTab].push(new_note)
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      axios
        .post(
          SERVER.URL +
            "/api/v1/board/" +
            this.$route.params.code +
            "/tab/" +
            this.activatedTab +
            "/note/",
          new_note,
          config
        )
        .then((res) => {
          console.log(res);
          if (res.data.type_pk.id == 5) {
            this.userLiveNoteIndex = res.data.note_index;
          }
          this.$socket.emit("moveNote", { tab: this.activatedTab });
          this.fetchNoteList();
        })
        .catch((err) => console.log(err.response.data));
    },
    delNote(no) {
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      let target_session_id =
        this.$route.params.code !== undefined
          ? this.$route.params.code
          : this.sessionid;

      axios
        .delete(
          SERVER.URL +
            "/api/v1/board/" +
            target_session_id +
            "/tab/" +
            this.activatedTab +
            "/note/" +
            no +
            "/",
          config
        )
        .then(() => {
          this.$socket.emit("moveNote", { tab: this.activatedTab });
          this.fetchNoteList();
          this.getRestoreList();
        })
        .catch((err) => console.log(err.response.data));
    },
    fetchTabList() {
      this.$emit("fetchTabList");
    },
    fetchNoteList() {
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      axios
        .get(
          SERVER.URL +
            "/api/v1/board/" +
            this.$route.params.code +
            "/tab/" +
            this.activatedTab +
            "/note/",
          config
        )
        .then((res) => {
          // console.log(res.data)
          this.notes = res.data;
          this.tmpnotes = this.notes;
          var his_obj = new Object([res.data, moment().format("LLL")]);
          // console.log(his_obj);
          this.history.push(his_obj);
          // console.log(this.notes)
          // this.$socket.emit("moveNote", { tab: this.activatedTab });
        })
        .catch((err) => console.log(err.response.data));
    },
    backToHistory(data) {
      this.notes = data;
    },
    youtubeEmbed(url) {
      let s = url.split("/");
      return "https://www.youtube.com/embed/" + s[s.length - 1];
    },
    exitBoard() {
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      axios
        .post(
          SERVER.URL + "/api/v1/board/" + this.$route.params.code + "/out/",
          null,
          config
        )
        .then(() => {
          // console.log(res.data)
          this.$router.push({ name: "BoardList" });
        })
        .catch((err) => console.log(err.response));
    },
    getRestoreList() {
      let base_url =
        SERVER.URL +
        "/api/v1/board/" +
        this.$route.params.code +
        "/tab/" +
        this.activatedTab +
        "/history/";

      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };

      axios
        .get(base_url, config)
        .then((res) => {
          this.restore_prev = res.data.previous;
          this.restore_next = res.data.next;
          this.restore_list = res.data.results;
        })
        .catch((err) => console.log(err.response.data));
    },
    tmpTimeSlip(note_list) {
      // console.log(note_list)
      this.tmpnotes = this.notes;
      this.notes = note_list;
    },
    tmpTimeSlipend() {
      this.notes = this.tmpnotes;
    },
    getVideoUrl(target) {
      if (target === this.$store.state.uid.username) {
        return target + ": you";
      } else {
        return target;
      }
    },
  },
  components: {
    BoardDrawer,
    NoteIamge,
  },
  computed: {},
  created() {
    // setInterval(this.fetchNoteList, 1);
    this.sessionid = this.$route.params.code;

    this.$socket.emit("join", {
      code: this.$route.params.code,
      name: this.$store.state.uid.username,
    });

    this.fetchNoteList();
    this.$socket.on("moveNote", () => {
      // console.log(data);
      // if (data.tab == this.activatedTab)
      this.fetchNoteList();
    });
  },
  destroyed() {
    if (this.userLiveNoteIndex) {
      let config = {
        headers: {
          Authorization: "Bearer " + cookies.get("auth-token"),
        },
      };
      let target_session_id =
        this.$route.params.code !== undefined
          ? this.$route.params.code
          : this.sessionid;

      axios.delete(
        SERVER.URL +
          "/api/v1/board/" +
          target_session_id +
          "/tab/" +
          this.activatedTab +
          "/note/" +
          this.userLiveNoteIndex +
          "/",
        config
      );

      this.userLiveNoteIndex = null;
    }

    this.$socket.emit("leave", {
      code: this.$route.params.code,
      name: this.$store.state.uid.username,
    });
  },
};
</script>

<style scoped>
.line {
  /* width: 100%; */
  /* height: 35px; */
  position: absolute;
  fill: rgb(255, 0, 0);
  transform: rotate(10deg) translateX(-50%) translateY(-15px);
  cursor: pointer;
  margin-left: auto;
  left: 50%;
}
.line:hover {
  fill: rgb(252, 76, 76);
}
.vdr {
  box-shadow: -30px 34px 36px -26px rgba(0, 0, 0, 0.5);
  background: linear-gradient(-55deg, transparent 1.5em, #f8f1ba 0) no-repeat;
  border: none;
  /* font-family: 'NEXON Lv1 Gothic OTF'; */
  font-family: "HangeulNuri-Bold";
  /* transition: .1s ease; */
  font-size: 15px;
}
.smooth {
  transition: ease 0.5s;
}
.vdr::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  display: inline-block;
  /* background: linear-gradient(-135deg, transparent 1.5em, rgb(239, 248, 106) 0) no-repeat; */
  border-bottom-left-radius: 5px;
  background-repeat: no-repeat;
  height: 3em;
  width: 1.35em;
  transform: translate(-3px, 178px) rotate(59.5deg);
  background: linear-gradient(
    to left bottom,
    transparent 50%,
    #cec365 0,
    #e9faab 27px,
    #d1b562
  );
  box-shadow: 0 6px 4px -4px #112429;
}
.vdr.BADBF8::after {
  background: linear-gradient(
    to left bottom,
    transparent 50%,
    #66acfd 0,
    #abeefa 27px,
    #6c8eff
  ) !important;
}
.vdr.F8BABA::after {
  background: linear-gradient(
    to left bottom,
    transparent 50%,
    #d47e8c 0,
    #ffcee7 27px,
    #ff8b95
  ) !important;
}
.vdr.BFF8BA::after {
  background: linear-gradient(
    to left bottom,
    transparent 50%,
    #80e467 0,
    #d5f7be 27px,
    #89e066
  ) !important;
}
.vdr.DBBAF8::after {
  background: linear-gradient(
    to left bottom,
    transparent 50%,
    #cf8bee 0,
    #e2bef7 27px,
    #c78fd4
  ) !important;
}
.content {
  padding: 25px 20px 25px;
  height: 100%;
  width: 100%;
  /* display:flex; */
  /* flex-direction: column;
  justify-content: center;
  align-items: center; */
  /* font-size: 2em; */
  font-size: 15px;
}
.content img {
  display: block;
  margin: 0 auto 0;
  object-fit: cover;
  max-height: 100%;
  max-width: 100%;
}
.content p {
  margin: 0;
}
.del_btn {
  color: #c4c4c4;
  cursor: pointer;
}
.del_btn:hover {
  color: #353745;
}
.tabBtn {
  display: flex;
  position: relative;
  flex-direction: row;
  height: 30px;
  width: 40px;
  margin: 10px 0 5px auto;
  box-shadow: 0px 6px 6px -4px #112429;
  cursor: pointer;
  transition: 0.2s ease;
  font-family: "Nanum Pen Script", cursive;
  /* font-family: 'HangeulNuri-Bold'; */
  font-size: 22px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.tabBtn p {
  margin: 0;
  height: 100%;
  overflow: hidden;
}
.tabcolor {
  height: 100%;
  background: rgb(29, 127, 255);
  width: 40px;
}
.tab {
  height: 100%;
  width: 5px;
  background: rgb(255, 255, 255);
  transition: 0.2s ease;
}
.tabBtn.active,
.tabBtn:hover {
  width: 55px;
}
.tabBtn.active .tab,
.tabBtn:hover .tab {
  width: 20px;
}
.zend {
  z-index: 2147483600 !important;
}
iframe {
  border: 0;
}
.v-overlay--active {
  z-index: 2147483646 !important;
  background: transparent;
}
.v-dialog__content {
  z-index: 2147483647 !important;
}
.exitBtn:hover {
  cursor: pointer;
}
.exitBtn:hover .v-icon {
  color: #26a500;
}
</style>