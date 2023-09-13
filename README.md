# zkkscore

## Project Setup

Clone, cd into root and then
```sh
npm install
cd backend && pip install -r requirements.txt
```

### Build

(from root, not in backend/)
```sh
npm run build
```

### Run
```sh
python3 backend/server.js
```
On the Raspberry PI you can run
```sh
pm2 <start/restart/stop> zkkscore
```
 to handle the backend.

### Redeploy on Raspberry PI
A redeploy runs every morning at 7:00 can also be triggered by running
```sh
./redeploy.sh
```
or running konami code on the keypad (up up down down left right left right).
