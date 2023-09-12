#!/bin/bash

git pull

npm install

npm run build

cd backend/

pip install -r requirements.txt

pm2 restart zkkscore
