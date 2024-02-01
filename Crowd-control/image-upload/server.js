import express from 'express';

const port = 8003;
const app = express();

const eIp = 'localhost';
const ePort = 8002;
// const eIp = process.env["IMAGE_PREDICT_LOAD_BALANCER_SERVICE_HOST"];
// const ePort = process.env["IMAGE_PREDICT_LOAD_BALANCER_SERVICE_PORT"];
console.log(ePort, eIp);

app.get("/", (req, res) => {
  console.log("Sending the image to a counting service");
  res.send(`
    <h2>Image uploading service</h2>
    <form action="http://${eIp}:${ePort}/crowdy/image/count" enctype="multipart/form-data" method="post">
      <div>Camera ID: <input type="integer" name="camera_id" /></div>
      <div>Photo: <input type="file" name="imageFileField" multiple="multiple" /></div>
      <input type="submit" value="Upload" />
    </form>
  `);
});

app.listen(port, () => {
  console.log(`Image uploading server running on port ${port}`)
})
