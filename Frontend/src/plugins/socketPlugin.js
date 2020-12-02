import Vue from 'vue';
import io from 'socket.io-client'

const socket = io.connect('https://k3c102.p.ssafy.io', { resource: 'socket/socket.io' });

const SocketPlugin = {
    install(vue) {
        vue.mixin({
        });

        vue.prototype.$sendMessage = ($payload) => {
            socket.emit('chat', {
                msg: $payload.msg,
                name: $payload.name,
            });
        };

        vue.prototype.$socket = socket;
    },
};

Vue.use(SocketPlugin);
