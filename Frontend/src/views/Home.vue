<template>
  <div>
    <!-- <div class="left">
      <v-form>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                outlined
                label="회의 코드 입력"
                prepend-inner-icon="mdi-keyboard"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </div>
    <div>
      <img src="@/assets/main.png" alt="">
    </div> -->
    <v-container class="lighten-5">
      <!-- Stack the columns on mobile by making one full-width and the other half-width -->
      <!-- Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop -->

      <!-- Columns are always 50% wide, on mobile and desktop -->
      <v-row>
        <v-col cols="6"
          ><h1 class="mt-10 mb-5 introduce">
            스크랩보드 기반 프리미엄 화상회의를 제공해주는 Vision Space입니다.
          </h1>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
          <v-row>
            <v-col cols="6" class="codeinput">
              <v-text-field
                outlined
                label="회의 코드 입력"
                prepend-inner-icon="mdi-keyboard"
              ></v-text-field></v-col
            ><v-col cols="3"
              ><v-btn class="mr-4 mt-2" type="submit"> 참가 </v-btn></v-col
            ></v-row
          >
          <hr />
          <p>계정이 없으신가요? 지금 <router-link to="login" class="router-link">무료로 가입</router-link>하세요.</p>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row>
      <hr class="mt-5">
      <div>
        <p class="center-text">Vision Space 주요 기능</p>
      </div>
      <v-row>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            나중에 완성 거의 다 됐을 때, 기능별로 정리할게요.
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/board.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            안전하게 사용할 수 있는 Vision Space
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            스크랩보드 기반 프리미엄 화상회의를 제공해주는 Vision Space입니다.
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6"
          ><img src="@/assets/mmain.jpg" alt="" class="mt-10 mmain" />
        </v-col>
        <v-col cols="6"
          ><h2 class="mt-10 mb-5 introduce3">
            안전하게 사용할 수 있는 Vision Space
          </h2>
          <h2 class="mb-5 introduce2">
            국무총리는 국회의 동의를 얻어 대통령이 임명한다. 재산권의 행사는
            공공복리에 적합하도록 하여야 한다
          </h2>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {};
</script>

<style>
.left {
  float: left;
}
.introduce {
  font-size: 48px;
  font-weight: 400;
  letter-spacing: -0.5px;
  line-height: 56px;
}
.introduce2 {
  color: #6a6e74;
  font-size: 20px;
  font-weight: 400;
  letter-spacing: initial;
  line-height: 28px;
}
.codeinput {
  /* padding: 0; */
}
.mmain {
  max-width: 100%;
  height: auto;
}
hr {
  border: solid #dadce0;
  border-width: 1px 0 0;
  clear: both;
  height: 0;
  margin-bottom: 19px;
}
.router-link {
  text-decoration: none;
}
.introduce3 {
    font-size: 36px;
    font-weight: 400;
    letter-spacing: -.25px;
    line-height: 44px;
}
.center-text {
  text-align: center;
}
</style>