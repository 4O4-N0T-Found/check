#!/usr/bin/env python3
#coding=utf-8
import sys
import argparse
import requests
import json
import time
import random


# You can prefill the following config to skip cli

# Session ID is required
SESSION = ""
CONFIG = {
    # Following fields are required
    "currentAddress": "",
    "temperature": "36.5°C~36.9°C",
    "province": "四川省",
    "city": "成都市",
    "county": "青羊区",
    # Following are optional
    "remark": "",
    "healthInfo": "正常",
    "isContactWuhan": 0,
    "isFever": 0,
    "isInSchool": 0,
    "isLeaveChengdu": 0,
    "isSymptom": 0
}

HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
    "X-Tag": "flyio",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wx521c0c16b77041a0/7/page-frame.html",
    "Accept-Language": "en-us"
}


def pre_check():
    global SESSION, CONFIG

    if SESSION == "":
        return False

    if (CONFIG['currentAddress'] == "" or
        CONFIG['temperature'] == "" or CONFIG['province'] == "" or
        CONFIG['city'] == "" or CONFIG['county'] == ""):
        return False
    return True


def _parse_args(parser):
    parser.add_argument(
        "sessionid",
        help="Your Session ID"
    )
    parser.add_argument(
        '-a', '--address',
        required=True,
        help='Current Address'
    )
    parser.add_argument(
        '-p', '--province',
        required=True,
        help='Province'
    )
    parser.add_argument(
        '-c', '--city',
        required=True,
        help='City'
    )
    parser.add_argument(
        '-n', '--county',
        required=True,
        help='County'
    )
    parser.add_argument(
        '-t', '--temperature',
        default='36.9°C~37.3°C',
        help='Temperature'
    )
    return parser.parse_args()


def put_value():
    if pre_check() is False:
        parser = argparse.ArgumentParser()
        args = _parse_args(parser)

        global SESSION, CONFIG
        SESSION = args.sessionid
        CONFIG['currentAddress'] = args.address
        CONFIG['temperature'] = args.temperature
        CONFIG['province'] = args.province
        CONFIG['city'] = args.city
        CONFIG['county'] = args.county

        if pre_check() is False:
            raise Exception("Invalid form!")


def register_check():
    resp = requests.get("https://xgaffairs.uestc.edu.cn/wxvacation/./checkRegister", headers=HEADERS)
    resp_data = json.loads(resp.text)
    data = resp_data['data']

    if data is None:
        print(" Session invalid or INTERNAL SERVER ERROR!")
        raise Exception("Session invalid or INTERNAL SERVER ERROR!")
    else: return data


def daily_register(SESSION):
    global HEADERS
    HEADERS['Cookie'] = "JSESSIONID=" + SESSION

    if register_check():
        print(" You have registered today!")
        raise Exception("You have registered today!")

    HEADERS['Content-Type'] = 'application/json'
    resp = requests.post("https://xgaffairs.uestc.edu.cn/wxvacation/./monitorRegister",
                         headers=HEADERS, data=json.dumps(CONFIG, ensure_ascii=False).encode('utf-8'))
    resp_data = json.loads(resp.text)

    if resp_data['code'] == 0:
        print("Register Success!")
    else:
        print(" Unknown Error")
        raise Exception("Unknown Error")


def main():
    # ran = random.randint(0,5)
    # time.sleep(ran*60)
    # print('#########################################')
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    put_value()
    daily_register(sys.argv[1])


if __name__ == '__main__':
    main()
