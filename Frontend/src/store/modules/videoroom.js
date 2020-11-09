export default {
    state: {
        sessionId: null,
        videoroom: null,
        options: null,
    },
    getters: {

    },
    mutations: {
        SET_SESSION_ID(state, sessionId) {
            state.sessionId = sessionId
        },
        SET_VIDEO_ROOM(state, videoroom) {
            state.videoroom = videoroom
        },
        SET_OPTION(state, option) {
            state.option = option
        }
    },
    actions: {
        register(context) {
            // state 값에 접근하는 방법: {commit, state} <-- 이 방법을 잊지 말자!
            console.log("register");
        },
        unpublish(context) {
            console.log("unpublish");
        },
        toggleMuteVideo(context) {
            console.log("toggleMuteVideo");
        },
        toggleMuteAudio(context) {
            console.log("toggleMuteAudio");
        },
        startShareScreen(context) {
            console.log("startShareScreen");
        },
        stopShareScreen(context) {
            console.log("stopShareScreen");
        },
    },
};

