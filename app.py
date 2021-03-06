#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest
from aliyunsdkcore import client
import json
import re
import subprocess
import sys

JSONDecoder = json.JSONDecoder()
JSONEncoder = json.JSONEncoder()

conf_file = "config.json"
argv_arr = sys.argv.copy()
argv_arr.reverse()
run_mode = "main"
while len(argv_arr) > 0:
    arg = argv_arr.pop()
    if arg == "-c" or arg == "--config":
        try:
            conf_file = argv_arr.pop();
            continue
        except:
            raise Exception("Uncomplete config argument.")
    if arg == "-g" or arg == "--get-record-id":
        run_mode = "get-record-id"
        continue
    if arg == "-?" or arg == "--help":
        print('''
Usage: %s [options]
  -c, --config:
    Custom config file path.
  -g, --get-record-id:
    Get record IDs of these records which are marked null only, do not update.
  -?, --help:
    Show this help.
''' % sys.argv[0])
        exit(0)

conf_file_in = open(conf_file, 'r')
try:
    conf_json_raw = conf_file_in.read()
except:
    raise Exception("Unable to find config.")
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
    get_IPv6_site = conf_json_obj['get_IPv6_site']
except:
    get_IPv6_site = 'ipv6.ip.sb'
try:
    aliyun_endpoint = conf_json_obj['aliyun_endpoint']
except:
    aliyun_endpoint = 'cn-hangzhou'
try:
    debug = conf_json_obj['debug']
    if debug != True and debug != False:
        debug = False
except:
    debug = False

def check_records(dns_domain):
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyun_endpoint)
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format('json')
    result = clt.do_action_with_exception(request)
    return result.decode()


def old_ip(rc_record_id):
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyun_endpoint)
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(rc_record_id)
    request.set_accept_format('json')
    result = clt.do_action_with_exception(request)
    result = json.JSONDecoder().decode(result.decode())
    result = result['Value']
    return result


def update_dns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyun_endpoint)
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(dns_rr)
    request.set_Type(dns_type)
    request.set_Value(dns_value)
    request.set_RecordId(dns_record_id)
    request.set_TTL(dns_ttl)
    request.set_accept_format(dns_format)
    result = clt.do_action_with_exception(request)
    return result


def get_local_IPv6_address():
    get_IPV6_process = subprocess.Popen(["curl", "-6", "--silent", get_IPv6_site], stdout=subprocess.PIPE)
    output = (get_IPV6_process.stdout.read())
    m = output.decode().split("\n")[0]
    if m != '':
        return m
    else:
        return None

def get_record_id():
    bool_got_ids = False
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

def main():
    bool_no_change = True
    rc_value = get_local_IPv6_address()
    for domain in rc_domain:
        for info in rc_info[domain]:
            rc_rr = info['rc_rr']
            rc_record_id = info['rc_record_id']
            if rc_record_id is None:
                rc_record_id_json_raw = check_records(domain)
                rc_record_id_json_obj = JSONDecoder.decode(rc_record_id_json_raw)
                if debug is True:
                    sys.stderr.write("Returned JSON:\n %s\n" % rc_record_id_json_raw)
                for record in rc_record_id_json_obj['DomainRecords']['Record']:
                    if record['RR'] == rc_rr and record['Type'] == rc_type and record['Locked'] == False and record['Status'] == "ENABLE":
                        rc_record_id = record['RecordId']
                        info['rc_record_id'] = record['RecordId']
                        bool_update_conf = True
                        break
                if rc_record_id is None:
                    raise Exception('Cannot get record id, please add an AAAA record first, or unlock the existed record.')
            rc_ttl = info['rc_ttl']
            rc_value_old = old_ip(rc_record_id)
            if rc_value is None:
                raise Exception('Emmm... Seems like that you do not have IPv6 address or your network is down')
            if rc_value_old != rc_value:
                rc_result = update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, 'json')
                bool_no_change = False
                if debug is True:
                    sys.stderr.write("Returned JSON:\n %s\n" % rc_result)
                print("DNS AAAA record updated for %s.%s (RecordId: %s)" % (rc_rr, domain, rc_record_id))
                print("old record is %s, new record is %s\n" % (rc_value_old, rc_value))
    if bool_no_change is True:
        print("No records changed.")

if __name__ == '__main__':
    if run_mode == "get-record-id":
        get_record_id()
    else:
        main()