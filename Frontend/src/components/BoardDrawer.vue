<template>
    <div>
    <v-btn class="mx-2" color="white" @click.stop="drawer_method(1)">
        Member List
    </v-btn>
    <v-btn class="mx-2" color="white" @click.stop="drawer_method(2)">
        Chatting
    </v-btn>
        <v-navigation-drawer right absolute v-show="drawer == 1">
        <template v-slot:prepend>
            <v-container fluid>
                <v-row dense>
                    <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
                    <v-card>
                        <v-img src="../assets/person-icon.png" class="white--text align-end" height="100px">
                        <!-- <v-card-title v-text="card.title"></v-card-title> -->
                        </v-img>
                    </v-card>
                    </v-col>
                </v-row>
                </v-container>
                <!-- <button >추가하기</button> -->
            </template>
            <v-divider></v-divider>
            <v-container fluid>
                <v-row dense>
                <p style="width:100%;text-align:center;">Add new note</p>
                <!-- <Chat /> -->
                <textarea class="note" type="text-area"></textarea>

                <!-- <div class="note" style="height:220px;width:220px;"> -->
                <!-- </div> -->
                </v-row>
            </v-container>
        </v-navigation-drawer>
        <v-navigation-drawer right absolute v-show="drawer == 2">
            <template v-slot:prepend>
                <v-container fluid>
                <v-row dense>
                    <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
                    <v-card>
                        <v-img src="../assets/person-icon.png" class="white--text align-end" height="100px">
                        <!-- <v-card-title v-text="card.title"></v-card-title> -->
                        </v-img>
                    </v-card>
                    </v-col>
                </v-row>
                </v-container>
            </template>
        </v-navigation-drawer>
    </div>
</template>

<script>
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
        }
    }

}
</script>

<style scoped>
.v-btn {
  position: absolute;
  left: 50%;
  bottom: 5px;
  translate: linear;
}
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
  padding: 25px 10px 25px;
  border: none;
}
</style>