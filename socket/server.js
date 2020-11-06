const app = require('express')();
const server = require('http').createServer(app);
// const path = require('path');
const io = require('socket.io')(server); 
io.origins('*:*') // for latest version
const cors = require('cors');
// peer
const { ExpressPeerServer } = require('peer');
const peerServer = ExpressPeerServer(server, {
    debug: true
})

app.use('/peerjs',peerServer)
app.use(cors());

app.all('/*', function(req, res, next) { 
    res.header("Access-Control-Allow-Origin", "*"); 
    res.header("Access-Control-Allow-Headers", "X-Requested-With"); next(); 
}); 


app.get('/', (req, res) => {
    // res.redirect(`/${uuidv4()}`); 
    res.header("Access-Control-Allow-Origin", "*"); 
})

const loginId = {}

io.on('connection' , function(socket) { 

    console.log('Connect from Client: '+ socket.handshake.address)                      
    let roomName = ''
    let userName = ''

    socket.on('join', (data) => {
        roomName = data.code;
        userName = data.name;
        console.log(loginId);
        // 새로 만들어진 방에 처음 접속했거나, 이미 만들어진 방에 처음 접속했다면
        // socket.join(roomName)
        if (typeof loginId[data.code]=="undefined" || typeof loginId[data.code][data.name]=="undefined" || loginId[data.code][data.name] == 0) {
            if (roomName in loginId) loginId[roomName][userName] = 1;
            else {
                loginId[roomName] = {};
                loginId[roomName][userName] = 1;
            }
        } else {
            loginId[roomName][userName] += 1;
            return;
        }
        console.log(loginId);
        socket.to(roomName).broadcast.emit('user-connected', userName);
        console.log(roomName + '에 ' + userName + '접속')
        io.sockets.in(roomName).emit('chat', {name: 'system', message: userName + '님이 접속하셨습니다.'});
    })
    socket.on('leave', (data) => {
        console.log(data)
        console.log(roomName + '에서' + userName + '나감')
        if (roomName in loginId && userName in loginId[roomName]) loginId[roomName][userName] -= 1;
        socket.leave(roomName);
        io.sockets.in(roomName).emit('chat', {name: 'system', message: userName + '님이 나가셨습니다.'});
    })
    socket.on('chat', function(data){ 
        console.log('message from Client: ' + data) 
        console.log(data)
        console.log(roomName)
        io.sockets.in(roomName).emit('chat', data);
        
    }); 
    socket.on('moveNote', function(data){ 
        io.sockets.in(roomName).emit('moveNote', data);
    }); 
    socket.on('changeTabName', function(){ 
        console.log(roomName, '탭수정')
        io.sockets.in(roomName).emit('changeTabName');
    }); 
    socket.on('logout', () => {
        socket.emit('logout');
    });
    socket.on('disconnect', function() {
        if (roomName in loginId && userName in loginId[roomName]) loginId[roomName][userName] = 0;
        // io.sockets.in(roomName).emit('chat', {name: 'system', message: userName + '님이 나가셨습니다.'});
        console.log('user disconnected:' + userName, roomName);
        socket.to(roomName).broadcast.emit('user-disconnected', userName)
    });
    socket.on('join-room', (roomId,userName) => {
        console.log('///////////////////////////////////////')
        socket.join(roomId)
        socket.to(roomId).broadcast.emit('user-connected',userName);
    });
}) 

server.listen(8081, () => { 
    console.log('socket io server listening on port 8081') 
})
