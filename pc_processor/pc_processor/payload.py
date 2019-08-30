

from sawtooth_sdk.processor.exceptions import InvalidTransaction


class PCPayload:

    def __init__(self,payload):
        try:
            self.action,self.data = payload.decode().split("|")
        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        # check the format

        if self.action not in ('init','sign_up','add_pacel','apply','accept','cancel','completed','fetch','transfer'):
            raise InvalidTransaction('Invalid action: {}'.format(self.action))

    @staticmethod
    def from_bytes(payload):
        return PCPayload(payload=payload)

class SignupData:
    def __init__(self,data):
        self.phone_number = data


class ApplyData:

    def __init__(self,data):
        print(data)
        a =data
        try:
            self.order_number,self.station,self.destination,self.pacel_number,coin_str = data.split(",")
            self.coin = int(coin_str)
        except ValueError:
            raise InvalidTransaction("Invalid apply data serialization")

class AcceptData:

    def __init__(self, data):
        self.order_number = data

class CancelData:

    def __init__(self, data):
        self.order_number = data

class CompletedData:

    def __init__(self, data):
        self.order_number = data


class FetchData:

    def __init__(self, data):
        self.order_number = data
'''
        f_data = data
        try:
            self.order_number, self.check_code= f_data.split(",")
        except ValueError:
            raise InvalidTransaction("Invalid transfer fetch serialization")
'''

class TransferData:

    def __init__(self, data):
        t_data = data
        try:
            self.another_user, count_str = t_data.split(",")
            self.count = int(count_str)
        except ValueError:
            raise InvalidTransaction("Invalid transfer data serialization")