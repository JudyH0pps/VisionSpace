<template>

    <div>
    <v-btn class="mx-2" fab dark small color="white" @click.stop="drawer = !drawer" :class="{ open:drawer }">
      <v-icon color="black">mdi-arrow-left</v-icon>
    </v-btn>

    <v-navigation-drawer right absolute v-model="drawer">
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
    </div>
</template>

<script>
export default {
    name: 'BoardDrawer',
    data: () => {
        return {
            cards: [
                { title: 'Pre-fab homes', src: '../assets/', flex: 6 },
                { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
                { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
                { title: 'Best airlinsses', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
            ],
            drawer: false,
        }
    },

}
</script>

<style scoped>
.v-btn {
  position: absolute;
  top: 50%;
  right: 0px;
  translate: linear;
}
.open {
  transform: translateX(-255px) rotate(180deg);
}
</style>