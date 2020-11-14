<template>
  <div class="container">
    <p>Restore Debug Phase</p>
    <!-- <div class="btns">
      <v-btn class="mr-2" @click="getPaginatedList('prev')">Prev</v-btn>
      <v-btn @click="getPaginatedList('next')">Next</v-btn>
    </div> -->
    <v-container>
      <v-row>
        <v-col v-for="(value, idx) in restore_list" :key="idx">
          <div
            v-if="value.type_index === 1"
            :text="value.content"
            :style="swatchStyle(value.color)"
            v-html="value.content"
          ></div>
          <NoteImage
            v-if="value.type_index === 2"
            :src="imgSrc(value.content)"
            :style="swatchStyle(value.color)"

          />
          <iframe
            v-if="value.type_index === 3"
            style="width:100%"
            :style="swatchStyle(value.color)"
            :src="youtubeEmbed(value.content)"
            frameborder="1"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
          <!-- {{ value }} -->
          <v-btn @click="requestRestore(value.note_index)">Restore</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import NoteImage from "@/components/NoteImage.vue";

export default {
  name: "Restore",
  components: {
    NoteImage,
  },
  data() {
    return {
      new_text: "",
    };
  },
  props: {
    restore_list: Array,
    restore_prev: String,
    restore_next: String,
  },
  created() {
    console.log("Hello FROM Restore");
    this.$emit("get-list");
  },
  computed: {},
  destroyed() {
    console.log("BYE FROM Restore");
  },
  methods: {
    imgSrc(name) {
      // console.log(name)
      return name.split(" ")[0];
    },
    youtubeEmbed(url) {
      let s = url.split("/");
      return "https://www.youtube.com/embed/" + s[s.length - 1];
    },
    requestRestore(target) {
      this.$emit("restore-request", target);
    },
    // getPaginatedList(target) {
    //   console.log(target);
    //   if (target === "prev" && this.restore_prev) {
    //     this.$emit("page-list", this.restore_prev);
    //   } else if (target === "next" && this.restore_next) {
    //     this.$emit("page-list", this.restore_next);
    //   }
    // },
    getList() {
      this.$emit("get-list");
    },
    swatchStyle(backColor) {
      if (backColor[0] == "#") {
        return {
          boxshadow: "0px 34px 36px -26px hsla(0, 0%, 0%, 0.5)",
          background: `linear-gradient(transparent 0em, ${backColor} 0) no-repeat`,
          marginLeft: "auto",
          marginRight: "auto",
          height: "220px",
          width: "220px",
          outline: "none",
          resize: "none",
          padding: "25px 20px 25px",
          border: "none",
          /* font-family: "Nanum Pen Script", cursive; */
          fontFamily: "HangeulNuri-Bold",
          fontSize: "15px",
        };
      } else {
        return {
          boxshadow: "0px 34px 36px -26px hsla(0, 0%, 0%, 0.5)",
          background: `linear-gradient(transparent 0em, #${backColor} 0) no-repeat`,
          marginLeft: "auto",
          marginRight: "auto",
          height: "220px",
          width: "220px",
          outline: "none",
          resize: "none",
          padding: "25px 20px 25px",
          border: "none",
          /* font-family: "Nanum Pen Script", cursive; */
          fontFamily: "HangeulNuri-Bold",
          fontSize: "15px",
        };
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");

iframe {
  border: 0;
}

.container{
  overflow-y: auto !important;
}

</style>