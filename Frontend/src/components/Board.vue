<template>
  <div style="display:flex;flex-direction:row;height:100%;width:100%;">
    <div style="width:60px;height:100%;background:#eee;">
      <v-tooltip right v-for="(tab,index) in tabs" :key="tab.tab_index">
        <template v-slot:activator="{ on, attrs }">
          <div class="tabBtn" v-bind="attrs" v-on="on" :class="{active:tab.tab_index == activatedTab}" @click="changeTab(tab.tab_index)">
            <div class="tabcolor" :style="{ background:colors[index] }"></div>
            <div class="tab"></div>
            <p style="position:absolute;margin-left:5px;width:100%;">{{ tab.name }}</p>
          </div>
        </template>
        <span>{{ tab.name }}</span>
      </v-tooltip>
      <v-tooltip right v-if="tabs.length < 15">
        <template v-slot:activator="{ on, attrs }">
          <div class="tabBtn" v-bind="attrs" v-on="on" @click="addTab()">
            <div class="tabcolor" :style="{ background: 'white' }">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 20 20">
                <title>
                  add
                </title>
                <path d="M16 9h-5V4H9v5H4v2h5v5h2v-5h5V9z"/>
              </svg>
            </div>
            <div class="tab"></div>
          </div>
        </template>
        <span>Add New Tab</span>
      </v-tooltip>
    </div>
    <div class="cork" style="width:100%;height:100%;">
      <BoardDrawer @addNote="addNote" />
      <!-- <Note v-for="(note) in notes[activatedTab]" :key="note.no"/> -->
      <vue-draggable-resizable v-for="(note, index) in notes" :key="note.no" :w="220" :h="220" :x="note.x" :y="note.y" @dragging="onDrag" :resizable="false" :parent="true" :drag-handle="'.line'">
        <svg @mousedown="activatedNote=index" @mouseup="patchNote(note.note_index)" class="line" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="40" height="40" viewBox="0 0 24 24"><path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" /></svg>
        <div class="content" v-html="note.content">
        </div>
        <!-- {{ note.note_index }} -->
        <div style="position:absolute;left:5px;bottom:5px;">
            <v-icon class="del_btn" @click="delNote(note.note_index)">mdi-trash-can-outline</v-icon>
        </div>
      </vue-draggable-resizable>
    </div>
  </div>
</template>

<script>
import SERVER from '@/api/drf'
import axios from 'axios'
import cookies from 'vue-cookies'
import BoardDrawer from "@/components/BoardDrawer.vue"
// import Note from "@/components/Note"

export default {
    name: 'Board',
    data: () => {
    return {
      activatedTab: 0,
      activatedNote: 0,
      colors: ['rgb(29, 127, 255)','red','#776ea7','pink','#17C37B','#B7E3E4','rgb(29, 127, 255)','red','#EED974','pink','green','#B7E3E4','rgb(29, 127, 255)','red','gray'],
      tabs: [
        {
          no: 0,
          name: 'tab1',
        },
      ],
      notes: [
          // {
          //   no: 0,
          //   width: 0,
          //   height: 0,
          //   x: 400,
          //   y: 300,
          //   content: '<lottie-player src="https://assets6.lottiefiles.com/packages/lf20_R7CRMj.json"  background="transparent"  speed="1"  loop  autoplay></lottie-player>'
          // }, 
          // {
          //   no: 1,
          //   width: 0,
          //   height: 0,
          //   x: 150,
          //   y: 200,
          //   content: "<p>왜안돼</p>",
          // }, 
          // {
          //   no: 2,
          //   width: 0,
          //   height: 0,
          //   x: 750,
          //   y: 200,
          //   // content: '<video id="videoInput" width="200px"></video>',
          // },
      ]
    }
  },
  methods: {
    addVideoStream(video, stream) {
      video.srcObject = stream
      video.addEventListener('loadedmetadata', () =>{
        video.play()
      })
  
    },
    // onResize(x, y, width, height) {
    //   this.x = x
    //   this.y = y
    //   this.width = width
    //   this.height = height
    // },
    onDrag(x, y) {
      // console.log(x,y,this.activatedNote)
      this.notes[this.activatedNote].x = x
      this.notes[this.activatedNote].y = y
    },
    patchNote(noteIdx) {
      let config = {
        headers: {
          Authorization: 'Bearer ' + cookies.get('auth-token')
        }
      };
      let patchingNote = new FormData();
      patchingNote.append('x',this.notes[this.activatedNote].x),
      patchingNote.append('y',this.notes[this.activatedNote].y),
      axios.patch(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.activatedTab +'/note/' + noteIdx + '/', patchingNote, config)
        .then(() => {
          // console.log(res)
          this.fetchNoteList();
        })
        .catch(err => console.log(err.response.data))
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
    addNote(text) {
        let new_note = new FormData();
        new_note.append('width', 220);
        new_note.append('height', 220);
        new_note.append('x', 150);
        new_note.append('y', 150);
        new_note.append('z', 150);
        new_note.append('content','<p>' + text + '</p>');
        new_note.append('type', 1);
        // this.notes[this.activatedTab].push(new_note)
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.post(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.activatedTab + '/note/', new_note, config)
          .then(() => {
            this.fetchNoteList();
          })
          .catch(err => console.log(err.response.data))        
    },
    delNote(no) {
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.delete(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.activatedTab + '/note/' + no + '/', config)
          .then(() => {
            this.fetchNoteList();
          })
          .catch(err => console.log(err.response.data))     
    },
    fetchTabList() {
      let config = {
        headers: {
          Authorization: 'Bearer ' + cookies.get('auth-token')
        }
      };
      axios.get(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/', config)
        .then(res => {
          // console.log(res.data)
          this.tabs = res.data;
        })
        .catch(err => console.log(err.response.data))
    },
    fetchNoteList() {
      let config = {
        headers: {
          Authorization: 'Bearer ' + cookies.get('auth-token')
        }
      };
      axios.get(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.activatedTab +'/note/', config)
        .then(res => {
          // console.log(res.data)
          this.notes = res.data;
        })
        .catch(err => console.log(err.response.data))
    },
    changeTab(tabIdx){
      this.activatedTab = tabIdx;
      this.fetchNoteList();
    }
  },
  components: {
    // Chat
    BoardDrawer,
    // Note,
  },
  created() {
    // setInterval(this.fetchNoteList, 1);
    this.$socket.on('connect', () => {
      this.$socket.emit('join', { code:this.$route.params.code, name:this.$store.state.uid.username})
    })
    this.fetchTabList();
    this.fetchNoteList();
  }
}
</script>

<style scoped>
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
.vdr {
  box-shadow: 0px 34px 36px -26px rgba(0,0,0,.5);
  background: linear-gradient(-55deg, transparent 1.5em, #ffea4b 0) no-repeat;
  border: none;
  font-family: 'Nanum Pen Script', cursive;
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
.content{
  padding: 25px 20px 25px;
  height: 100%;
  width: 100%;
  /* display:flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; */
  /* font-size: 2em; */
  font-size: 20px;
}
.del_btn{
    color:#e9faab;
    cursor: pointer;
}
.del_btn:hover{
    color:#47493e;
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
  transition: .2s ease;
  font-family: 'Nanum Pen Script', cursive;
  font-size: 20px;
  overflow: hidden;
}
.tabBtn p{
  margin: 0;
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
  transition: .2s ease;
}
.tabBtn.active,
.tabBtn:hover{
  width:55px;
}
.tabBtn.active .tab,
.tabBtn:hover .tab{
  width: 20px;
}
</style>