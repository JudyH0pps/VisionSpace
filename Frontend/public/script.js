// root path
const socket = io('/')
const videoGrid = document.getElementById('video-grid')

// peer 생성
const myPeer = new Peer(undefined, {
    host: '/',
    port: '3001'
})
const myVideo = document.createElement('video')

// 입장하는 사람들 저장
const peers = {}

// muted 안쓰면 입장 하는 사람마다 모두 마이크 ON! => 개시끄러워짐
myVideo.muted = true

navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false,
}).then(stream => {
    addVideoStream(myVideo, stream)

    // 다른 사람이 접속 시 video 생성
    myPeer.on('call', call => {
        call.answer(stream)

        // 새로 유입된 유저도 기존의 정보를 받게 하기 위해 아래처럼 작성
        const video = document.createElement('video')
        call.on('stream', userVideoStream => {
            addVideoStream(video, userVideoStream)
        })
    })

    // 새로운 유저가 들어왔을 때
    socket.on('user-connected', userId => {
        connectToNewUser(userId, stream)
    })
})

socket.on('user-disconnected', userId => {
    console.log(userId)
    if (peers[userId]) peers[userId].close()
})


myPeer.on('open', id => {
    // ROOM_ID는 path_id, user id를 10으로
    // socket.emit('join-room', ROOM_ID, 10)

    // 다른 사람이 방으로 들어오면 user-conected 실행된다. 매번 새로고침 할 때 마다 새로운 유저가 들어왔다고 인식
    socket.emit('join-room', ROOM_ID, id)


})

// 아래는 확인용 코드
socket.on('user-connected', userId => {
    console.log('User conntected : ' + userId)
})

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream)
    const video = document.createElement('video')
        // video 추가
    call.on('stream', userVideoStream => {
        addVideoStream(video, userVideoStream)
    })

    // 연결 끊기면 close 실행되야 하는데... 왜 안되는거지??
    call.on('close', () => {
        console.log('방금 나갔어요')
        video.remove()
    })

    //peers에 userId 저장
    peers[userId] = call
}

// video 생성
function addVideoStream(video, stream) {
    video.srcObject = stream
    video.addEventListener('loadedmetadata', () => {
        video.play()
    })
    videoGrid.append(video)
        //video 생성 완료
}