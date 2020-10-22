// console.log('hi')
const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const { v4: uuidV4 } = require('uuid')


app.set('view engine', 'ejs')
    // public은 javascript 사용을 위해
app.use(express.static('public'))

// 1-2. room parameter를 사용 (uuid를 사용, 그래서 roomId 가 아니라 uuidV4)
app.get('/', (req, res) => {
    // 개인 uuid 번호 확인 
    // 2-1. res.redirect(`/${uuidV4()}`) 실행 후 localhost:3000 확인
    // 2-2. url을 확인하면 uuid 생성 , 다른 크롬 창에서 실행하면 다른 uuid 할당
    res.redirect(`/${uuidV4()}`)

    // res.redirect(`/${roomId}`)
})

// 1-1. room parameter를 지정
app.get('/:room', (req, res) => {
    res.render('room', { roomId: req.params.room })
})

// io는 communicate 기능
io.on('connection', socket => {
    socket.on('join-room', (roomId, userId) => {
        // console.log(roomId, UserId)
        // 새로운 유저가 들어올 때 join을 사용(roomId는 먼저 있다고 가정)
        socket.join(roomId)

        // send message to room, 나빼고 모든 사람들에게 알리는 기능
        socket.to(roomId).broadcast.emit('user-connected', userId)

        // 방을 나갈 때 빠른 반응을 위해서 
        socket.on('disconnect', () => {
            socket.to(roomId).broadcast.emit('user-disconnected', userId)
        })
    })
})

// port 3000 사용
server.listen(3000)