

import logging


from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

import json

from pc_processor.state import *

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

        try:
            pc_payload = json.loads(transaction.payload.decode())

            print(pc_payload['action'])

            if pc_payload['action'] == 'warehouse':

                LOGGER.info("warehouse")
                station = pc_payload['station']
                pacels = pc_payload['pacels']

                if not StationState(context).check_authority(station,signer):
                    raise InvalidTransaction('unauthority')

                mobile_state = MobileState(context)
                order_state = OrderState(context)
                for p in pacels:
                    mobile_state.add_order(p['mobile'],[p['order_number']])
                    order_state.create_order(p['order_number'],station,p['pacel_number'])

            elif pc_payload['action'] == 'sign_up':
                LOGGER.info("sign_up")
                user_state = UserState(context)

                if user_state.get_state(signer) is not None:
                    raise InvalidTransaction('user exist')

                user_state.set_state(signer,0,pc_payload['mobile'])

                LOGGER.info('sign up finished')

            elif pc_payload['action'] == 'init':


                LOGGER.info("init")

                setting_state = SettingState(context)
                user_state = UserState(context)

                if setting_state.get_admin_key() is not None:
                    raise InvalidTransaction("admin has benn register")
                else:
                    setting_state.set_inited_key(signer)

                user_state.set_state(signer,100000000,'000000000')

                LOGGER.info("init finished")

            elif pc_payload['action'] == 'apply':

                LOGGER.info('apply')

                order_number = pc_payload['order_number']
                coin = pc_payload['coin']
                destination = pc_payload['destination']


                user_state = UserState(context)
                order_state = OrderState(context)
                mobile_state = MobileState(context)

                user = user_state.get_state(signer)
                if user is None:
                    raise InvalidTransaction("user not register")

                if user['coin']-coin < 0:
                    raise InvalidTransaction('coin not enough')
                else:
                    user_state.subtract_coin(signer,coin)

                mobile = user['mobile']

                pacels_of_mobile = mobile_state.get_state(mobile)
                if order_number not in pacels_of_mobile['order_number']:
                    raise InvalidTransaction("not such order")

                if not order_state.apply_order(order_number,coin,destination):
                    raise InvalidTransaction('could not apply order')


                LOGGER.info('apply finished')

            elif pc_payload['action'] == 'accept':

                LOGGER.info('accept')

                order_state = OrderState(context)

                if not order_state.accept_order(pc_payload['order_number'],signer):
                    raise InvalidTransaction('could accept order')

                user_state = UserState(context)
                user = user_state.get_state(signer)
                mobile_state = MobileState(context)
                mobile_state.add_accepted_order(user['mobile'],[pc_payload['order_number']])

                LOGGER.info('accept finish')

            elif pc_payload['action'] == 'fetch':
                LOGGER.info('fetch')

                order_number = pc_payload['order_number']

                order_state = OrderState(context)
                order = order_state.get_order(order_number)

                if order is None:
                    raise InvalidTransaction("order not exist")
                # check the authority
                if order['state'] == 'init':
                    user_state = UserState(context)
                    user = user_state.get_state(signer)
                    mobile_state = MobileState(context)
                    order_of_user = mobile_state.get_state(user['mobile'])


                    if order_number in order_of_user['order_number']:
                        order_state.set_order_state(order_number,'completed')
                    else:
                        raise InvalidTransaction('unauthorized')
                elif order['state'] == 'accepted':
                    if signer == order['acceptor']:
                        order_state.set_order_state(order_number,'fetched')
                    else:
                        raise InvalidTransaction('unauthorized')
                else:
                    raise InvalidTransaction('could not fetch order')

                LOGGER.info('fetch finish')

            elif pc_payload['action'] == 'confirm':

                LOGGER.info('confirm')
                order_state = OrderState(context)
                order_number = pc_payload['order_number']

                order = order_state.get_order(order_number)

                if order is None:
                    raise InvalidTransaction("unauthorized")

                user_state = UserState(context)
                user = user_state.get_state(signer)
                mobile_state = MobileState(context)
                order_of_user = mobile_state.get_state(user['mobile'])

                if order_number not in order_of_user['order_number']:
                    raise InvalidTransaction("unauthorized")
                if order['state'] != 'fetched':
                    raise InvalidTransaction("order could not be completed")

                order_state.set_order_state(order_number,'completed')

                # receive the coin
                user_state = UserState(context)
                user_state.add_coin(order['acceptor'],order['coin'])

                LOGGER.info('confirm finish ')

            elif pc_payload['action'] == 'transfer':

                LOGGER.info('transfer')

                coin = pc_payload['coin']
                acceptor = pc_payload['acceptor']
                user_state = UserState(context)
                if not user_state.subtract_coin(signer,coin):
                    raise InvalidTransaction('balance not enough')
                if not user_state.add_coin(acceptor,coin):
                    raise InvalidTransaction('acceptor not exist')

                LOGGER.info('transfer finished')

            elif pc_payload['action'] == 'authorize':
                LOGGER.info('authorize')

                station = pc_payload['station']
                pub_key = pc_payload['pub_key']

                setting_state = SettingState(context)
                if signer!= setting_state.get_admin_key():
                    raise InvalidTransaction('unauthority')

                station_state = StationState(context)
                station_state.add_key(station,pub_key)

                LOGGER.info('authorize finish')

            else:
                raise InvalidTransaction('unsupported action type')

        except TypeError as e:
            raise InvalidTransaction('error format of payload or error type in payload')

        except KeyError as e:
            raise InvalidTransaction('missing key :' + str(e))


        '''old version without using json

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

            setting_state = SettingState(context)
            if not setting_state.inited(signer):
                raise InvalidTransaction("init key existed")

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
        
        '''
