<template>
  <div class="home">
    <RoomList/>
  </div>
</template>

<script>
// @ is an alias to /src
import RoomList from '@/components/RoomList.vue'
export default {
  name: 'Home',
  components: {
    RoomList
  }
}
</script>

<style scoped>
h1 {
  text-align: center;
}
</style>
