#!/bin/env python
#encoding=utf-8
# Author: shaolong - shaolong@sogou-inc.com
# Last modified: 2014-08-10 15:24
# Filename: huobi.py
# Description: 
import sys
import urllib2
import urllib
import httplib
import hashlib
import json
import time

class Huobi:
    def __init__(self):
        self.conn=httplib.HTTPSConnection("api.huobi.com")                                        
        self.BTC_DEPTH_FILENAME = 'http://market.huobi.com/staticmarket/depth_btc_json.js'
        self.market_depth = None
        self.access_key = '5795d5d4-ab3e0ccd-76a1387a-d912a'
        self.secret_key = '0f84f0a7-84b938ef-08fe8854-d48c5'

    def output(self, data):
        print json.dumps(data, ensure_ascii=False)


    def __send_request(self, data):
        pass
        data.append(('access_key',  self.access_key))
        data.append(('created',  int(time.time())))
        data.append(('secret_key',  self.secret_key))
        data = sorted(data, key = lambda x: x[0])
        pre_sign = urllib.urlencode(data)
        md5 = hashlib.md5(pre_sign).hexdigest()
        data.append(('sign',  md5))

        headers = {
                "User-Agent": "Mozilla-Firefox5.0",
                'Content-type': 'application/x-www-form-urlencoded'
                }


        self.conn.request("POST",'/apiv2.php', urllib.urlencode(data), headers) 
        response = self.conn.getresponse()
        if response.status == 200:
            result = json.loads(response.read())
            if 'result' in result and result['result'] == 'fail':
                print >> sys.stderr, result['msg']
                print >> self.output(result)
                return None

            return result
        else:
            print >> sys.stderr, 'Cannot get proper response from server, error code:', response.status
            return None
        




    def get_account_info(self):
        pass
        data = []
        data.append(('method', 'get_account_info'))
        result = self.__send_request(data)
        return result

    def get_orders(self):
        pass
        data = []
        data.append(('method', 'get_orders'))
        data.append(('coin_type', 1))
        result = self.__send_request(data)
        return result

    def get_market_depth(self):
        try:
            response = urllib2.urlopen(self.BTC_DEPTH_FILENAME, timeout=5)
        except Exception, e:
            print >> sys.stderr, "Can not get_market_depth ", e
            return None

        json_str = response.read()
        
        try:
            resut_dict = json.loads(json_str)
        except Exception, e:
            print >> sys.stderr, "Parsing get_market_depth result error ", e
            return None

        self.market_depth = resut_dict
    
    def buy_market(self, amount):
        pass
        data = []
        data.append(('method', 'buy_market'))
        data.append(('coin_type', 1))
        result = self.__send_request(data)
        return result

    def sell_market(self, amount):
        pass
        data = []
        data.append(('method', 'sell_market'))
        data.append(('coin_type', 1))
        result = self.__send_request(data)
        return result



if __name__ == '__main__':
    hb = Huobi()
    hb.get_market_depth()
    print hb.market_depth
    #hb.output(hb.get_account_info())
    #hb.output(hb.get_orders())
    #hb.output(hb.buy_market(0.001))
    #hb.output(hb.sell_market(0.001))
