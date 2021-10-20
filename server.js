const express = require("express");
const app = express();
const port = process.env.PORT || 5500;
app.use(express.static('public'));
const http = require("http").Server(app);

const io = require("socket.io")(http); //io is now going to listen on the server and wait for the client to connect, then setup a socket connection

app.get("/", (req, res) => res.sendFile(__dirname + "/home.html"));

http.listen(port, function() {
    console.log(`listen on ${port}`);
});



io.on("connection", (socket) => {
  console.log(`socket connection: ${socket.id}`);

  //message from the client and sends (emits) to the client
  socket.on("message", (data) => {
    io.sockets.emit('message', data)  
  })

  //typing events and to all clients but sender
  socket.on('typing', (data) => {
    socket.broadcast.emit('typing', data);
  })

});

