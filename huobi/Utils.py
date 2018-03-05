#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests

# 此处填写APIKEY

ACCESS_KEY = ""
SECRET_KEY = ""

# 首次运行可通过get_accounts()获取acct_id,然后直接赋值,减少重复获取。
ACCOUNT_ID = 

# API 请求地址
MARKET_URL = "https://api.huobi.pro"
TRADE_URL = "https://api.huobi.pro"

# 所有的交易对
ALL_TRADE_PAIRS = ['omgusdt', 'linkbtc', 'naseth', 'eoseth', 'swftcbtc', 'xemusdt', 'zecusdt', 'dashbtc', 'paybtc',
                   'evxbtc', 'mdseth', 'tntbtc', 'qasheth', 'smteth', 'trxeth', 'thetausdt', 'luneth', 'ruffeth',
                   'bchbtc', 'elaeth', 'iosteth', 'tnbbtc', 'gnxeth', 'thetabtc', 'sntusdt', 'datbtc', 'soceth',
                   'eosusdt', 'chateth', 'manabtc', 'smtusdt', 'xrpbtc', 'ltcusdt', 'qtumusdt', 'letbtc', 'bcdbtc',
                   'sntbtc', 'wprbtc', 'cvcusdt', 'elfeth', 'gnteth', 'utkbtc', 'sbtcbtc', 'neousdt', 'mcobtc',
                   'osteth', 'htbtc', 'rcnbtc', 'bt2btc', 'qunbtc', 'hsreth', 'topceth', 'salteth', 'aidoceth',
                   'waxbtc', 'cvceth', 'dtaeth', 'btcusdt', 'meeeth', 'powreth', 'gaseth', 'adxeth', 'neobtc',
                   'saltbtc', 'letusdt', 'btmbtc', 'ekoeth', 'bateth', 'ekobtc', 'srnbtc', 'appcbtc', 'ocneth',
                   'cmtbtc', 'veneth', 'qtumeth', 'reqbtc', 'bifibtc', 'btmeth', 'icxbtc', 'ocnbtc', 'zecbtc', 'actbtc',
                   'dgdeth', 'dateth', 'etcusdt', 'ostbtc', 'iostusdt', 'stketh', 'mcoeth', 'hteth', 'storjbtc',
                   'hsrbtc', 'quneth', 'socbtc', 'elfbtc', 'cmteth', 'venbtc', 'gntbtc', 'dbcbtc', 'storjusdt',
                   'waxeth', 'trxbtc', 'powrbtc', 'zilusdt', 'dtausdt', 'dtabtc', 'sncbtc', 'zilbtc', 'meebtc',
                   'lskbtc', 'nasbtc', 'tnbeth', 'swftceth', 'ltcbtc', 'eosbtc', 'linketh', 'iostbtc', 'yeebtc',
                   'htusdt', 'ruffbtc', 'rdnbtc', 'lunbtc', 'gnxbtc', 'elabtc', 'leteth', 'evxeth', 'wpreth', 'astbtc',
                   'acteth', 'bchusdt', 'dashusdt', 'icxeth', 'bcxbtc', 'mtneth', 'propyeth', 'dgdbtc', 'xrpusdt',
                   'zileth', 'zrxbtc', 'thetaeth', 'ethbtc', 'snceth', 'dbceth', 'reqeth', 'wicceth', 'smtbtc',
                   'lsketh', 'rpxbtc', 'tnteth', 'mtxbtc', 'srneth', 'ethusdt', 'itcbtc', 'omgbtc', 'payeth', 'stkbtc',
                   'venusdt', 'mdsbtc', 'adxbtc', 'etcbtc', 'aidocbtc', 'kncbtc', 'hsrusdt', 'qtumbtc', 'cvcbtc',
                   'qspbtc', 'qspeth', 'btgbtc', 'batbtc', 'zlaeth', 'qashbtc', 'itceth', 'xembtc', 'mtxeth', 'manaeth',
                   'gasbtc', 'mtnbtc', 'chatbtc', 'bt1btc', 'zlabtc', 'omgeth', 'rcneth', 'utketh', 'topcbtc', 'mtlbtc',
                   'gntusdt', 'appceth', 'propybtc', 'wiccbtc', 'rdneth', 'elfusdt', 'yeeeth']

# 价格精度
PRICE_PRECISION = {'omgusdt': 2, 'linkbtc': 8, 'naseth': 6, 'eoseth': 8, 'swftcbtc': 8, 'xemusdt': 4, 'zecusdt': 2,
                   'dashbtc': 6, 'paybtc': 6, 'evxbtc': 8, 'mdseth': 8, 'tntbtc': 8, 'qasheth': 6, 'smteth': 8,
                   'trxeth': 8, 'thetausdt': 4, 'luneth': 6, 'ruffeth': 8, 'bchbtc': 6, 'elaeth': 8, 'iosteth': 8,
                   'tnbbtc': 8, 'gnxeth': 8, 'thetabtc': 8, 'sntusdt': 4, 'datbtc': 8, 'soceth': 8, 'eosusdt': 2,
                   'chateth': 8, 'manabtc': 8, 'smtusdt': 4, 'xrpbtc': 8, 'ltcusdt': 2, 'qtumusdt': 2, 'letbtc': 8,
                   'bcdbtc': 6, 'sntbtc': 8, 'wprbtc': 8, 'cvcusdt': 4, 'elfeth': 8, 'gnteth': 8, 'utkbtc': 8,
                   'sbtcbtc': 6, 'neousdt': 2, 'mcobtc': 6, 'osteth': 8, 'htbtc': 8, 'rcnbtc': 8, 'bt2btc': 6,
                   'qunbtc': 8, 'hsreth': 6, 'topceth': 8, 'salteth': 6, 'aidoceth': 8, 'waxbtc': 8, 'cvceth': 8,
                   'dtaeth': 8, 'btcusdt': 2, 'meeeth': 8, 'powreth': 8, 'gaseth': 6, 'adxeth': 8, 'neobtc': 6,
                   'saltbtc': 6, 'letusdt': 4, 'btmbtc': 8, 'ekoeth': 8, 'bateth': 8, 'ekobtc': 8, 'srnbtc': 8,
                   'appcbtc': 8, 'ocneth': 8, 'cmtbtc': 8, 'veneth': 8, 'qtumeth': 6, 'reqbtc': 8, 'bifibtc': 8,
                   'btmeth': 8, 'icxbtc': 6, 'ocnbtc': 8, 'zecbtc': 6, 'actbtc': 8, 'dgdeth': 6, 'dateth': 8,
                   'etcusdt': 2, 'ostbtc': 8, 'iostusdt': 4, 'stketh': 8, 'mcoeth': 6, 'hteth': 8, 'storjbtc': 8,
                   'hsrbtc': 6, 'quneth': 8, 'socbtc': 8, 'elfbtc': 8, 'cmteth': 8, 'venbtc': 8, 'gntbtc': 8,
                   'dbcbtc': 8, 'storjusdt': 4, 'waxeth': 6, 'trxbtc': 8, 'powrbtc': 8, 'zilusdt': 4, 'dtausdt': 4,
                   'dtabtc': 8, 'sncbtc': 8, 'zilbtc': 8, 'meebtc': 8, 'lskbtc': 6, 'nasbtc': 6, 'tnbeth': 8,
                   'swftceth': 8, 'ltcbtc': 6, 'eosbtc': 8, 'linketh': 8, 'iostbtc': 8, 'yeebtc': 8, 'htusdt': 4,
                   'ruffbtc': 8, 'rdnbtc': 8, 'lunbtc': 6, 'gnxbtc': 8, 'elabtc': 8, 'leteth': 8, 'evxeth': 8,
                   'wpreth': 8, 'astbtc': 8, 'acteth': 8, 'bchusdt': 2, 'dashusdt': 2, 'icxeth': 6, 'bcxbtc': 8,
                   'mtneth': 8, 'propyeth': 8, 'dgdbtc': 6, 'xrpusdt': 4, 'zileth': 8, 'zrxbtc': 8, 'thetaeth': 8,
                   'ethbtc': 6, 'snceth': 8, 'dbceth': 8, 'reqeth': 8, 'wicceth': 8, 'smtbtc': 8, 'lsketh': 6,
                   'rpxbtc': 8, 'tnteth': 8, 'mtxbtc': 8, 'srneth': 8, 'ethusdt': 2, 'itcbtc': 8, 'omgbtc': 6,
                   'payeth': 6, 'stkbtc': 8, 'venusdt': 2, 'mdsbtc': 8, 'adxbtc': 8, 'etcbtc': 6, 'aidocbtc': 8,
                   'kncbtc': 8, 'hsrusdt': 2, 'qtumbtc': 6, 'cvcbtc': 8, 'qspbtc': 8, 'qspeth': 8, 'btgbtc': 6,
                   'batbtc': 8, 'zlaeth': 8, 'qashbtc': 8, 'itceth': 8, 'xembtc': 8, 'mtxeth': 8, 'manaeth': 8,
                   'gasbtc': 6, 'mtnbtc': 8, 'chatbtc': 8, 'bt1btc': 6, 'zlabtc': 8, 'omgeth': 6, 'rcneth': 8,
                   'utketh': 8, 'topcbtc': 8, 'mtlbtc': 6, 'gntusdt': 4, 'appceth': 6, 'propybtc': 8, 'wiccbtc': 8,
                   'rdneth': 8, 'elfusdt': 4, 'yeeeth': 8}

# 数量精度
AMOUNT_PRECISION = {'omgusdt': 4, 'linkbtc': 2, 'naseth': 4, 'eoseth': 2, 'swftcbtc': 2, 'xemusdt': 4, 'zecusdt': 4,
                    'dashbtc': 4, 'paybtc': 4, 'evxbtc': 2, 'mdseth': 0, 'tntbtc': 0, 'qasheth': 4, 'smteth': 0,
                    'trxeth': 2, 'thetausdt': 4, 'luneth': 4, 'ruffeth': 2, 'bchbtc': 4, 'elaeth': 2, 'iosteth': 2,
                    'tnbbtc': 0, 'gnxeth': 0, 'thetabtc': 2, 'sntusdt': 4, 'datbtc': 2, 'soceth': 2, 'eosusdt': 4,
                    'chateth': 2, 'manabtc': 0, 'smtusdt': 4, 'xrpbtc': 0, 'ltcusdt': 4, 'qtumusdt': 4, 'letbtc': 2,
                    'bcdbtc': 4, 'sntbtc': 0, 'wprbtc': 2, 'cvcusdt': 2, 'elfeth': 0, 'gnteth': 0, 'utkbtc': 2,
                    'sbtcbtc': 4, 'neousdt': 4, 'mcobtc': 4, 'osteth': 2, 'htbtc': 2, 'rcnbtc': 0, 'bt2btc': 4,
                    'qunbtc': 2, 'hsreth': 4, 'topceth': 2, 'salteth': 4, 'aidoceth': 2, 'waxbtc': 4, 'cvceth': 0,
                    'dtaeth': 2, 'btcusdt': 4, 'meeeth': 2, 'powreth': 0, 'gaseth': 4, 'adxeth': 2, 'neobtc': 4,
                    'saltbtc': 4, 'letusdt': 4, 'btmbtc': 0, 'ekoeth': 2, 'bateth': 0, 'ekobtc': 2, 'srnbtc': 2,
                    'appcbtc': 2, 'ocneth': 2, 'cmtbtc': 0, 'veneth': 2, 'qtumeth': 4, 'reqbtc': 1, 'bifibtc': 4,
                    'btmeth': 0, 'icxbtc': 4, 'ocnbtc': 2, 'zecbtc': 4, 'actbtc': 2, 'dgdeth': 4, 'dateth': 2,
                    'etcusdt': 4, 'ostbtc': 2, 'iostusdt': 4, 'stketh': 2, 'mcoeth': 4, 'hteth': 2, 'storjbtc': 2,
                    'hsrbtc': 4, 'quneth': 2, 'socbtc': 2, 'elfbtc': 0, 'cmteth': 0, 'venbtc': 2, 'gntbtc': 0,
                    'dbcbtc': 2, 'storjusdt': 4, 'waxeth': 4, 'trxbtc': 2, 'powrbtc': 0, 'zilusdt': 4, 'dtausdt': 4,
                    'dtabtc': 2, 'sncbtc': 2, 'zilbtc': 2, 'meebtc': 2, 'lskbtc': 4, 'nasbtc': 4, 'tnbeth': 0,
                    'swftceth': 2, 'ltcbtc': 4, 'eosbtc': 2, 'linketh': 2, 'iostbtc': 2, 'yeebtc': 2, 'htusdt': 2,
                    'ruffbtc': 2, 'rdnbtc': 0, 'lunbtc': 4, 'gnxbtc': 0, 'elabtc': 2, 'leteth': 2, 'evxeth': 2,
                    'wpreth': 2, 'astbtc': 0, 'acteth': 2, 'bchusdt': 4, 'dashusdt': 4, 'icxeth': 4, 'bcxbtc': 4,
                    'mtneth': 2, 'propyeth': 2, 'dgdbtc': 4, 'xrpusdt': 2, 'zileth': 2, 'zrxbtc': 0, 'thetaeth': 2,
                    'ethbtc': 4, 'snceth': 2, 'dbceth': 2, 'reqeth': 1, 'wicceth': 2, 'smtbtc': 0, 'lsketh': 4,
                    'rpxbtc': 2, 'tnteth': 0, 'mtxbtc': 2, 'srneth': 2, 'ethusdt': 4, 'itcbtc': 0, 'omgbtc': 4,
                    'payeth': 4, 'stkbtc': 2, 'venusdt': 4, 'mdsbtc': 0, 'adxbtc': 2, 'etcbtc': 4, 'aidocbtc': 2,
                    'kncbtc': 0, 'hsrusdt': 4, 'qtumbtc': 4, 'cvcbtc': 0, 'qspbtc': 0, 'qspeth': 0, 'btgbtc': 4,
                    'batbtc': 0, 'zlaeth': 2, 'qashbtc': 4, 'itceth': 0, 'xembtc': 2, 'mtxeth': 2, 'manaeth': 0,
                    'gasbtc': 4, 'mtnbtc': 2, 'chatbtc': 2, 'bt1btc': 4, 'zlabtc': 2, 'omgeth': 4, 'rcneth': 0,
                    'utketh': 2, 'topcbtc': 2, 'mtlbtc': 4, 'gntusdt': 4, 'appceth': 4, 'propybtc': 2, 'wiccbtc': 2,
                    'rdneth': 0, 'elfusdt': 4, 'yeeeth': 2}

# 所有的换币组合
ALL_TRADE_GROUP = ['omgusdt-omgbtc-btcusdt', 'omgusdt-omgeth-ethusdt', 'xemusdt-xembtc-btcusdt',
                   'zecusdt-zecbtc-btcusdt', 'thetausdt-thetabtc-btcusdt', 'thetausdt-thetaeth-ethusdt',
                   'sntusdt-sntbtc-btcusdt', 'eosusdt-eoseth-ethusdt', 'eosusdt-eosbtc-btcusdt',
                   'smtusdt-smteth-ethusdt', 'smtusdt-smtbtc-btcusdt', 'ltcusdt-ltcbtc-btcusdt',
                   'qtumusdt-qtumeth-ethusdt', 'qtumusdt-qtumbtc-btcusdt', 'cvcusdt-cvceth-ethusdt',
                   'cvcusdt-cvcbtc-btcusdt', 'neousdt-neobtc-btcusdt', 'btcusdt-dashbtc-dashusdt',
                   'btcusdt-bchbtc-bchusdt', 'btcusdt-thetabtc-thetausdt', 'btcusdt-xrpbtc-xrpusdt',
                   'btcusdt-letbtc-letusdt', 'btcusdt-sntbtc-sntusdt', 'btcusdt-htbtc-htusdt', 'btcusdt-neobtc-neousdt',
                   'btcusdt-zecbtc-zecusdt', 'btcusdt-storjbtc-storjusdt', 'btcusdt-hsrbtc-hsrusdt',
                   'btcusdt-elfbtc-elfusdt', 'btcusdt-venbtc-venusdt', 'btcusdt-gntbtc-gntusdt',
                   'btcusdt-dtabtc-dtausdt', 'btcusdt-zilbtc-zilusdt', 'btcusdt-ltcbtc-ltcusdt',
                   'btcusdt-eosbtc-eosusdt', 'btcusdt-iostbtc-iostusdt', 'btcusdt-ethbtc-ethusdt',
                   'btcusdt-smtbtc-smtusdt', 'btcusdt-omgbtc-omgusdt', 'btcusdt-etcbtc-etcusdt',
                   'btcusdt-qtumbtc-qtumusdt', 'btcusdt-cvcbtc-cvcusdt', 'btcusdt-xembtc-xemusdt',
                   'letusdt-letbtc-btcusdt', 'letusdt-leteth-ethusdt', 'etcusdt-etcbtc-btcusdt',
                   'iostusdt-iosteth-ethusdt', 'iostusdt-iostbtc-btcusdt', 'storjusdt-storjbtc-btcusdt',
                   'zilusdt-zilbtc-btcusdt', 'zilusdt-zileth-ethusdt', 'dtausdt-dtaeth-ethusdt',
                   'dtausdt-dtabtc-btcusdt', 'htusdt-htbtc-btcusdt', 'htusdt-hteth-ethusdt', 'bchusdt-bchbtc-btcusdt',
                   'dashusdt-dashbtc-btcusdt', 'xrpusdt-xrpbtc-btcusdt', 'ethusdt-eoseth-eosusdt',
                   'ethusdt-smteth-smtusdt', 'ethusdt-iosteth-iostusdt', 'ethusdt-elfeth-elfusdt',
                   'ethusdt-gnteth-gntusdt', 'ethusdt-hsreth-hsrusdt', 'ethusdt-cvceth-cvcusdt',
                   'ethusdt-dtaeth-dtausdt', 'ethusdt-veneth-venusdt', 'ethusdt-qtumeth-qtumusdt',
                   'ethusdt-hteth-htusdt', 'ethusdt-leteth-letusdt', 'ethusdt-zileth-zilusdt',
                   'ethusdt-thetaeth-thetausdt', 'ethusdt-ethbtc-btcusdt', 'ethusdt-omgeth-omgusdt',
                   'venusdt-veneth-ethusdt', 'venusdt-venbtc-btcusdt', 'hsrusdt-hsreth-ethusdt',
                   'hsrusdt-hsrbtc-btcusdt', 'gntusdt-gnteth-ethusdt', 'gntusdt-gntbtc-btcusdt',
                   'elfusdt-elfeth-ethusdt', 'elfusdt-elfbtc-btcusdt']


# 'Timestamp': '2017-06-02T06:13:49'

def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)

    try:
        response = requests.get(url, postdata, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" % (response.text, e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)

    try:
        response = requests.post(url, postdata, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" % (response.text, e))
        return


def api_key_get(params, request_path):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)

    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
