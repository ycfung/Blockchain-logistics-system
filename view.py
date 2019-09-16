import json
import requests
import base64
import yaml
import hashlib

PC_NAMESPACE = hashlib.sha512('pacel_chain'.encode("utf-8")).hexdigest()[0:6]
USER_NAMEPCACE = hashlib.sha512('user_state'.encode("utf-8")).hexdigest()[0:4]
ODER_NAMESPACE = hashlib.sha512('oder_state'.encode("utf-8")).hexdigest()[0:4]

def make_user_address(public_key):
    return PC_NAMESPACE + USER_NAMEPCACE + public_key[-60:]
def make_oder_address(oder_number):
    return PC_NAMESPACE + ODER_NAMESPACE + hashlib.sha512(oder_number.encode("utf-8")).hexdigest()[-60:]
def make_station_address(station):
    return PC_NAMESPACE + hashlib.sha512(station.encode('utf-8')).hexdigest()[-64:]
def make_mobile_address(mobile):
    return PC_NAMESPACE + hashlib.sha512(mobile.encode('utf-8')).hexdigest()[-64:]
SETTING_ADDRESS = PC_NAMESPACE + "0000000000000000000000000000000000000000000000000000000000000000"


class ViewConditions:
    def __init__(self,url):
        self.url=url

    def getBlocks(self):
        rjson = self._get_warp(url=self.url+'/blocks')
        blocks=[]
        for x in rjson['data']:
            blocks.append(x)
        return blocks

    def getBlock(self,id):
        return self._get_warp(url=self.url+'/blocks/'+str(id))

    def getStates(self):
        rjson = self._get_warp(url=self.url + '/state')
        states = []
        for x in rjson['data']:
            x['data'] = base64.b64decode(x['data'])
            states.append(x)
        return states

    def getState(self,adress):
        return base64.b64decode(self._get_warp(url=self.url + '/state/' + str(adress))['data'])


    def getTransactions(self):
        rjson = self._get_warp(url=self.url + '/transactions')
        transactions = []
        for x in rjson['data']:
            transactions.append(x)
        return transactions

    def getTransaction(self,transcationid):
        return self._get_warp(url=self.url+'/transactions/'+str(transcationid))

    def _get_warp(self,url,para=set()):
        r = requests.get(url=url,params=para)
        if r.status_code == 200:
            rjson = r.json()
            return rjson
        else:
            raise RequestError(r.status_code)


def sortByKey(transaction,key):
        resaults=[]
        for transaction in transaction:
            if key == transaction['header']['signer_public_key']:
                resaults.append(transaction)
        return resaults

def sorByState(transactions,adress):
        results=[]
        for transaction in transactions:
            if (adress in transaction['header']['inputs'])or(adress in transaction['header']['outputs']):
               results.append(transaction)
        return results

def sortByInput(transactions,adress):
        results = []
        for transaction in transactions:
            if adress in transaction['header']['inputs']:
                results.append(transaction)
        return results

def sortByOutput(transactions,adress):
        results = []
        for transaction in transactions:
            if adress in transaction['header']['outputs']:
                results.append(transaction)
        return results

class RequestError(Exception):
    def __init__(self,statu):
        self.statu=statu
    def __str__(self):
        return "Http State Code:"+repr(self.statu)


vc=ViewConditions('http://127.0.0.1:8008')
state=vc.getState(make_mobile_address("13160606060"))
print(state)

