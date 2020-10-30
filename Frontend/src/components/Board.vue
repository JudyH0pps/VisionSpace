<template>
  <div style="display:flex;flex-direction:row;height:100%;width:100%;">
    <div style="width:60px;height:100%;background:#eee;">
      <v-tooltip right v-for="tab in tabs" :key="tab.no">
        <template v-slot:activator="{ on, attrs }">
          <div class="tabBtn" v-bind="attrs" v-on="on" :class="{active:tab.no == activatedTab}" @click="activatedTab=tab.no">
            <div class="tabcolor" :style="{ background: tab.color }"></div>
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
      <vue-draggable-resizable v-for="(note,index) in notes[activatedTab]" :key="note.no" :w="220" :h="220" :x="note.x" :y="note.y" @dragging="onDrag" :resizable="false" :parent="true" :drag-handle="'.line'">
        <svg class="line" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="40" height="40" viewBox="0 0 24 24"><path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" /></svg>
        <div class="content" v-html="note.content">
        </div>
        <div style="position:absolute;left:5px;bottom:5px;">
            <v-icon class="del_btn" @click="del_note(index)">mdi-trash-can-outline</v-icon>
        </div>
      </vue-draggable-resizable>
    </div>
  </div>
</template>

<script>
import BoardDrawer from "@/components/BoardDrawer.vue"

export default {
    name: 'Board',
    data: () => {
    return {
      activatedTab: 0,
      tabs: [
        {
          no: 0,
          name: 'tab1',
          color: 'rgb(29, 127, 255)',
        },
        {
          no: 1,
          name: 'aasdadssdas',
          color: 'red',
        }
      ],
      notes: [
        [
          {
            no: 0,
            width: 0,
            height: 0,
            x: 400,
            y: 300,
            content: '<lottie-player src="https://assets6.lottiefiles.com/packages/lf20_R7CRMj.json"  background="transparent"  speed="1"  loop  autoplay></lottie-player>'
          }, 
          {
            no: 1,
            width: 0,
            height: 0,
            x: 150,
            y: 200,
            content: "<p>왜안돼</p>",
          }, 
          {
            no: 2,
            width: 0,
            height: 0,
            x: 750,
            y: 200,
            // content: '<video id="videoInput" width="200px"></video>',
          },
        ],
        []
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
    onResize(x, y, width, height) {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
    },
    onDrag(x, y) {
      this.x = x
      this.y = y
    },
    addTab() {
      let newTab = {};
      newTab.no = this.tabs.length;
      newTab.name = 'tab' + (this.tabs.length + 1);
      newTab.color = 'pink';
      this.tabs.push(newTab);
      this.notes.push([]);
    },
    addNote(text) {
        let new_note = {};
        new_note.no = 400;
        new_note.width = 0;
        new_note.height = 0;
        new_note.x = 0;
        new_note.y = 0;
        new_note.content = '<p>' + text + '</p>'
        this.notes[this.activatedTab].push(new_note)
    },
    delNote(no) {
        this.notes.splice(no,1);
    }
  },
  components: {
    // Chat
    BoardDrawer,
  },
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