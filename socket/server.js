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

io.on('connection' , function(socket) { 

    console.log('Connect from Client: '+ socket.handshake.address)                      
    let roomName = ''
    let userName = ''
    socket.on('join', (data) => {
        console.log(data)
        roomName = data.code;
        userName = data.name;

        socket.join(roomName)
        socket.to(roomName).broadcast.emit('user-connected', userName);
        console.log(roomName + '에 ' + userName + '접속')
        io.sockets.in(roomName).emit('chat', {name: userName, message: userName + '님이 접속하셨습니다.'});
    })
    socket.on('leave', (data) => {
        console.log(data)
        console.log(roomName + '에서' + userName + '나감')
        socket.leave(roomName);
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
    socket.on('disconnect', function() {
        console.log('user disconnected:' + userName);
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
