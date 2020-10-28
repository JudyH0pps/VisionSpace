<template>
  <v-container>
    <v-row dense>
        <v-col cols="2">
          <v-card @click="newRoomDialog = true" height="150" width="150" style="display:flex;justify-content:center;align-items:center;border:4px dotted black;border-radius:15px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 20 20">
              <title>
                add
              </title>
              <path d="M16 9h-5V4H9v5H4v2h5v5h2v-5h5V9z"/>
            </svg>
          </v-card>
          <v-dialog
          v-model="newRoomDialog"
          width="500"
          >
            <v-card>
              <v-card-title class="headline grey lighten-2">
                Create New Room
              </v-card-title>

              <v-card-text>
                새로운 보드를 생성합니다. 보드의 이름을 입력해주세요.
              </v-card-text>
              <v-card-text>
                <input class="roomNameInput" v-model="newRoomName">
              </v-card-text>
              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                  <v-btn
                  color="primary"
                  @click="addRoom"
                  >
                  CREATE
                  </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
        <v-col v-for="room in rooms" :key="room.title" cols="2">
          <v-card height="150" width="150" @click="moveToBoard(room.code)">
              <v-card-title>{{ room.name }}</v-card-title>
          </v-card>
        </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    newRoomDialog: false,
    newRoomName: '',
    rooms: [
        { name: 'Board 1', code: 'abced' },
        { name: 'Board 2', code: 'abcda' },
        { name: 'Board 3', code: 'abcdk' },
        { name: 'Board 4', code: 'abcdf' },
    ],
  }),
  watch: {
    newRoomDialog() {
      this.newRoomName = '';
    }
  },
  methods: {
    moveToBoard(_code) {
      this.$router.push({ name: 'board', params: {code:_code}})

    },
    addRoom() {
      if (this.newRoomName === '') {
        alert('보드 이름을 입력해주세요');
        return
      }
      let newRoom = {};
      newRoom.name = this.newRoomName;
      newRoom.code = 'random';
      this.rooms.unshift(newRoom);
      this.newRoomDialog = false;
    }
  }
};
</script>

<style>
.plus {
  width: 80%;
  padding: auto auto;
  margin: 50px;
  margin-left: auto;
  margin-right: auto;
}
.text {
  text-align: center;
  /* background-color: yellow; */
  position: absolute;
  top: 40%;
	left: 40%;
  /* transform: translate( -50%, -50% ); */
}
.roomNameInput {
  font-family: 'Nanum Pen Script', cursive;
  background: rgb(247, 245, 245);
  border: 1px solid rgb(184, 184, 184);
  border-radius: 0;
  width: 100%;
  height: 30px;
  font-size: 20px;
}
.roomNameInput:focus {
  outline:2px solid #7a9fc2;
}
.v-card__title {
  font-family: 'Nanum Pen Script', cursive;
  font-size: 25px;
}
</style>