<template>
    <div>
        <div class="buttons" style="z-index:2147483647;">
            <v-btn class="mx-2" color="white" @click.stop="drawer_method(1)">
                <v-icon>mdi-account-multiple</v-icon>Member List
            </v-btn>
            <v-btn class="mx-2" color="white" @click.stop="drawer_method(2)">
                <v-icon>mdi-comment-multiple-outline</v-icon>Chatting
            </v-btn>
            <v-btn class="mx-2" color="white" @click.stop="drawer_method(3)">
                <v-icon>mdi-note-outline</v-icon>New note
            </v-btn>
        </div>
        <div class="drawer" v-show="drawer == 1">
        <template>
            <v-container fluid>
                <WebRtc />
                <!-- <v-row dense>
                    <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
                    <v-card>
                        <v-img src="../assets/person-icon.png" class="white--text align-end" height="100px">
                        </v-img>
                    </v-card>
                    </v-col>
                </v-row> -->
                </v-container>
                <!-- <button >추가하기</button> -->
            </template>
        </div>
        <div class="drawer" right absolute v-show="drawer == 2">
                <div class="chat" style="height:100%;">
                    <!-- <Chat /> -->
                    <div style="height:85%;background:skyblue;">
                        <Message-List :msgs="msgDatas" class="msg-list"></Message-List>
                    </div>
                    <textarea style="box-sizing:border-box;height:10%;width:100%;resize:none;padding:5px;" placeholder="메시지를 입력하세요" v-model="msg" @keyup.enter="sendMessage" class="roomNameInput"></textarea>
                    <!-- <v-text-field
                            v-model="msg"
                            label="chat"
                            placeholder="보낼 메시지를 입력하세요."
                            solo
                            @keyup.13="submitMessageFunc"
                    ></v-text-field> -->
                    <div style="background:white;">
                        <!-- <Message-Form v-on:submitMessage="sendMessage" class="msg-form"></Message-Form> -->
                        
                    </div>
                </div>
        </div>
        <div class="drawer" v-show="drawer == 3">
                    <textarea class="note" type="text-area" v-model="new_text"></textarea>
                    <v-btn color='primary' style="text-align:center;margin: 25px auto 15px;" @click="addNote">Add new note</v-btn>
        </div>
    </div>
</template>

<script>
// import Chat from "./Chat.vue";
import WebRtc from './webRtc.vue'
import {mapMutations, mapState} from 'vuex';
import MessageList from '@/components/Chat/MessageList.vue'
// import MessageForm from '@/components/Chat/MessageForm.vue'
import Constant from '@/Constant'

export default {
    name: 'BoardDrawer',
    data() {
        return {
            msg: '',
            datas:[],
            drawer: 0,
            new_text: '',
        }
    },
    computed: {
        ...mapState({
            'msgDatas': state => state.socket.msgDatas,
        }),
    },
    created() {
        this.$socket.on('chat', (data) => {
            console.log(data)
            this.pushMsgData(data);
            this.datas.push(data);
        });
    },
    methods: {
        ...mapMutations({
            'pushMsgData': Constant.PUSH_MSG_DATA,
        }),
        sendMessage() {
            // console.log(this.$store.state.uid.username)
            if (this.msg == '') {
                alert('내용이없어'); 
                return;
            }
            let msg = this.msg;
            this.pushMsgData({
                from: {
                    name: this.$store.state.uid.username,
                },
                msg,
            });
            this.$sendMessage({
                name: this.$store.state.uid.username,
                msg,
            });
            this.msg = '';
        },
        drawer_method(no) {
            // alert(no)
            if (this.drawer === no){
                this.drawer = 0;
            }
            else {
                this.drawer = no;
            }
        },
        addNote() {
            if (this.new_text === '') {
                alert('Type any text!');
                return;
            }
            this.$emit('addNote', this.new_text);
            this.new_text = '';
        }
    },
    components: {
        // Chat,
        WebRtc,
        MessageList,
        // MessageForm,
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap');
.open {
  color: black;
}
.note {
  box-shadow: 0px 34px 36px -26px hsla(0, 0%, 0%, 0.5);
  background: linear-gradient(transparent 0em, #ffea4b 0) no-repeat;
  margin-left: auto;
  margin-right: auto;
  height:220px;
  width:220px;
  outline: none;
  resize: none;
  padding: 25px 20px 25px;
  border: none;
  font-family: 'Nanum Pen Script', cursive;
  font-size: 20px;
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
.drawer{
    position: fixed;
    right: 0;
    width: 300px;
    display: flex;
    flex-direction: column;
    height: 100%;
    border-left: 1px #eee solid;
    z-index: 2147483646;
    background: white;
    align-content: center;
}
</style>