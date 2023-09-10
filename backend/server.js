import DataHandler from './data_handler.js';
import Reader from './reader.js';
import express from 'express';
import bodyParser from 'body-parser';

const app = express()
const port = 3080;

const dh = new DataHandler();
const rd = new Reader();

app.use(express.static('../dist/'));

app.use(bodyParser.json());

app.get('/api/card', async (req, res) => {
  const uid = await rd.run();
  res.json(uid);
});

app.get('/api/cardstop', async (req, res) => {
  await rd.stop();
  res.json("Stopped")
});

app.get('/api/exists', async (req, res) => {
  const uid = req.query.uid;
  console.log(`Existing user ${uid}?`)
  const exists = await dh.exists(uid);
  res.json(`${exists}`);
});

app.get('/api/user', async (req, res) => {
  const uid = req.query.uid;
  console.log(`Fetching user ${uid}`)
  const user = await dh.getUser(uid);
  res.json(user)
});

app.post('/api/adduser', async (req, res) => {
  const uid = req.body.uid;
  const data = req.body.data;
  console.log(`Adding user ${uid}`)
  await dh.addUser(uid, data);
  res.json("User added!");
});

app.post('/api/updateuser', async (req, res) => {
  const uid = req.body.uid;
  const data = req.body.data;
  console.log(`Updating user ${uid}`)
  await dh.updateUser(uid, data);
  res.json("User updated!");
});

app.listen(port, () => {
  console.log(`Server listening on the port::${port}`);
});
