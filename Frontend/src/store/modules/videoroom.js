import Room from "janus-room";

export default {
    namespaced: true,
    state: {
        videoroom: null,
        sessionId: null,
        options: null,
    },
    getters: {
        getSessionId: state => {
            return state.sessionId
        },
        getVideoRoom: state => {
            return state.videoroom
        },
        getOptions: state => {
            return state.options
        },
    },
    mutations: {
        SET_SESSION_ID(state, payload) {
            state.sessionId = payload.sessionId
        },
        SET_VIDEO_ROOM(state) {
            state.videoroom = new Room(state.options)
        },
        SET_OPTION(state, payload) {
            state.options = payload
        },
    },
    actions: {
        initializeJanusRoom({ state }, username) {
            state.videoroom
                .init()
                .then(function () {
                    // console.log(state.videoroom);
                    setTimeout(function () {
                        state.videoroom.register({
                            username: username,
                            room: state.sessionId,
                        });
                    }, 1000);
                })
                .catch((err) => {
                    alert(err);
                });
        },
        register() {
            // state 값에 접근하는 방법: {commit, state} <-- 이 방법을 잊지 말자!
            console.log("register");
        },
        unpublish() {
            console.log("unpublish");
        },
        toggleMuteVideo() {
            console.log("toggleMuteVideo");
        },
        toggleMuteAudio() {
            console.log("toggleMuteAudio");
        },
        startShareScreen() {
            console.log("startShareScreen");
        },
        stopShareScreen() {
            console.log("stopShareScreen");
        },
    },
};

