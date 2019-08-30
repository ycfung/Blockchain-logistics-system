from client import *


u01 = Client('http://localhost:8008','/root/.sawtooth/keys/u01.priv')
root = Client('http://localhost:8008','/root/.sawtooth/keys/root.priv')

root.send_txn('init|'.encode())