#!/bin/bash

git clone https://github.com/MobbareKurtZ/zkkscore.git

npm install

npm run build

pm2 restart zkkscore

cd backend/

pip install -r requirements.txt
