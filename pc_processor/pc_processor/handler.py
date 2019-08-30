

import logging


from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError


from pc_processor.state import User
from pc_processor.state import Order
from pc_processor.state import UserState
from pc_processor.state import OrderState
from pc_processor.state import PC_NAMESPACE

from pc_processor.payload import *

LOGGER = logging.getLogger(__name__)


class PCTransactionHandler(TransactionHandler):

    @property
    def family_name(self):
        return 'pacel_chain'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [PC_NAMESPACE]

    def apply(self, transaction, context):

        LOGGER.info('try to apply an transaction')

        header = transaction.header
        signer = header.signer_public_key
        pc_payload = PCPayload.from_bytes(transaction.payload)

        if pc_payload.action == 'sign_up':

            LOGGER.info("sign_up")
            user_state = UserState(context)

            signup_data = SignupData(pc_payload.data)
            newuser = User(0, signup_data.phone_number)


            if user_state.get_state(signer) is not None:
                raise InvalidTransaction("user exist")

            user_state.set_state(signer,newuser)
            #change the config state
            #log init finish
            LOGGER.info("sign up finish")

        elif pc_payload.action == 'init':


            LOGGER.info("init")
            user_state = UserState(context)
            administator = User(10000000,'00000000000')

            user_state.set_state(signer,administator)
            #change the config state
            #log init finish
            LOGGER.info("init finished")


        elif pc_payload.action == 'apply':

            LOGGER.info('apply')
            apply_data = ApplyData(pc_payload.data)

            #check balance
            user_state = UserState(context)
            initiator = user_state.get_state(signer)

            #pay for order
            if initiator.coin < apply_data.coin:
                raise InvalidTransaction("balance not enough")
            else:
                initiator.coin -= apply_data.coin
                user_state.set_state(signer,initiator)

            #create new order
            order_state = OrderState(context)
            if order_state.get_order(apply_data.order_number) is not None:
                raise InvalidTransaction("order has been existed")
            else:
                order_state.create_order(apply_data.order_number,signer,'',apply_data.station,apply_data.destination,
                                      apply_data.pacel_number,apply_data.coin)

            LOGGER.info('apply finish')


        elif pc_payload.action == 'accept':

            LOGGER.info('accept')
            accept_data = AcceptData(pc_payload.data)

            order_state = OrderState(context)
            order = order_state.get_order(accept_data.order_number)
            if order is None:
                raise InvalidTransaction("order not exist")
            else:
                order.state = 'accepted'
                order.acceptor = signer
                order_state.set_order(order)

            LOGGER.info('accept finish')

        elif pc_payload.action == 'cancel':

            LOGGER.info('cancel')
            cancel_data = CancelData(pc_payload.data)
            user_state = UserState(context)

            initiator = user_state.get_state(signer)

            order_state = OrderState(context)
            order = order_state.get_order(cancel_data.order_number)
            if order  is None:
                raise InvalidTransaction("order not exist")
            elif order.initiator!= signer:
                raise InvalidTransaction("unauthorized")
            elif order.state != 'apply':
                raise InvalidTransaction("order could not be accepted")
            else:
                order.state = 'canceled'
                initiator.coin += order.coin
                user_state.set_state(signer,initiator)
                order_state.set_order(order)

            LOGGER.info('cancel finish')


        elif pc_payload.action == 'fetch':

            LOGGER.info('fetch')
            fetch_data = FetchData(pc_payload.data)

            order_state = OrderState(context)
            order = order_state.get_order(fetch_data.order_number)

            if order is None:
                raise InvalidTransaction("order not exist")
            # check the authority
            if signer != order.acceptor:
                raise InvalidTransaction("unauthorized")
            elif order.state != 'accepted':
                raise InvalidTransaction("order could not be fetched")

            order.state = 'fetched'
            # log succeed
            order_state.set_order(order)

            LOGGER.info('fetch finish')

        elif pc_payload.action == 'completed':

            LOGGER.info('completed')
            completed_data = CompletedData(pc_payload.data)

            order_state = OrderState(context)
            order = order_state.get_order(completed_data.order_number)

            if order is None:
                raise InvalidTransaction("unauthorized")
            if signer!= order.initiator:
                raise InvalidTransaction("unauthorized")
            if order.state != 'fetched':
                raise InvalidTransaction("order could not be completed")

            order.state = 'completed'
            order_state.set_order(order)
            #recevie the coin
            user_state = UserState(context)
            acceptor = user_state.get_state(order.acceptor)
            acceptor.coin += order.coin
            user_state.set_state(order.acceptor,acceptor)
            LOGGER.info('completed finish ')


        elif pc_payload.action == 'transfer':


            LOGGER.info('transfer')
            transfer_data = TransferData(pc_payload.data)

            user_state = UserState(context)
            user = user_state.get_state(signer)
            another_user = user_state.get_state(transfer_data.another_user)

            user.coin -= transfer_data.count
            if(user.coin<0):
                raise InvalidTransaction("balance not enough")
            another_user.coin += transfer_data.count

            user_state.set_state(signer,user)
            user_state.set_state(transfer_data.another_user,another_user)

            LOGGER.info('transfer finish')
