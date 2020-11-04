<template>
  <div>
    <p>DEBUG</p>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "Google-Login-Handler",
  methods: {
    ...mapActions(["google_login"]),
  },
  created() {
    this.google_login({
      code: this.$route.query.code,
    });
  },
};
</script>

<style>
</style>