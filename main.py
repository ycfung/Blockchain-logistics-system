import hashlib
import logging
import sys

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

from pc_processor.handler import PCTransactionHandler

def main():
    try:

        print('pacel-chain-transaction-handler start-------------\n')
        # Register the transaction handler and start it.

        processor = TransactionProcessor(url='tcp://localhost:4004')

        handler = PCTransactionHandler()

        processor.add_handler(handler)

        processor.start()



    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        #traceback.print_exc(file=sys.stderr)
        sys.exit(1)

main()