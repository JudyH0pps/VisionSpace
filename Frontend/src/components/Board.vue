<template>
  <div style="display: flex; flex-direction: row; height: 100%; width: 100%">
    <div style="width: 60px; height: 100%; background: #eee">
      <v-tooltip right v-for="(tab, index) in tabs" :key="tab.tab_index">
        <template v-slot:activator="{ on, attrs }">
          <div
            class="tabBtn"
            v-bind="attrs"
            v-on="on"
            :class="{ active: tab.tab_index == activatedTab }"
            @click="changeTab(tab.tab_index)"
          >
            <div class="tabcolor" :style="{ background: colors[index] }"></div>
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
    <div class="cork" style="width: 100%; height: 100%">
      <BoardDrawer
        :history="history"
        :activatedTab="activatedTab"
        @addNote="addNote"
        @backToHistory="backToHistory"
      />
      <!-- <Note v-for="(note) in notes[activatedTab]" :key="note.no"/> -->
      <vue-draggable-resizable
        v-for="(note, index) in notes"
        :key="note.note_index"
        :class="{
          smooth: note.note_index != activatedNote,
          zend: note.note_index == activatedNote,
          zend: isZend == note.note_index,
        }"
        :w="220"
        :h="220"
        :x="note.x"
        :y="note.y"
        @dragging="onDrag"
        :resizable="false"
        :parent="true"
        :drag-handle="'.line'"
        :style="{ 'z-index': note.z }"
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
          <div v-if="note.type_pk.id == 1">
            <p v-for="(line, index) in lines(note.content)" :key="index">
              {{ line }}
            </p>
          </div>
          <img v-if="note.type_pk.id == 2" :src="imgSrc(note.content)" />
        </div>
        <!-- {{ note.note_index }} -->
        <div @mouseover="isZend = note.note_index" style="position: absolute; left: 5px; bottom: 5px; display:flex; flex-direction:row;">
          <v-icon v-if="note.username == $store.state.uid.username" class="del_btn" @click="delNote(note.note_index)"
            >mdi-trash-can-outline</v-icon
          >
          <p style="color:gray;margin:5px 15px 0;font-size:10px;" v-show="note.note_index == isZend">작성자 : {{ note.username }}</p>
        </div>
        <!-- {{ note.note_index }} -->
      </vue-draggable-resizable>
    </div>
  </div>
</template>

<script>
import SERVER from "@/api/drf";
import axios from "axios";
import cookies from "vue-cookies";
import moment from "moment";
import BoardDrawer from "@/components/BoardDrawer.vue";
import "@/plugins/socketPlugin";

export default {
  name: "Board",
  data: () => {
    return {
      activatedTab: 0,
      activatedNote: -1,
      activatedNoteOrder: -1,
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
      isZend: -1,
      history: [],
    };
  },
  props: {
    tabs: Array,
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
    changeTab(tabIdx) {
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
    addNote(text,color) {
      let new_note = new FormData();
      new_note.append("width", 220);
      new_note.append("height", 220);
      new_note.append("x", 150);
      new_note.append("y", 150);
      new_note.append("z", this.maxZ() + 1);
      new_note.append("content", text);
      new_note.append("type", 1);
      new_note.append("color", color);
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
        .then(() => {
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
      axios
        .delete(
          SERVER.URL +
            "/api/v1/board/" +
            this.$route.params.code +
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
          var his_obj = new Object([res.data, moment().format("LLL")]);
          console.log(his_obj);
          this.history.push(his_obj);
          // console.log(this.notes)
        })
        .catch((err) => console.log(err.response.data));
    },
    backToHistory(data) {
      this.notes = data;
    },
  },
  components: {
    BoardDrawer,
  },
  created() {
    // setInterval(this.fetchNoteList, 1);
    this.$socket.emit("join", {
      code: this.$route.params.code,
      name: this.$store.state.uid.username,
    });
    this.fetchNoteList();
    this.$socket.on("moveNote", (data) => {
      // console.log(data);
      if (data.tab == this.activatedTab) this.fetchNoteList();
    });
  },
  destroyed() {
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
  box-shadow: 0px 34px 36px -26px rgba(0, 0, 0, 0.5);
  background: linear-gradient(-55deg, transparent 1.5em, #fff398 0) no-repeat;
  border: none;
  /* font-family: 'NEXON Lv1 Gothic OTF'; */
  font-family: 'HangeulNuri-Bold';
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
  transform: translate(-3px, 177px) rotate(59.5deg);
  background: linear-gradient(
    to left bottom,
    transparent 50%,
    #cec365 0,
    #e9faab 27px,
    #d1b562
  );
  box-shadow: 0 6px 4px -4px #112429;
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
  display:flex;
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
  z-index: 2147483644 !important;
}
</style>