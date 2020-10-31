<template>
  <div class="msgList">
    <div v-for="(msg,index) in msgs" :key="index">
        <span>{{ msg.from.name }}</span>
        <div class="content">
            {{ msg.msg }}
        </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'MessageList',
    props:['msgs'],
};
</script>

<style scoped>
.list-item {
    display: inline-block;
    margin-right:10px;
}
.list-enter-active, .list-leave-active {
    transition: all ls;
}
.list-enter, .list-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
.msgList {
    padding: 10px;
    overflow-y: scroll;
    height: 100%;
    font-family: 'Nanum Pen Script', cursive;
}
.content {
    border-radius: 0px 15px 15px 15px;
    background: white;
    padding: 10px 10px 10px 10px;
    margin-right: auto;
    width: 80%;
    white-space:normal;
    font-size: 18px;
}
.msgList::-webkit-scrollbar{
    width: 0.25rem;
}

.msgList::-webkit-scrollbar-track{
    background: #ffffff;
}

.msgList::-webkit-scrollbar-thumb{
    background: #ffa8f3;
}
</style>