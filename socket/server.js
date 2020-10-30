var app = require('express')();
var server = require('http').createServer(app);
var path = require('path');
var io = require('socket.io')(server); //해당 서버를 소켓 서버로 설정
const { v4: uuidv4 } = require('uuid') //추가

// app.set('view engine', 'vue')
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.all('/*', function(req, res, next) { 
    res.header("Access-Control-Allow-Origin", "*"); 
    res.header("Access-Control-Allow-Headers", "X-Requested-With"); next(); 
}); 


// 이제 localhost:3000/으로 들어오면 uuid 생성하여 redirect 하도록 만들었다.
app.get('/', (req, res) => {
    res.redirect(`/${uuidv4()}`); 
})

app.get('/:room', (req,res) => {
    const roomId = req.params.room
    console.log(roomId)  
    // 앞에 있는 'room'은 room.ejs를 의미, 뒤에잇는 req.params.room은 :room에 있는 paramet를 의미
    res.render('room', { roomId: req.params.room })
})

//connection event handler 
io.on('connection' , function(socket) { 
    console.log('Connect from Client: '+socket) 
    socket.on('chat', function(data){ 
        console.log('message from Client: '+data.message) 
        
        var rtnMessage = { 
            message: data.message 
        }; 

        // 클라이언트에게 메시지를 전송한다 
        socket.broadcast.emit('chat', rtnMessage); 
    }); 
}) 

server.listen(3000, function() { 
    console.log('socket io server listening on port 3000') 
})
