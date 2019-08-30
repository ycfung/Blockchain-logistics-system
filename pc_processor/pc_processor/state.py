import hashlib

from sawtooth_sdk.processor.exceptions import InternalError


PC_NAMESPACE = hashlib.sha512('pacel_chain'.encode("utf-8")).hexdigest()[0:6]

USER_NAMEPCACE = hashlib.sha512('user_state'.encode("utf-8")).hexdigest()[0:4]
ODER_NAMESPACE = hashlib.sha512('oder_state'.encode("utf-8")).hexdigest()[0:4]

CONFIG_ADDRESS = PC_NAMESPACE

def make_user_address(public_key):
    return PC_NAMESPACE + USER_NAMEPCACE + public_key[-60:]

def make_oder_address(oder_number):
    return PC_NAMESPACE + ODER_NAMESPACE + hashlib.sha512(oder_number.encode("utf-8")).hexdigest()[-60:]



class User:

    def __init__(self,coins,mobile):
        self.coin = coins
        self.mobile = mobile


class UserState:

    def __init__(self, contest):
        self._context  = contest
        self.TIMEOUT = 3
        self._address_cache = {}


    def get_state(self,public_key):

        address = make_user_address(public_key)

        if address in self._address_cache:
            data = self._address_cache[address]
        else:
            datas = self._context.get_state([address])
            if datas:
                data = datas[0].data
            else:
                return None

        coins_str,mobile = data.decode().split(',')
        coins = int(coins_str)
        return User(coins,mobile)


    def set_state(self,public_key,user):
        address = make_user_address(public_key)
        data = (str(user.coin)+','+str(user.mobile)).encode()
        self._address_cache[address] = data
        self._context.set_state({address:data},timeout = self.TIMEOUT)



class Order:

    def __init__(self,order_number,initiator,accepter,station,destination,pacel_number,coin,state):
        self.order_number = order_number
        self.initiator = initiator
        self.acceptor = accepter
        self.station = station
        self.destination = destination
        self.pacel_number = pacel_number
        self.coin = coin
        self.state = state


class OrderState:


    def __init__(self,contest):
        self._contest = contest
        self.TIMEOUT = 3

        self._address_cache = {}


    def create_order(self,order_number, initiator,accepter,station,destination,pacel_number,coin):
        order = Order(order_number, initiator,accepter,station,destination,pacel_number,coin,'apply')
        self.set_order(order)


    def set_order(self, order):
        address = make_oder_address(order.order_number)

        data = self._serialize(order)
        self._address_cache[address] = data
        self._contest.set_state({address:data},timeout = self.TIMEOUT)


    def get_order(self,order_number):
        address = make_oder_address(order_number)
        if address in self._address_cache:
            order = self._deserialize( self._address_cache[address] )
            return order
        else:
            serialize_orders = self._contest.get_state([address],timeout = self.TIMEOUT)
            if serialize_orders:
                serialize_order = serialize_orders[0].data
                order = self._deserialize(serialize_order)
                return order
            else:
                return None

    def delete_order(self,order_number):
        address = make_oder_address(order_number)
        if self._address_cache[address]:
            del self._address_cache[address]

        self._contest.delete_state([address],timeout = self.TIMEOUT)




    def _deserialize(self,data):
        order_str = data.decode()
        order_number,initiator,accepter,station,destination,pacel_number,coin,state = order_str.split(",")
        return Order(order_number,initiator,accepter,station,destination,pacel_number,int(coin),state)

    def _serialize(self,order):
        order_str = ",".join([order.order_number,order.initiator,order.acceptor,order.station,order.destination,
                              order.pacel_number,str(order.coin),order.state])
        return order_str.encode()

