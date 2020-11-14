import Vue from "vue"
import Room from "janus-room";

export default {
    namespaced: true,
    state: {
        videoroom: null,
        sessionId: null,
        options: null,
        publisherInfo: null,
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
        SET_SUBSCRIBER_INIT(state) {
            state.subscriberList = Object()
        },
        SET_SUBSCRIBER_INSERT(state, payload) {
            Vue.set(state.subscriberList, payload.remoteId, payload)
            // state.subscriberList[payload.remoteId] = payload
        },
        SET_SUBSCRIBER_OUT(state, payload) {
            Vue.delete(state.subscriberList, payload.remoteId)
            // delete state.subscriberList[payload.remoteName]
        },
        SET_SUBSCRIBER_CLEAN(state) {
            state.subscriberList = null
        }
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

                // const setStopVideo = `<i class="fas fa-video"></i><span >화면 끄기</span>`
                // const setVideo = `<i class="stopVideo fas fa-video-slash"></i><span >화면 켜기</span>`
                const setStopVideo = `<i class="fas fa-video"></i>`
                const setVideo = `<i class="stopVideo fas fa-video-slash"></i>`
                if (muted) {
                    el.innerHTML = setVideo;
                } else {
                    el.innerHTML = setStopVideo;
                }
            });
        },
        toggleMuteAudio({ state }) {
            state.videoroom.toggleMuteAudio().then((muted) => {
                const el = document.getElementById("toggle-mute-audio");

                // const unMutehtml = `<i class="fas fa-microphone "></i><span>음소거</span>`
                // const mutehtml =  `<i class="unMute fas fa-microphone-slash"></i><span >재 생</span>`
                const unMutehtml = `<i class="fas fa-microphone "></i>`
                const mutehtml = `<i class="unMute fas fa-microphone-slash"></i>`
                if (muted) {
                    el.innerHTML = mutehtml;
                } else {
                    el.innerHTML = unMutehtml;
                }
            });
        },
        startShareScreen({ state }) {
            if (state.sessionId === null) {
                console.log("No Session Running")
                return;
            }

            state.videoroom.shareScreen().catch((err) => {
                alert(err);
            });
        },
        stopShareScreen({ state }) {
            if (state.sessionId === null) {
                console.log("No Session Running")
                return;
            }

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
            commit('SET_SUBSCRIBER_CLEAN')
        },
    },
};

