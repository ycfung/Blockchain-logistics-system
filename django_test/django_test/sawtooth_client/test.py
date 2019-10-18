from django_test.sawtooth_client.view import *
from django_test.sawtooth_client.features import *
import hashlib

PC_NAMESPACE = hashlib.sha512('pacel_chain'.encode("utf-8")).hexdigest()[0:6]
USER_NAMESPACE = hashlib.sha512('user_state'.encode("utf-8")).hexdigest()[0:4]
ODER_NAMESPACE = hashlib.sha512('oder_state'.encode("utf-8")).hexdigest()[0:4]

CONFIG_ADDRESS = PC_NAMESPACE

rest_api_addr = "http://127.0.0.1:8008"


def make_user_address(public_key):
    return PC_NAMESPACE + USER_NAMESPACE + public_key[-60:]


def make_order_address(oder_number):
    return PC_NAMESPACE + ODER_NAMESPACE + hashlib.sha512(oder_number.encode("utf-8")).hexdigest()[-60:]


def make_station_address(station):
    return PC_NAMESPACE + hashlib.sha512(station.encode('utf-8')).hexdigest()[-64:]


def make_mobile_address(mobile):
    return PC_NAMESPACE + hashlib.sha512(mobile.encode('utf-8')).hexdigest()[-64:]


SETTING_ADDRESS = PC_NAMESPACE + "0000000000000000000000000000000000000000000000000000000000000000"

root = Client(rest_api_addr, pri_key_str="e8e8fd3e759b5cfd252c142f2c3d8526e32de612d42677933d9a255ec78298ec")
client1 = Client(rest_api_addr, pri_key_str="77729b8c6c50dcc19e9c56263fdfc9f0224677ecd2709dc821ad603be2613b1c")
client2 = Client(rest_api_addr, pri_key_str="1a87897c4be8ea07d5b7a125211dacfdd4321050d2b3cf060fa54eef01461622")
client3 = Client(rest_api_addr, pri_key_str='5444b6010f181c198a490b8e07f3ac26d50ffb6046fffebb64d3d3542b1bcee3')


class method:

    # 普通用户注册
    def sign_up(mobile, key):
        if (key is None):
            temp_client = Client(rest_api_addr, pri_key_str=gen_random_key_str())
        else:
            temp_client = Client(rest_api_addr, pri_key_str=key)
        temp_client.send_txn(json.dumps({'action': 'sign_up', 'mobile': mobile}).encode())

    # root用户给普通用户转账
    def initial_transfer(amount, pub_key):
        root.send_txn(json.dumps({'action': 'transfer', 'coin': amount, 'acceptor': pub_key}).encode(),
                      anotherUser=pub_key)

    # root用户授权驿站管理员
    def authorize(pub_key, station):
        root.send_txn(json.dumps({'action': 'authorize', 'pub_key': pub_key, 'station': station}).encode(),
                      setting=True, station=station)

    # 驿站管理员入库包裹
    def register_package(admin_private_key, station, mobile, order_number, parcel_number):
        admin = Client(rest_api_addr,
                       pri_key_str=admin_private_key)
        admin.send_txn(json.dumps({'action': 'warehouse', 'station': station, 'pacels':
            [{'mobile': mobile, 'order_number': order_number, 'pacel_number': parcel_number}]}).encode()
                       , station=station, order_numbers=[order_number], mobiles=[mobile])

    # 直接取走包裹
    def fetch_package(user_private_key, order_number, mobile):
        user = Client(rest_api_addr, pri_key_str=user_private_key)
        user.send_txn(json.dumps({'action': 'fetch', 'order_number': order_number}).encode(),
                      order_numbers=[order_number],
                      mobiles=[mobile])

    # 已入库的包裹发起新委托
    def new_request(user_private_key, order_number, coin, destination, mobile):
        user = Client(rest_api_addr, pri_key_str=user_private_key)
        user.send_txn(
            json.dumps(
                {'action': 'apply', 'order_number': order_number, 'coin': coin, 'destination': destination}).encode()
            , order_numbers=[order_number], mobiles=[mobile])

    # 接受委托
    def accept_request(user_private_key, order_number, mobile):
        user = Client(rest_api_addr, pri_key_str=user_private_key)
        user.send_txn(json.dumps({'action': 'accept', 'order_number': order_number}).encode(),
                      order_numbers=[order_number],
                      mobiles=[mobile])

    # 取走委托的包裹
    def fetch_request_package(user_private_key, order_number):
        user = Client(rest_api_addr, pri_key_str=user_private_key)
        user.send_txn(json.dumps({'action': 'fetch', 'order_number': order_number}).encode(),
                      order_numbers=[order_number])

    # 确认委托完成
    def confirm_request(self, user_private_key, order_number, recipient_public_key, mobile):
        user = Client(rest_api_addr, pri_key_str=user_private_key)
        user.send_txn(json.dumps({'action': 'confirm', 'order_number': order_number}).encode(),
                      order_numbers=[order_number],
                      anotherUser=recipient_public_key,
                      mobiles=[mobile])

    # 以下方法属于 GET 方法

    # 产生随机私钥
    def get_random_key(self):
        d = {}
        d['random_key'] = gen_random_key_str()
        return str(d)

    # 将私钥转为公钥
    def get_public_key(private_key_str):
        user = Client(rest_api_addr, pri_key_str=private_key_str)
        d = {}
        d['public_key'] = user.public_key
        return str(d)

    # 获取用户个人信息
    def get_user_info(user_private_key):
        try:
            user = Client(rest_api_addr, pri_key_str=user_private_key)
            vc = ViewConditions(rest_api_addr)
            state = vc.getState(make_user_address(user.public_key))
            return state
        except RequestError as err:
            return err.status

    # 通过手机号获取交易状态
    def get_transaction_condition(mobile):
        try:
            vc = ViewConditions(rest_api_addr)
            state = vc.getState(make_mobile_address(mobile))
            return state
        except RequestError as err:
            return err.status

    # 通过单号查询交易状态
    def get_order_status(order_number):
        try:
            vc = ViewConditions(rest_api_addr)
            state = vc.getState(make_order_address(order_number))
            return state
        except RequestError as err:
            return err.status


if __name__ == '__main__':
    print(method.get_public_key('e8e8fd3e759b5cfd252c142f2c3d8526e32de612d42677933d9a255ec78298ec'))
