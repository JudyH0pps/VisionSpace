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
      <v-tooltip class="asd" right v-if="tabs.length < 15">
        <template v-slot:activator="{ on, attrs }">
          <div class="tabBtn" v-bind="attrs" v-on="on" @click="addTab">
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
      <BoardDrawer :activatedTab="activatedTab" @addNote="addNote" />
      <!-- <Note v-for="(note) in notes[activatedTab]" :key="note.no"/> -->
      <vue-draggable-resizable v-for="(note, index) in notes" :key="note.note_index" :w="220" :h="220" :x="note.x" :y="note.y" @dragging="onDrag" :resizable="false" :parent="true" :drag-handle="'.line'">
        <svg @mousedown="activatedNote=index" @mouseup="patchNote(note.note_index)" class="line" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="40" height="40" viewBox="0 0 24 24"><path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" /></svg>
        <div class="content">
          <p v-if="note.type_pk.id == 1" v-text="note.content"></p>
          <v-img v-if="note.type_pk.id == 2" :src="imgSrc(note.content)"></v-img>
        </div>
        <!-- {{ note.note_index }} -->
        <div style="position:absolute;left:5px;bottom:5px;">
            <v-icon class="del_btn" @click="delNote(note.note_index)">mdi-trash-can-outline</v-icon>
        </div>
        <!-- {{ note.note_index }} -->
      </vue-draggable-resizable>
    </div>
  </div>
</template>

<script>
import SERVER from '@/api/drf'
import axios from 'axios'
import cookies from 'vue-cookies'
import BoardDrawer from "@/components/BoardDrawer.vue"
// import '@/plugins/socketPlugin';

export default {
    name: 'Board',
    data: () => {
    return {
      activatedTab: 0,
      activatedNote: 0,
      colors: ['rgb(29, 127, 255)','red','#776ea7','pink','#17C37B','#B7E3E4','rgb(29, 127, 255)','red','#EED974','pink','green','#B7E3E4','rgb(29, 127, 255)','red','gray'],
      notes: [
      ]
    }
  },
  props: {
    tabs: Array,
  },

  methods: {
    imgSrc(name) {
      // console.log(name)
      return name.split(' ')[1]
    },
    addVideoStream(video, stream) {
      video.srcObject = stream
      video.addEventListener('loadedmetadata', () =>{
        video.play()
      })
  
    },
    changeTab(tabIdx){
      this.activatedTab = tabIdx;
      this.$emit('changeTab', this.tabs[tabIdx].name, tabIdx)
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
          this.$socket.emit('moveNote', {
            tab: this.activatedTab,
            note: this.activatedNote,
            x: this.notes[this.activatedNote].x,
            y: this.notes[this.activatedNote].y,
          });
        })
        .catch(err => console.log(err.response.data))
    },
    addTab() {
      this.$emit('addTab');
    },
    addNote(text) {
        let new_note = new FormData();
        new_note.append('width', 220);
        new_note.append('height', 220);
        new_note.append('x', 150);
        new_note.append('y', 150);
        new_note.append('z', 150);
        new_note.append('content', text);
        new_note.append('type', 1);
        // this.notes[this.activatedTab].push(new_note)
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.post(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.activatedTab + '/note/', new_note, config)
          .then(() => {
            this.$socket.emit('moveNote', {tab: this.activatedTab})
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
            this.$socket.emit('moveNote', {tab: this.activatedTab})
            this.fetchNoteList();
          })
          .catch(err => console.log(err.response.data))     
    },
    fetchTabList() {
      this.$emit('fetchTabList');
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
          // console.log(this.notes)
        })
        .catch(err => console.log(err.response.data))
    },
  },
  components: {
    // Chat
    BoardDrawer,
    // Note,
  },
  created() {
    // setInterval(this.fetchNoteList, 1);
    this.$socket.emit('join', { code:this.$route.params.code, name:this.$store.state.uid.username})
    this.fetchNoteList();
    this.$socket.on('moveNote', (data) => {
      // console.log(data);
      if (data.tab == this.activatedTab) this.fetchNoteList();
    })
  },
  destroyed() {
    this.$socket.emit('leave',{ code:this.$route.params.code, name:this.$store.state.uid.username});
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
  background: linear-gradient(-55deg, transparent 1.5em, #f8f1ba 0) no-repeat;
  border: none;
  font-family: 'Nanum Pen Script', cursive;
  /* transition: .1s ease; */
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
    color:#353745;
    cursor: pointer;
}
.del_btn:hover{
    color:#353745;
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