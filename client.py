from base64 import b64encode
import time
import random
import requests
import yaml

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

from django_test.sawtooth_client.state import *


def _sha512(data):
    return hashlib.sha512(data).hexdigest()


class Client:
    def __init__(self, base_url, pri_key_str=None):

        self._base_url = base_url

        if pri_key_str is None:
            self._signer = None
            return

        try:
            self.private_key_str = pri_key_str
        except OSError as err:
            raise Exception(
                'Failed to read private key {}: {}'.format(
                    pri_key_str, str(err)))

        try:
            private_key = Secp256k1PrivateKey.from_hex(self.private_key_str)
        except ParseError as e:
            raise Exception(
                'Unable to load private key: {}'.format(str(e)))

        self._signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_key)

        self.public_key = self._signer.get_public_key().as_hex()


    def _get_status(self, batch_id, wait, auth_user=None, auth_password=None):
        try:
            result = self._send_request(
                'batch_statuses?id={}&wait={}'.format(batch_id, wait),
                auth_user=auth_user,
                auth_password=auth_password)
            return yaml.safe_load(result)['data'][0]['status']
        except BaseException as err:
            raise Exception(err)

    def _send_request(self,
                      suffix,
                      data=None,
                      content_type=None,
                      name=None,
                      auth_user=None,
                      auth_password=None):
        if self._base_url.startswith("http://"):
            url = "{}/{}".format(self._base_url, suffix)
        else:
            url = "http://{}/{}".format(self._base_url, suffix)

        headers = {}
        if auth_user is not None:
            auth_string = "{}:{}".format(auth_user, auth_password)
            b64_string = b64encode(auth_string.encode()).decode()
            auth_header = 'Basic {}'.format(b64_string)
            headers['Authorization'] = auth_header

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if result.status_code == 404:
                raise Exception("No such game: {}".format(name))

            if not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise Exception(err)

        return result.text

    def send_txn(self,
                 payload,
                 order_numbers=None,
                 anotherUser=None,
                 setting=False,
                 station=None,
                 mobiles=None,
                 wait=None,
                 auth_user=None,
                 auth_password=None):
        # Serialization is just a delimited utf-8 encoded string

        # Construct the address

        change_adress = [make_user_address(self._signer.get_public_key().as_hex())]

        if order_numbers is not None:
            for o in order_numbers:
                change_adress.append(make_oder_address(o))
        if anotherUser is not None:
            change_adress.append(make_user_address(anotherUser))
        if setting:
            change_adress.append(SETTING_ADDRESS)
        if station is not None:
            change_adress.append(make_station_adress(station))
            print(make_station_adress(station))
        if mobiles is not None:
            for m in mobiles:
                change_adress.append(make_mobile_adress(m))

        header = TransactionHeader(
            signer_public_key=self._signer.get_public_key().as_hex(),
            family_name="pacel_chain",
            family_version="1.0",
            inputs=change_adress,
            outputs=change_adress,
            dependencies=[],
            payload_sha512=_sha512(payload),
            batcher_public_key=self._signer.get_public_key().as_hex(),
            nonce=hex(random.randint(0, 2 ** 64))
        ).SerializeToString()

        signature = self._signer.sign(header)

        transaction = Transaction(
            header=header,
            payload=payload,
            header_signature=signature
        )

        batch_list = self._create_batch_list([transaction])
        batch_id = batch_list.batches[0].header_signature

        if wait and wait > 0:
            wait_time = 0
            start_time = time.time()
            response = self._send_request(
                "batches", batch_list.SerializeToString(),
                'application/octet-stream',
                auth_user=auth_user,
                auth_password=auth_password)
            while wait_time < wait:
                status = self._get_status(
                    batch_id,
                    wait - int(wait_time),
                    auth_user=auth_user,
                    auth_password=auth_password)
                wait_time = time.time() - start_time

                if status != 'PENDING':
                    return response

            return response

        return self._send_request(
            "batches", batch_list.SerializeToString(),
            'application/octet-stream',
            auth_user=auth_user,
            auth_password=auth_password)

    def _create_batch_list(self, transactions):
        transaction_signatures = [t.header_signature for t in transactions]

        header = BatchHeader(
            signer_public_key=self._signer.get_public_key().as_hex(),
            transaction_ids=transaction_signatures
        ).SerializeToString()

        signature = self._signer.sign(header)

        batch = Batch(
            header=header,
            transactions=transactions,
            header_signature=signature)
        return BatchList(batches=[batch])
