#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest
from aliyunsdkcore import client
import json
import re
import subprocess

JSONDecoder = json.JSONDecoder()
JSONEncoder = json.JSONEncoder()

conf_file = "config.json"
argv_arr = sys.argv.copy()
argv_arr.reverse()
while len(argv_arr) > 1:
    arg = argv_arr.pop()
    if arg == "-c" || arg == "--config":
        try:
            conf_file = argv_arr.pop();
        except:
            raise Exception("Uncomplete config argument.")
    else if arg == "-?" || "--help":
        print('''
Usage: %s [options]
  -c, --config:
    Custom config file path.
  -?, --help:
    Show this help.
''' % sys.argv[0])

conf_file_in = open(conf_file, 'r')
try:
    conf_json_raw = conf_file_in.read()
except:
    raise Exception("Unable to find config")
finally:
    conf_file_in.close()


conf_json_obj = JSONDecoder.decode(conf_json_raw)
accessKeyId = conf_json_obj['accessKeyId']
accessKeySecret = conf_json_obj['accessKeySecret']
rc_info = conf_json_obj['rc_info']
rc_domain = list(rc_info.keys())

rc_type = 'AAAA'
rc_record_RequestId = 'D4'
try:
    aliyun_endpoint = conf_json_obj['aliyun_endpoint']
except:
    aliyun_endpoint = 'cn-hangzhou'
bool_got_ids = False
def check_records(dns_domain):
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyun_endpoint)
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format('json')
    result = clt.do_action_with_exception(request)
    return result.decode()

for domain in rc_domain:
    for info in rc_info[domain]:
        rc_rr = info['rc_rr']
        rc_record_id = info['rc_record_id']
        if rc_record_id is None:
            rc_record_id_json_raw = check_records(domain)
            rc_record_id_json_obj = JSONDecoder.decode(rc_record_id_json_raw)
            for record in rc_record_id_json_obj['DomainRecords']['Record']:
                if record['RR'] == rc_rr and record['Type'] == rc_type and record['Locked'] == False and record['Status'] == "ENABLE":
                    print("Record: %s.%s, Type: %s, TTL: %d, Line: %s.\nRecordId: %s\n" % (rc_rr, domain, rc_type, record['TTL'], record['Line'], record['RecordId']))
                    bool_got_ids = True
            if bool_got_ids is False:
                print("No records found.")