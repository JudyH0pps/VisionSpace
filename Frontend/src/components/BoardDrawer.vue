<template>
  <div>
    <div class="buttons" style="z-index: 2147483645">
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-on="on"
            v-bind="attrs"
            class="mx-2"
            color="white"
            @click.stop="drawer_method(1)"
          >
            <v-icon v-if="drawer == 1" color="blue">mdi-account-multiple</v-icon
            ><v-icon v-else>mdi-account-multiple</v-icon>
          </v-btn>
        </template>
        <span>Member List</span>
      </v-tooltip>
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-on="on"
            v-bind="attrs"
            class="mx-2"
            color="white"
            @click.stop="drawer_method(2)"
          >
            <v-badge
              color="red"
              :value="newChat"
              :content="String(newChat)"
              offset-x="1"
              offset-y="5"
            >
            <v-icon v-if="drawer == 2" color="blue"
              >mdi-comment-multiple-outline</v-icon
            ><v-icon v-else>mdi-comment-multiple-outline</v-icon>
          </v-badge>
          </v-btn>
          
        </template>
        <span>Chatting</span>
      </v-tooltip>
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-on="on"
            v-bind="attrs"
            class="mx-2"
            color="white"
            @click.stop="drawer_method(3)"
          >
            <v-icon v-if="drawer == 3" color="blue">mdi-note-outline</v-icon
            ><v-icon v-else>mdi-note-outline</v-icon>
          </v-btn>
        </template>
        <span>Add Note</span>
      </v-tooltip>
      <v-tooltip top>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-on="on"
            v-bind="attrs"
            class="mx-2"
            color="white"
            @click.stop="drawer_method(4)"
          >
            <v-icon v-if="drawer == 4" color="blue">mdi-backup-restore</v-icon
            ><v-icon v-else>mdi-backup-restore</v-icon>
          </v-btn>
        </template>
        <span>History</span>
      </v-tooltip>
    </div>
    <div class="drawer" v-show="drawer == 1">
      <div style="height: 100%">
        <WebRtc />
      </div>
    </div>
    <div class="drawer" right absolute v-show="drawer == 2">
      <div class="chat" style="height: 100%">
        <!-- <Chat /> -->
        <div class="msglist" style="height: 85%">
          <Message-List :msgs="datas" class="msg-list"></Message-List>
        </div>
        <textarea
          style="
            box-sizing: border-box;
            height: 10%;
            width: 100%;
            resize: none;
            padding: 5px;
            background: white;
            outline: none;
            font-family: 'HangeulNuri-Bold';
            font-size: 15px;
          "
          placeholder="메시지를 입력하세요"
          v-model="chatMsg"
          @keyup.enter="sendMessage"
          class="roomNameInput"
        ></textarea>
        <!-- <v-text-field
                            v-model="msg"
                            label="chat"
                            placeholder="보낼 메시지를 입력하세요."
                            solo
                            @keyup.13="submitMessageFunc"
                    ></v-text-field> -->
        <div style="background: white">
          <!-- <Message-Form v-on:submitMessage="sendMessage" class="msg-form"></Message-Form> -->
        </div>
      </div>
    </div>
    <div class="drawer" v-show="drawer == 3">
      <div class="btns">
        <button @click="note_type = 1">
          <v-icon>mdi-format-color-text</v-icon>
        </button>
        <button @click="note_type = 2">
          <v-icon>mdi-file-upload-outline</v-icon>
        </button>
        <button @click="note_type = 3"><v-icon>mdi-youtube</v-icon></button>
      </div>
      <p
        style="
          color: white;
          text-align: center;
          font-family: 'HangeulNuri-Bold';
          font-size: 25px;
        "
        v-if="note_type == 1"
      >
        텍스트 입력
      </p>
      <p
        style="
          color: white;
          text-align: center;
          font-family: 'HangeulNuri-Bold';
          font-size: 25px;
        "
        v-if="note_type == 2"
      >
        이미지 업로드
      </p>
      <p
        style="
          color: white;
          text-align: center;
          font-family: 'HangeulNuri-Bold';
          font-size: 25px;
        "
        v-if="note_type == 3"
      >
        Youtube 영상 업로드
      </p>
      <textarea
        v-if="note_type == 1"
        :style="[swatchStyle]"
        class="note"
        type="text-area"
        v-model="new_text"
      ></textarea>
      <!-- <div > -->
      <draganddrop :activatedTab="activatedTab" v-if="note_type == 2" />
      <div
        v-if="note_type == 3"
        :style="[swatchStyle]"
        class="note"
        style="
          display: flex;
          flex-direction: column;
          jusity-content: center;
          align-itmes: center;
        "
      >
        <p
          style="
            text-align: center;
            font-family: 'HangeulNuri-Bold';
            font-size: 13px;
          "
        >
          Youtube영상을 공유하세요
        </p>
        <img
          style="width: 80%; margin: 0 auto 5px"
          src="../assets/youtube1.png"
        />
        <img
          style="width: 100%; margin-bottom: 5px"
          src="../assets/youtube2.png"
        />
        <p
          style="
            text-align: center;
            font-family: 'HangeulNuri-Bold';
            font-size: 13px;
            margin-bottom: 5px;
          "
        >
          Youtube 영상 링크를 입력
        </p>
        <input class="youtubelink" v-model="youtubelink" />
      </div>
      <v-btn
        v-if="note_type == 1 || note_type == 3"
        color="primary"
        style="text-align: center; margin: 25px auto 15px"
        @click="addNote"
        >Add new note</v-btn
      >
      <!-- </div> -->
      <div v-if="note_type != 2">
        <v-color-picker
          class="ma-2 color__pick"
          hide-canvas
          hide-mode-switch
          hide-inputs
          :swatches="swatches"
          show-swatches
          disabled
          v-model="pickColor"
        ></v-color-picker>
      </div>
    </div>
    <div class="drawer" v-show="drawer == 4">
      <History :host="host" :activatedTab="activatedTab"></History>
    </div>
  </div>
</template>

<script>
import WebRtc from "./WebRTC.vue";
import { mapState } from "vuex";
import MessageList from "@/components/Chat/MessageList.vue";
import draganddrop from "./draganddrop.vue";
import History from "./History.vue";

export default {
  name: "BoardDrawer",
  data() {
    return {
      pickColor: "#f8f1ba",
      chatMsg: "",
      datas: [],
      drawer: 2,
      new_text: "",
      note_type: 1,
      background: "",
      swatches: [
        ["#F8BABA"],
        ["#f8f1ba"],
        ["#BFF8BA"],
        ["#BADBF8"],
        ["#DBBAF8"],
      ],
      sticker: "",
      youtubelink: "",
      newChat: 0,
    };
  },
  props: {
    activatedTab: Number,
    host: String,
  },
  computed: {
    ...mapState({
      msgDatas: (state) => state.socket.msgDatas,
    }),
    swatchStyle() {
      const { pickColor } = this;
      return {
        boxshadow: "0px 34px 36px -26px hsla(0, 0%, 0%, 0.5)",
        background: `linear-gradient(transparent 0em, ${pickColor} 0) no-repeat`,
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
      };
    },
  },
  watch: {
    drawer() {
      if (this.drawer == 2) this.newChat = 0;
    }
  },
  created() {
    this.$socket.on("chat", (data) => {
      this.datas.push(data);
      if (this.drawer != 2) {
        this.newChat += 1;
      }
    });
  },
  methods: {
    sendMessage() {
      if (this.chatMsg.length == 1) return;
      let msg = this.chatMsg;

      this.$socket.emit("chat", {
        name: this.$store.state.uid.username,
        message: msg,
      });
      this.chatMsg = "";
    },
    drawer_method(no) {
      if (this.drawer === no) {
        this.drawer = 0;
      } else {
        this.drawer = no;
      }
    },
    addNote() {
      if (
        (this.note_type === 1 && this.new_text === "") ||
        (this.note_type === 3 && this.youtubelink === "")
      ) {
        alert("아무것도 입력하지 않으셨습니다.");
        return;
      }
      let content = "";
      if (this.note_type == 1) {
        content = this.new_text;
      } else if (this.note_type == 3) {
        content = this.youtubelink;
      }
      // alert(content)
      this.$emit(
        "addNote",
        this.note_type,
        content,
        this.pickColor[1] +
          this.pickColor[2] +
          this.pickColor[3] +
          this.pickColor[4] +
          this.pickColor[5] +
          this.pickColor[6]
      );
      this.new_text = "";
      this.youtubelink = "";
    },
  },
  components: {
    WebRtc,
    MessageList,
    draganddrop,
    History,
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.open {
  color: black;
}
.buttons {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.drawer {
  position: fixed;
  right: 0;
  width: 300px;
  display: flex;
  flex-direction: column;
  height: 100%;
  border-left: 1px #eee solid;
  z-index: 2147483646;
  background: rgba(0, 0, 0, 0.5);
  align-content: center;
}
.btns {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 30px auto 15px;
}
.v-icon {
  color: white;
}
.btns button:nth-child(1) {
  border-radius: 10px 0 0 10px;
  border-right: 0;
}
.btns button:last-child {
  border-radius: 0 10px 10px 0;
  border-left: 0;
}
.btns button {
  border: 1px rgb(236, 236, 236) solid;
  width: 80px;
  height: 30px;
  outline: none;
}
.btns button:hover {
  background: rgb(112, 112, 112);
}
.blue {
  color: blue;
}
.color__pick {
  background-color: transparent;
}
.youtubelink {
  height: 40px;
  background: white;
  outline: none;
  font-size: 15px;
  width: 100%;
  border: 1px solid #b6b6b6;
}
.youtubelink:focus {
  outline: 2px solid skyblue;
}
</style>