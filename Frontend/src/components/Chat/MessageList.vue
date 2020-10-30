<template>
  <v-list v-auto-bottom="msgs">
      <transition-group name="list">
          <div v-for="(msg,index) in msgs" :key="index">
              <v-list-tile>
                  <v-list-tile-action>
                      <span>{{ msg.from.name }}</span>
                  </v-list-tile-action>
                  <v-list-tile-content>
                      <v-list-tile-title>{{ msg.msg }}</v-list-tile-title>
                  </v-list-tile-content>
              </v-list-tile>
              <v-divider inset></v-divider>
          </div>
      </transition-group>
  </v-list>
</template>

<script>
export default {
    name: 'MessageList',
    props:['msgs'],
};
</script>

<style>
.list-item {
    display: inline-block;
    margin-right:10px;
}
.list-enter-active, .list-leave-active {
    transition: all ls;
}
.list-enter, .list-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
</style>