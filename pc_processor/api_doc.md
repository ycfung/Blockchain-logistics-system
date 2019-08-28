# api_doc

本文档将介绍事务族pacel_chain相关信息,根据这些信息使用sawtooth提供的接口,可以完成生成交易和查询相关信息的client

## 1.information of Transaction Family

Family name = 'pacel_chain'
version = '1.0'


## 2.name space and adress

在sawtooth中，gobal state的地址由70位组成

在本事务族中，address的前六位表示交易族的名称空间，七到十位表示state的类型（如：用户state，包裹state），剩下的60位根据state所属用户或者单号等具体情况决定

交易族名称空间
PC_NAMESPACE = hashlib.sha512('pacel_chain'.encode("utf-8")).hexdigest()[0:6]

- 用户state地址组成

        USER_NAMEPCACE = hashlib.sha512('user_state'.encode("utf-8")).hexdigest()[0:4] 
        adress  =  PC_NAMESPACE + USER_NAMEPCACE + public_key[-60:]

- 订单state地址组成

        ODER_NAMESPACE = hashlib.sha512('oder_state'.encode("utf-8")).hexdigest()[0:4]
        adress = PC_NAMESPACE + ODER_NAMESPACE + hashlib.sha512(oder_number.encode("utf-8")).hexdigest()[-60:]

## 3.content of state

- 用户state

用户state由余额和电话号码组成，使用  ',' 分隔

- 订单state由单号（string），发起人公钥，接受人公钥，驿站地址，收货地址，取货号，金额，订单状态组成，使用  ',' 分隔

## 4.transaction and its payload

transaction中由使用者进行签名，主要关注payload和input，output的内容，payload表明该事务的类型和相关数据，input和output表明该交易可读写的address

payload由action和data两部分内容组成，使用 '|‘ 进行分隔，之后进行encode，action代表该事务的类型


下面是各种类型交易所需的data和input，output（下面的input和output表示的是由这些用户的公钥或者货号生成的address所组成的数组，signer指的是发起该交易的用户）


#### action = 'sign up'

注册，注册后余额为0

data ： phone number（str）

input ：signer

output ：signer


#### action = 'init'

注册初始账户，初始账户可以获得100000000余额

data ： 无

input ：signer

output ： signer


#### action = 'transfer'

转账

data ：address of accepter ， count （用逗号分隔）

input ：signer，accepter

output ： signer ，accepter


#### action = 'apply'

申请订单

data : 单号，驿站，收货地址，货号，金额

input：signer ，订单

output：  signer ，订单

#### action = 'accept'


接受订单

data : 单号

input ：signer ，订单

output ：signer ， 订单


#### action = 'fetch'


取货

data : 单号

input :  signer, 订单

output : signer , 订单


#### action = 'completed'

由订单的发起人确认订单的完成

data：  单号

intput：signer，acceptor ，订单

output：signer ， acceptor ， 订单
