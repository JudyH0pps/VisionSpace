<template>
  <v-app>
    <div class="container">
      <div class="row">
        <div class="col-1 col-md-12">
          <p>{{ roomId }}</p>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script>
export default {
  name: "WebRTC",
  components: {},
  data() {
    return {
      img: null,
      roomId: "",
    };
  },
  computed: {},
  watch: {},
  methods: {},
  created() {
    this.roomId = this.$route.params.code;
  },
  mounted() {
    // this.onJoin();
  },
  destroyed() {
    // this.onLeave();
  },
};
</script>
<style scoped>
.btn-primary {
  margin-left: 5px;
}
</style>
