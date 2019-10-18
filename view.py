from django_test.sawtooth_client.client import *
import base64


PC_NAMESPACE = hashlib.sha512('pacel_chain'.encode("utf-8")).hexdigest()[0:6]
USER_NAMESPACE = hashlib.sha512('user_state'.encode("utf-8")).hexdigest()[0:4]
ODER_NAMESPACE = hashlib.sha512('oder_state'.encode("utf-8")).hexdigest()[0:4]

rest_api_addr = "http://127.0.0.1:8008"


def make_user_address(public_key):
    return PC_NAMESPACE + USER_NAMESPACE + public_key[-60:]


def make_oder_address(oder_number):
    return PC_NAMESPACE + ODER_NAMESPACE + hashlib.sha512(oder_number.encode("utf-8")).hexdigest()[-60:]


def make_station_address(station):
    return PC_NAMESPACE + hashlib.sha512(station.encode('utf-8')).hexdigest()[-64:]


def make_mobile_address(mobile):
    return PC_NAMESPACE + hashlib.sha512(mobile.encode('utf-8')).hexdigest()[-64:]


SETTING_ADDRESS = PC_NAMESPACE + "0000000000000000000000000000000000000000000000000000000000000000"

class ViewConditions:
    def __init__(self, url):
        self.url = url

    def getBlocks(self):
        r_json = self.get_warp(url=self.url + '/blocks')
        blocks = []
        for x in r_json['data']:
            blocks.append(x)
        return blocks

    def getBlock(self, id):
        return self.get_warp(url=self.url + '/blocks/' + str(id))

    def getStates(self):
        r_json = self.get_warp(url=self.url + '/state')
        states = []
        for x in r_json['data']:
            x['data'] = base64.b64decode(x['data'])
            states.append(x)
        return states

    def getState(self, address):
        return base64.b64decode(self.get_warp(url=self.url + '/state/' + str(address))['data'])

    def getTransactions(self):
        r_json = self.get_warp(url=self.url + '/transactions')
        transactions = []
        for x in r_json['data']:
            transactions.append(x)
        return transactions
    
    def getApply(self):
        applys = []
        accepteds = []
        transactions = self.getTransactions();
        for t in transactions:
            print(t['payload'])
            print(str(base64.b64decode(t['payload'])))
            try:
                payload = json.loads(str(base64.b64decode(t['payload']))[2:-1])
                if payload['action'] == 'apply':
                    applys.append(payload['order_number'])
                if payload['action'] == 'accept':
                    accepteds.append(payload['order_number'])
            except:
                continue;   
        for ac in accepteds:
            applys.remove(ac)
        return applys

    def getApplyPage(self,limit):
        r_json = self.get_warp(url=self.url + '/transactions',para={'limit':limit})
        return ApplyPage(self,r_json)

    def getTransaction(self, transaction_id):
        return self.get_warp(url=self.url + '/transactions/' + str(transaction_id))

    def get_warp(self, url, para=set()):
        r = requests.get(url=url, params=para)
        if r.status_code == 200:
            r_json = r.json()
            return r_json
        else:
            raise RequestError(r.status_code)

class ApplyPage:
    def __init__(self,vc,page_json,accepteds = []):
        self.vc = vc
        self.limit = page_json["paging"]["limit"]
        self.next_page_url = page_json["paging"]["next"]
        transactions = []
        for x in page_json['data']:
            transactions.append(x)
        
        self.applys = []
        self.accepteds = accepteds
        for t in transactions:
            print(t['payload'])
            print(str(base64.b64decode(t['payload'])))
            try:
                payload = json.loads(str(base64.b64decode(t['payload']))[2:-1])
                if payload['action'] == 'apply':
                    applys.append(payload['order_number'])
                if payload['action'] == 'accept':
                    accepteds.append(payload['order_number'])
            except:
                continue;    
        for ac in self.accepteds:
            self.applys.remove(ac)

    def get_next_page(self):
        return ApplyPage(self.vc,self.vc.get_warp(self.next_page_url,{'limit':self.limit}),self.accepteds)

    def get_applys(self):
        return self.applys

        

def sortByKey(transaction, key):
    results = []
    for transaction in transaction:
        if key == transaction['header']['signer_public_key']:
            results.append(transaction)
    return results


def sorByState(transactions, address):
    results = []
    for transaction in transactions:
        if (address in transaction['header']['inputs']) or (address in transaction['header']['outputs']):
            results.append(transaction)
    return results


def sortByInput(transactions, address):
    results = []
    for transaction in transactions:
        if address in transaction['header']['inputs']:
            results.append(transaction)
    return results


def sortByOutput(transactions, address):
    results = []
    for transaction in transactions:
        if address in transaction['header']['outputs']:
            results.append(transaction)
    return results


class RequestError(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "Http State Code: " + repr(self.status)

