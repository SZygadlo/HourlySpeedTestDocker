#!/bin/sh
touch $HOME/Results.csv
sudo docker run --volume $HOME/.config/ookla/speedtest-cli.json:/root/.config/ookla/speedtest-cli.json --volume $HOME/Results.csv:/sp/Data.csv --restart no -d --name sp sp