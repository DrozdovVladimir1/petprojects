import * as tf from '@tensorflow/tfjs-node'
import cocoSsd from '@tensorflow-models/coco-ssd';
import fs from 'fs';

import express from 'express';
import formidable from 'formidable';
import socketIOClient from 'socket.io-client';

const port = 8002;
const eIp = process.env["DASHBOARD_LOAD_BALANCER_SERVICE_HOST"];
const ePort = process.env["DASHBOARD_LOAD_BALANCER_SERVICE_PORT"];
console.log(ePort, eIp);
var app = express();
app.use(express.json({ limit: '50mb' }));
var socket = socketIOClient.connect(`http://${eIp}:${ePort}`, {
    transports: ['websocket'], maxHttpBufferSize: 1e8
});
socket.on('connect', function () { console.log("socket connected"); });
socket.on("disconnect", () => {
    console.log("Disconnect");
});
socket.on("connect_error", (err) => {
    console.log(`connect_error due to ${err.message}`);
});
socket.on('error', function (err) {
    console.log(`error due to ${err.message}`);
});
socket.on('httpRequestReceived', (data) => {
    console.log('Response received');
});

/**
 * The form served by this route handler can be used for testing the ML model only.
 */

// app.get("/", (req, res) => {
//     res.send(`
//     <h2>With <code>"express"</code> npm package</h2>
//     <form action="/crowdy/image/count" enctype="multipart/form-data" method="post">
//       <div>Text field title: <input type="text" name="title" /></div>
//       <div>File: <input type="file" name="imageFileField" multiple="multiple" /></div>
//       <input type="submit" value="Upload" />
//     </form>
//   `);
// });

/** 
 * The handler in this path will do the head counting. 
 * The response of the handler is a JSON object with the following structure
 * 
 * { imageId: <image-id-based of the name given in the request>, count: <number of people found in the picture> }
 */

function base64_encode(file) {
    var bitmap = fs.readFileSync(file);
    return new Buffer.from(bitmap).toString('base64');
}

app.post("/crowdy/image/count", async (req, res, next) => {
    console.log("Counting heads");
    const formData = formidable({});
    formData.parse(req, async (error, incomingFields, incomingFiles) => {
        if (error) {
            next(error);
        } else {
            let camera_id = incomingFields['camera_id'][0];
            let file = incomingFiles.imageFileField[0];
            const count = await countHeads(file.filepath);
            res.json({ imageId: file["originalFilename"], count });
            console.log(`Counted [${count}] heads in [${file["newFilename"]}]`);
            socket.emit('setData', {
                "counter": count,
                "camera_id": camera_id,
                "base-64_img": base64_encode(file.filepath)
            });
            console.log("Message emitted");
        }
    })
})

app.listen(port, () => {
    console.log(`Head counting server running on port ${port}`)
})

async function countHeads(filepath) {
    const imageBuffer = loadImageFromDisk(filepath);
    const tensorImage = tf.node.decodeImage(imageBuffer);
    const model = await cocoSsd.load();
    const predictions = await model.detect(tensorImage);
    const count = predictions.filter(pred => pred.class === "person").length;
    return count;
}


function loadImageFromDisk(path) {
    return fs.readFileSync(path);
}
