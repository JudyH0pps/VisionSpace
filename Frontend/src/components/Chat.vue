<template>
    <md-app>
      <md-app-toolbar class="md-primary">
      </md-app-toolbar>
      <md-app-content>
        <md-field>
          <label>Message</label>
          <md-textarea v-model="textarea" disabled></md-textarea>
        </md-field>
        <md-field>
          <label>Your Message</label> 
          <md-input v-on:keyup.enter="sendMessage" v-model="message"></md-input>
          <md-button class="md-primary md-raised" @click="sendMessage()">Submit</md-button>
        </md-field>
      </md-app-content>
    </md-app>
</template> 

<script> 
    export default { 
        name: 'Chat', 
        created() { 
          this.$socket.on('chat', (data)=> { 
              this.textarea += data.message + "\n" 
          })
        }, 
        data() { 
            return { 
                textarea: "", 
                message: '', 
                // ROOM_ID: roomid,
            } 
        }, 
        methods: { 
            sendMessage () { 
                this.$socket.emit('chat',{ 
                    message: this.message 
                }); 
                
                this.textarea += this.message + "\n"
                this.message = '' 
            } 
        } 
    } 
</script> 

<style scoped>
.md-app {
  height: 800px;
  border: 1px solid rgba(#000, 0.12);
}
.md-textarea {
  height: 300px;
}
</style>