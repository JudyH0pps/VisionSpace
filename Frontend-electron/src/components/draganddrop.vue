<template>
    <div style="display:flex;flex-direction:column;align-items:center;">
      <!--UPLOAD-->
      <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
        <div class="dropbox note">
          <input type="file" multiple :name="uploadFieldName" :disabled="isSaving" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
            accept="image/*" class="input-file">
            <p v-if="isInitial">
              Drag your file here<br>or<br>click to browse
            </p>
            <p v-if="isSaving">
              <!-- Uploading {{ fileCount }} files... -->
              uploading...
            </p>
        </div>
      </form>
      <!--SUCCESS-->
      <div v-if="isSuccess">
        <!-- <h2>Uploaded {{ uploadedFiles.length }} file successfully.</h2> -->
        <!-- <p>
          <a href="javascript:void(0)" @click="reset()">Upload again</a>
        </p> -->
        <div class="note">
            <img v-for="(item, index) in uploadedFiles" :key="index" :src="item.url" class="img-responsive img-thumbnail" :alt="item.originalName">
        </div>
      </div>
      <!--FAILED-->
      <div v-if="isFailed">
        <h2>Uploaded failed.</h2>
        <p>
          <a href="javascript:void(0)" @click="reset()">Try again</a>
        </p>
        <pre>{{ uploadError }}</pre>
      </div>
      <v-btn color='primary' style="text-align:center;margin: 25px auto 15px;" @click="addNote">Add new note</v-btn>
    </div>
</template>

<script>
import SERVER from '@/api/drf'
import axios from 'axios'
import cookies from 'vue-cookies'
  // swap as you need
  import { upload } from './file-upload.fake.service'; // fake service
  // import { upload } from './file-upload.service';   // real service
  import { wait } from './utils';
  const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;
  export default {
    name: 'draganddrop',
    data() {
      return {
        selectedFile: null,
        uploadedFiles: [],
        uploadError: null,
        currentStatus: null,
        uploadFieldName: 'photos'
      }
    },
    props: {
         activatedTab: Number,
    },
    computed: {
      isInitial() {
        return this.currentStatus === STATUS_INITIAL;
      },
      isSaving() {
        return this.currentStatus === STATUS_SAVING;
      },
      isSuccess() {
        return this.currentStatus === STATUS_SUCCESS;
      },
      isFailed() {
        return this.currentStatus === STATUS_FAILED;
      }
    },
    methods: {
        addNote() {
            // console.log(this.uploadedFiles);
        let new_note = new FormData();
        new_note.append('width', 220);
        new_note.append('height', 220);
        new_note.append('x', 150);
        new_note.append('y', 150);
        new_note.append('z', 150);
        new_note.append('content',this.selectedFile);
        new_note.append('type', 2);
        // this.notes[this.activatedTab].push(new_note)
        let config = {
          headers: {
            Authorization: 'Bearer ' + cookies.get('auth-token')
          }
        };
        axios.post(SERVER.URL + '/api/v1/board/' + this.$route.params.code + '/tab/' + this.activatedTab + '/note/', new_note, config)
          .then(() => {
            this.$socket.emit('moveNote', {tab: this.activatedTab})
            this.fetchNoteList();
          })
          .catch(err => console.log(err.response.data))                    

        },
      reset() {
        // reset form to initial state
        this.currentStatus = STATUS_INITIAL;
        this.uploadedFiles = [];
        this.uploadError = null;
      },
      save(formData) {
        // upload data to the server
        this.currentStatus = STATUS_SAVING;
        upload(formData)
          .then(wait(1500)) // DEV ONLY: wait for 1.5s 
          .then(x => {
            this.uploadedFiles = [].concat(x);
            this.currentStatus = STATUS_SUCCESS;
          })
          .catch(err => {
            this.uploadError = err.response;
            this.currentStatus = STATUS_FAILED;
          });
      },
      filesChange(fieldName, fileList) {
        // handle file changes
        // console.log(fileList[0])
        this.selectedFile = fileList[0];
        const formData = new FormData();
        if (!fileList.length) return;
        // append the files to FormData
        Array
          .from(Array(fileList.length).keys())
          .map(x => {
            formData.append(fieldName, fileList[x], fileList[x].name);
          });
        // save it
        this.save(formData);
      }
    },
    mounted() {
      this.reset();
    },
  }
</script>

<style lang="scss">
  .dropbox {
    outline: 2px dashed grey; /* the dash box */
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    padding: 10px 10px;
    min-height: 200px; /* minimum height */
    position: relative;
    cursor: pointer;
  }
  
  .input-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    // height: 200px;
    // position: absolute;
    cursor: pointer;
  }
  
  .dropbox:hover {
    background: lightblue; /* when mouse over to the drop zone, change color */
  }
  
  .dropbox p {
    font-size: 1.2em;
    text-align: center;
    padding: 0;
  }
  li {
      list-style: none;
  }
  .note {
  box-shadow: 0px 34px 36px -26px hsla(0, 0%, 0%, 0.5);
  background: linear-gradient(transparent 0em, #f8f1ba 0) no-repeat;
  margin-left: auto;
  margin-right: auto;
  height:220px;
  width:220px;
  outline: none;
  resize: none;
  padding: 25px 20px 25px;
  border: none;
  font-family: 'Nanum Pen Script', cursive;
  font-size: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.note img {
    height: 100%;
}
input {
    position: absolute;
    height: 100%;
    transform: translate(-20px, -25px);
}
</style>