#!/bin/sh
sudo -u sawtooth sawtooth-validator -vv &
sudo -u sawtooth devmode-engine-rust -vv --connect tcp://localhost:5050 &
sudo -u sawtooth sawtooth-rest-api -B 0.0.0.0:8008 -v &
sudo -u sawtooth settings-tp -v & 
