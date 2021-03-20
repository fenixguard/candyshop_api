#!/bin/bash

echo "Clone repo project into /home/entrant/soft ..."
sudo mkdir /home/entrant/soft
cd /home/entrant/soft/
git clone https://www.github.com/fenixguard/candyshop_api.git
echo "Done!"

echo "Coping config file..."
cp /home/entrant/soft/candyshop_api/candyshop.service /etc/systemd/system/
echo "Done!"

echo "Reloading daemon..."
systemctl daemon-reload
echo "Daemon reloaded!"

echo "Starting service..."
systemctl start candyshop
echo "Service started on 0.0.0.0:8080 "