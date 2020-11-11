import Room from "janus-room";

export default {
    namespaced: true,
    state: {
        videoroom: null,
        sessionId: null,
        options: null,
        subscriberList: null,
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
        getSubscriberList: state => {
            return state.subscriberList
        },
    },
    mutations: {
        SET_SESSION_ID(state, payload) {
            if (payload === null || payload === undefined) {
                state.sessionId = payload
            }

            else {
                state.sessionId = payload.sessionId
            }
        },
        SET_VIDEO_ROOM(state) {
            state.videoroom = new Room(state.options)
        },
        SET_VIDEO_ROOM_CLEAN(state) {
            console.log("Deleting Room class...")
            state.videoroom = null
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
        register({ state }) {
            // state 값에 접근하는 방법: {commit, state} <-- 이 방법을 잊지 말자!
            state.videoroom.register({
                username: state.username,
                room: state.sessionId
            })
        },
        unpublish({ state }) {
            state.videoroom.unpublishOwnFeed().then(() => {
                setTimeout(() => {
                    state.videoroom.stop();
                    state.videoroom.leaveRoom();
                }, 500);
            });
        },
        toggleMuteVideo({ state }) {
            state.videoroom.toggleMuteVideo().then((muted) => {
                const el = document.getElementById("toggle-mute-video");
                if (muted) {
                    el.innerHTML = "Resume webcam";
                } else {
                    el.innerHTML = "Pause webcam";
                }
            });
        },
        toggleMuteAudio({ state }) {
            state.videoroom.toggleMuteAudio().then((muted) => {
                const el = document.getElementById("toggle-mute-audio");
                if (muted) {
                    el.innerHTML = "Unmute";
                } else {
                    el.innerHTML = "Mute";
                }
            });
        },
        startShareScreen({ state }) {
            state.videoroom.shareScreen().catch((err) => {
                alert(err);
            });
        },
        stopShareScreen({ state }) {
            state.videoroom.stopShareScreen().catch((err) => {
                alert(err);
            });
        },
        joinRoomHandler({ state }) {
            if (state.sessionId) {
                return;
            }

            state.videoroom.publishOwnFeed({
                audioSend: true,
                videoSend: true,
                replaceVideo: true,
                replaceAudio: true,
            })
        },
        leaveRoomHandler({ commit, state }) {
            if (state.sessionId === null) {
                return;
            }

            // 명시적으로 클린하게 세션을 정리하도록 한다.
            state.videoroom.unpublishOwnFeed(); // When Vue page has destroyed. then is not working.
            state.videoroom.leaveRoom();
            state.videoroom.stop();
            commit('SET_SESSION_ID', null)
            commit('SET_VIDEO_ROOM_CLEAN')
            commit('SET_OPTION', null)
        },
    },
};

