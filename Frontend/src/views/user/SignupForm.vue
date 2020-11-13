<template>
  <div id="con">
    <v-container id="signinup-form" class="fill-height">
      <!-- <Notification
      :message="snackbarMessage"
      :snackbar="snackbar"
      :type="snackbarType"
    /> -->
      <v-row align="center" justify="center" no-gutters>
        <v-col cols="12" sm="8" md="8" class="">
          <v-card class="evelation-12 card">
            <v-window v-model="step">
              <!--SignIn-->
              <v-window-item :value="1">
                <v-row class="">
                  <v-col cols="12" md="8" class="pt-6 pb-6">
                    <v-card-text>
                      <v-form class="signup-form-form">
                        <h1
                          class="text-center display-1 mb-10"
                          :class="`${bgColor}--text`"
                        >
                          Login
                        </h1>
                        <v-text-field
                          id="username"
                          v-model="loginData.username"
                          label="Username"
                          name="Username"
                          append-icon="person"
                          type="text"
                          :color="bgColor"
                        />
                        <v-text-field
                          id="password"
                          v-model="loginData.password"
                          label="Password"
                          name="Password"
                          append-icon="lock"
                          type="password"
                          :color="bgColor"
                        />
                        <div class="text-center">
                          <a
                            href="#"
                            class="mt-3 overline no-text-decoration"
                            :class="`${bgColor}--text`"
                            @click="step = 3"
                          >
                            Forgot your password?
                          </a>
                        </div>
                        <div class="text-center mt-6">
                          <v-btn
                            type="button"
                            large
                            :color="bgColor"
                            dark
                            @click="login(loginData)"
                            >Login</v-btn
                          >
                        </div>
                        <!-- <div
                          style="height:40px;width:40px;display:flex;justify-content:center;align-items:center;margin: 0 auto 15px;position:relative;transform:translateY(35px);background:white;border-radius:50%;border:1px #dddddd solid;"
                        >or</div> -->
                        </v-form>
                        <!-- <v-divider></v-divider> -->
                        <div class="text-center" style="margin-top: 30px;">
                          <a
                            href="https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://k3c102.p.ssafy.io/google-login&prompt=consent&response_type=code&client_id=92928176186-4g466nfn41s6ptuqkb42ior3rhmnhgkv.apps.googleusercontent.com&scope=email&access_type=offline"
                            class="mt-3 overline no-text-decoration"
                            :class="`${bgColor}--text`"
                          >
                            <v-img src="../../assets/google-login-button.png" width="250" style="margin: 0 auto 0; border:1px solid #4285f4"></v-img>
                          </a>
                        </div>
                    </v-card-text>
                  </v-col>
                  <v-col
                    cols="12"
                    md="4"
                    class="darken-2 vcenter"
                    :class="`${bgColor}`"
                  >
                    <div>
                      <v-card-text :class="`${fgColor}--text`">
                        <h1 class="text-center headline mb-3">No User?</h1>
                        <h5 class="text-center overline mb-3">
                          Please Sign Up to continue
                        </h5>
                      </v-card-text>
                      <div class="text-center mb-6">
                        <v-btn dark outlined @click="step = 2">Sign Up</v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-window-item>
              <!--SignUp-->
              <v-window-item :value="2">
                <v-row class="fill-height">
                  <v-col
                    cols="12"
                    md="4"
                    class="darken-2 vcenter"
                    :class="`${bgColor}`"
                  >
                    <div>
                      <v-card-text :class="`${fgColor}--text`">
                        <h1 class="text-center headline mb-3">
                          Already a user?
                        </h1>
                        <h5 class="text-center overline mb-3">Please Login</h5>
                      </v-card-text>
                      <div class="text-center mb-6">
                        <v-btn dark outlined @click="step = 1">Login</v-btn>
                      </div>
                    </div>
                  </v-col>
                  <v-col cols="12" md="8" class="pt-6 pb-6">
                    <v-card-text>
                      <h1
                        class="text-center display-1 mb-10"
                        :class="`${bgColor}--text`"
                      >
                        Sign Up
                      </h1>
                      <v-form
                        class="signup-form-form"
                        @submit.prevent="signup(signupData)"
                      >
                        <v-text-field
                          id="username"
                          v-model="signupData.username"
                          label="Username"
                          name="username"
                          append-icon="person"
                          type="text"
                        />
                        <v-text-field
                          id="nickname"
                          v-model="signupData.nickname"
                          label="Nickname"
                          name="nickname"
                          append-icon="person"
                          type="text"
                        />
                        <v-text-field
                          id="email"
                          v-model="signupData.email"
                          label="eMail"
                          name="email"
                          append-icon="email"
                          type="email"
                        />
                        <v-text-field
                          id="password"
                          v-model="signupData.password1"
                          label="Password"
                          name="password"
                          append-icon="lock"
                          type="password"
                        />
                        <v-text-field
                          id="passwordConfirm"
                          v-model="signupData.password2"
                          label="Password-confirm"
                          name="passwordConfirm"
                          append-icon="lock"
                          type="password"
                        />
                        <div class="text-center mt-6">
                          <v-btn type="submit" large :color="bgColor" dark>
                            Sign Up</v-btn
                          >
                        </div>
                      </v-form>
                    </v-card-text>
                  </v-col>
                </v-row>
              </v-window-item>
              <!--PW Rest-->
              <v-window-item :value="3">
                <v-row class="fill-height">
                  <v-col
                    cols="12"
                    md="4"
                    class="darken-2 vcenter"
                    :class="`${bgColor}`"
                  >
                    <div>
                      <v-card-text :class="`${fgColor}--text`">
                        <h1 class="text-center headline mb-3">
                          Already a user?
                        </h1>
                        <h5 class="text-center overline mb-3">Please Login</h5>
                      </v-card-text>
                      <div class="text-center mb-6">
                        <v-btn dark outlined @click="step = 1">Login</v-btn>
                      </div>
                    </div>
                  </v-col>
                  <v-col cols="12" md="8" class="pt-6 pb-6">
                    <v-card-text>
                      <v-form class="signup-form-form">
                        <h1
                          class="text-center display-1 mb-10"
                          :class="`${bgColor}--text`"
                        >
                          Reset Password
                        </h1>
                        <v-text-field
                          id="login"
                          v-model="login"
                          label="Username / eMail"
                          name="login"
                          append-icon="person / email"
                          type="text"
                          :color="bgColor"
                          class="v-input__icon--double"
                        />
                        <div class="text-center mt-6">
                          <v-btn large :color="bgColor" dark
                            >Reset Password</v-btn
                          >
                        </div>
                      </v-form>
                    </v-card-text>
                  </v-col>
                </v-row>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "SignupForm",
  components: {},
  props: {
    source: {
      type: String,
      default: "",
    },
    bgColor: {
      type: String,
      default: "indigo",
    },
    fgColor: {
      type: String,
      default: "white",
    },
  },
  // async fetch({ store, error }, user) {
  //   try {
  //     await store.dispatch('users/signupUser', user)
  //   } catch (e) {
  //     error({
  //       statusCode: 503,
  //       message: 'Unable to sign up user. Please try again later.'
  //     })
  //   }
  // },
  data: () => ({
    loginData: {
      username: null,
      password: null,
    },
    signupData: {
      username: null,
      nickname: null,
      email: null,
      password1: null,
      password2: null,
    },
    step: 1,
    // username: '',
    // email: '',
    // password: '',
    // passwordConfirm: '',
    // login: '',
    snackbarType: "success",
    snackbarMessage: "",
    snackbar: false,
  }),
  methods: {
    ...mapActions(["signup", "login"]),
    movingBackground() {
      let con = document.querySelector("#con");
      window.onmousemove = function (e) {
        let x = -e.clientX / 100,
          y = -e.clientY / 100;
        con.style.backgroundPositionX = x + "px";
        con.style.backgroundPositionY = y + "px";
      };
    },
    // signup() {
    //   this.$auth
    //     .signup({
    //       data: {
    //         user: {
    //           username: this.username,
    //           email: this.email,
    //           password: this.password
    //         }
    //       }
    //     })
    //     .catch((e) => {
    //       this.error = e + ''
    //     })
    // },
    // async signin() {
    //   try {
    //     const response = await this.$auth.loginWith('local', {
    //       data: {
    //         login: this.login,
    //         password: this.password
    //       }
    //     })
    //     this.snackbarType = response.data.type
    //     this.snackbarMessage = response.data.message
    //     this.snackbar = true
    //   } catch (err) {
    //     this.snackbarType = 'error'
    //     this.snackbarMessage = 'Error signing you in'
    //     this.snackbar = true
    //   }
    // }
  },
  mounted() {
    document.documentElement.scrollTop = 0;
    // this.movingBackground();
  },
};
</script>

<style scoped lang="scss">
.v-input__icon--double .v-input__icon {
  margin-left: -4.25rem !important;
}
a.no-text-decoration {
  text-decoration: none;
}
#signinup-form {
  max-width: 75rem;
}
.signup-form-form {
  max-width: 23rem;
  margin: 0 auto;
}
.card {
  overflow: hidden;
}
.vcenter {
  display: flex;
  align-items: center;
  justify-content: center;
}
#con {
  position: absolute;
  /* top: 5%;
    left: 5%;
    right: 5%;
    bottom: 5%; */
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url("../../assets/space2.jpg") #151729;
  background-size: cover;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
  z-index: 10000;
}
</style>