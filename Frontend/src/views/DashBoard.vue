<template>
  <div class="dashboard">
    <RoomList/>
  </div>
</template>

<script>
// @ is an alias to /src
import RoomList from '@/components/RoomList.vue'
export default {
  name: 'DashBoard',
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
