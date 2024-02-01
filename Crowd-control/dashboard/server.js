const express = require("express");
const fs = require("fs");
const {
    parse
} = require("papaparse");

app = express()
http = require("http").Server(app);
socketIO = require("socket.io")(http, {
    maxHttpBufferSize: 1e8
});


var global_counter = 0;
var cam_to_counter = Array(10);
for (let i = 0; i < 10; i++) {
    cam_to_counter[i] = new Array(2);
}

function send(file, response) {
    fs.readFile(__dirname + file,
        (err, data) => {
            if (err) {
                response.writeHead(500)
                return response.end("Error loading client.html");
            }
            response.writeHead(200)
            response.end(data);
        }
    );
}

socketIO.on("connection", function (socket) {
    console.log("We have a connection");

    socket.on('setData', (data) => {
        global_counter += data['counter']
        cam_to_counter[data['camera_id'] - 1][0] = data['counter'];
        cam_to_counter[data['camera_id'] - 1][1] = data['base-64_img'];
        socketIO.emit("increase_counter", { counter: data['counter'], camera_id: data['camera_id'], image: data['base-64_img'] });
        console.log("Current global counter:", global_counter);
    });
});


app.get("/", (req, res) => {
    console.log("client");
    send("/client.html", res);
})

app.get('/counters', (req, res) => {
    console.log("Displaying counters for the last 30 seconds");
    res.setHeader("Content-Type", "application/json");
    res.send(JSON.stringify(
        { counter: global_counter }
    ));
    global_counter = 0;
});

http.listen(4400)
console.log("Server Listening on http://localhost:4400");
