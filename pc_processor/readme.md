# About pc_processor

pc_processor 是本项目的交易处理器部分

api文档见 [api_doc.md](https://github.com/ycfung/bc-package/blob/master/pc_processor/api_doc.md)


## 组成

#### client.py以及test_cli.py是用于测试的简易脚本

client.py提供简易的发送交易的函数

test.cli.py是一个使用示例

#### pc_processor是处理器的组成部分

handler.py用于交易的逻辑处理

state.py用于处理gobal_state的地址,转换地址内容

payload.py用于转换交易的payload


## 使用方法

在ubuntu上初始化(密钥,初始块生成等)并启动sawtooth(包括validator,rest-api,setting-tp,devmode-engine-rust)

运行main.py脚本

## 已知问题

  1. 可以多次使用init交易(之后会引入设置state或者通过创世块解决)
 
  2. 错误的payload格式可能会导致验证器崩溃(崩溃解决方案:ctrl+c停止validator,main.py,devmode-engine-rust) 
  
  
## 暂不支持的功能

 1. 设置文件(即将加入)

 2. 数据库,货物入库等
 
