#!/bin/bash

echo "Clone repo project into /home/candyshop/soft/ ..."
sudo mkdir /home/entrant/candyshop
cd /home/entrant/candyshop/
git clone https://www.github.com/fenixguard/candyshop_api.git
echo "Done!"

echo "Coping config file..."
cp /home/candyshop/soft/candyshop_api/candyshop.service /etc/systemd/system/
echo "Done!"

echo "Reloading daemon..."
systemctl daemon-reload
echo "Daemon reloaded!"

echo "Starting service..."
systemctl start candyshop
echo "Service started on 0.0.0.0:8080 "