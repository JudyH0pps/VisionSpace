<template>
    <vue-draggable-resizable :w="220" :h="220" :x="note.x" :y="note.y" @dragging="onDrag" :resizable="false" :parent="true" :drag-handle="'.line'">
        <svg class="line" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="40" height="40" viewBox="0 0 24 24"><path d="M16,12V4H17V2H7V4H8V12L6,14V16H11.2V22H12.8V16H18V14L16,12Z" /></svg>
        <div class="content" v-html="note.content">
        </div>
        <div style="position:absolute;left:5px;bottom:5px;">
            <v-icon class="del_btn" @click="del_note(index)">mdi-trash-can-outline</v-icon>
        </div>
    </vue-draggable-resizable>
</template>

<script>
export default {
    name: 'Note',
    data() {
        return {
            
        }
    }
}
</script>