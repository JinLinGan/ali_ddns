#!/usr/bin/env python


'''
pip isntall aliyun-python-sdk-alidns
'''
import json
import sys

from datetime import datetime

from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkcore import client


# get RR list
def get_RR_list(fulldomain, domain):
    RR = []
    if type(fulldomain) == str:
        n_rr = fulldomain.split('.' + domain)[0]
        print_("add RR %s to list" % n_rr)
        RR.append(n_rr)
    if type(fulldomain) == list:
        for f in fulldomain:
            n_rr = f.split('.' + domain)[0]
            print_("add RR %s to list" % n_rr)
            RR.append(n_rr)
    return RR


def print_(str):
    if debug:
        print(str)


#fulldomain = "@.ganjl.top"
#text = "text changed" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

fulldomain = sys.argv[1]
text = sys.argv[2]

domain = "ganjl.top"

debug = True

RR = get_RR_list(fulldomain, domain)

config = {
    "key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "secret": "yyyyyyyyyyyyyyyyyyyyyyyyyyyy",
    "region": "cn-hangzhou"
}

c = client.AcsClient(config["key"], config["secret"], config["region"])


def get_RR_requestID(RR):
    id_r = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    id_r.set_DomainName("ganjl.top")
    id_r.set_accept_format("JSON")
    id_re = c.do_action(id_r)
    j = json.loads(id_re)

    change_list = {}
    for r in j["DomainRecords"]["Record"]:
        if r["RR"] in RR and r['Type'] == 'TXT' and (not change_list.has_key(r["RR"])):
            change_list[r["RR"]] = r['RecordId']

    for r in RR:
        if not change_list.has_key(r):
            change_list[r] = None

    return change_list


# RR


def update(id, RR, text):
    print_("update RR '%s' value is %s --  id is %s " % (RR, text, id))
    id_r = UpdateDomainRecordRequest.UpdateDomainRecordRequest()

    id_r.set_RecordId(id)
    id_r.set_RR(RR)
    id_r.set_Type('TXT')
    id_r.set_Value(text)

    id_re = c.do_action(id_r)
    print_(id_re)


def add(RR, text):
    print_("add RR '%s' value is %s " % (RR, text))
    id_r = AddDomainRecordRequest.AddDomainRecordRequest()

    id_r.set_DomainName(domain)
    id_r.set_RR(RR)
    id_r.set_Type('TXT')
    id_r.set_Value(text)

    id_re = c.do_action(id_r)
    print_(id_re)


def process(change_list):
    for k in change_list.keys():
        if change_list[k] is None:
            add(k, text)
        else:
            update(change_list[k], k, text)


change_list = get_RR_requestID(RR)

process(change_list)
#
#
# add(RR,text)
# sys.exit(0)
