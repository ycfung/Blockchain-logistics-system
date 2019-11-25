from client import *
import json


u01 = Client('http://localhost:8008','/root/.sawtooth/keys/u01.priv')
u02 = Client('http://localhost:8008','/root/.sawtooth/keys/u02.priv')
root = Client('http://localhost:8008','/root/.sawtooth/keys/root.priv')
s01 = Client('http://localhost:8008','/root/.sawtooth/keys/s01.priv')

root_pub = '037d80e02eaa62373961510e1691c6b986d31ed7c9d1dea05be562ef5f773edf3f'
u01_pub = '02897f17d3d6f0ba1feafb9e28c26a78e883e2df10ca33898dc7f87c2442678239'
u02_pub = '02578bdf3129a20403071afd1161385f224d028a4f4fe7736285b99633a8691d29'
s01_pub = '039cdbd9c35f2e668375c9eab2df59fd0335d8ad6ee1b0f12192109317c3b36e7c'

# 创建管理员
root.send_txn(json.dumps({'action':'init'}).encode(),setting = True)

# 用户注册（用户余额为0）
u01.send_txn(json.dumps({'action':'sign_up','mobile':'13160606060'}).encode())
u02.send_txn(json.dumps({'action':'sign_up','mobile':'13160606070'}).encode())

# 管理员向用户转账
root.send_txn(json.dumps({'action':'transfer','coin':100,'acceptor':u01_pub}).encode(),anotherUser=u01_pub)

# 管理员为某个驿站设置一个管理员，管理员可以入库包裹
root.send_txn(json.dumps({'action':'authorize','pub_key':s01_pub,'station':'beiyuan'}).encode(),
                setting = True,station = 'beiyuan')

# 管理员入库包裹
s01.send_txn(json.dumps({'action':'warehouse','station':'beiyuan','pacels':
            [{'mobile':'13160606060','order_number':'001','pacel_number':'10-10-10'},
                {'mobile':'13160606070','order_number':'002','pacel_number':'10-10-11'}]}).encode()
             ,station='beiyuan',order_numbers=['001','002'],mobiles=['13160606060','13160606070'])

# 直接取走入库的包裹
u02.send_txn(json.dumps({'action':'fetch', 'order_number':'002'}).encode(),order_numbers=['002'],mobiles=['13160606070'])

# 将已经入库的包裹发起委托
u01.send_txn(json.dumps({'action':'apply','order_number':'001','coin':20,'destination':'nanyuan'}).encode()
                                       ,order_numbers = ['001'],mobiles=['13160606060'])

# 接受委托
u02.send_txn(json.dumps({'action':'accept','order_number':'001'}).encode(),order_numbers=['001'],mobiles=['13160606070'])

# 取走委托的包裹
u02.send_txn(json.dumps({'action':'fetch','order_number':'001'}).encode(),order_numbers=['001'])

# 确认委托完成
u01.send_txn(json.dumps({'action':'confirm','order_number':'001'}).encode(),order_numbers=['001'],anotherUser=u02_pub,
                mobiles=['13160606060'])


