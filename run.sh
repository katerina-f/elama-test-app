#!/bin/bash
source venv/bin/activate

cd test_app.db || exit

docker-compose up -d
sleep 3

cd ..

cd test_app.mq || exit

docker-compose up -d

sleep 3

cd ..

systemctl start runserver.service
