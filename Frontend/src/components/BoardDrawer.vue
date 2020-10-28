<template>
    <div>
        <div class="buttons">
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
        <v-navigation-drawer right absolute v-show="drawer == 1">
        <template v-slot:prepend>
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
        </v-navigation-drawer>
        <v-navigation-drawer right absolute v-show="drawer == 2">
            <template v-slot:prepend>
                <v-container fluid>
                    <Chat />
                </v-container>
            </template>
        </v-navigation-drawer>
        <v-navigation-drawer right absolute v-show="drawer == 3">
            <v-container fluid>
                <v-row dense>
                    <textarea class="note" type="text-area" v-model="new_text"></textarea>
                    <v-btn color='primary' style="text-align:center;margin: 25px auto 15px;" @click="add_note">Add new note</v-btn>
                </v-row>
            </v-container>
        </v-navigation-drawer>
    </div>
</template>

<script>
import Chat from "./Chat.vue";
import WebRtc from './webRtc.vue'

export default {
    name: 'BoardDrawer',
    data() {
        return {
            drawer: 0,
            cards: [
                { title: 'Pre-fab homes', src: '../assets/', flex: 6 },
                { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
                { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
                { title: 'Best airlinsses', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
            ],
            new_text: '',
        }
    },
    methods: {
        drawer_method(no) {
            // alert(no)
            if (this.drawer === no){
                this.drawer = 0;
            }
            else {
                this.drawer = no;
            }
        },
        add_note() {
            if (this.new_text === '') {
                alert('Type any text!');
                return;
            }
            this.$emit('add_note', this.new_text);
            this.new_text = '';
        }
    },
    components: {
        Chat,
        WebRtc,
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
</style>