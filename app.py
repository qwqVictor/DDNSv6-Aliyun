# -*- coding: utf-8 -*-
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest
from aliyunsdkcore import client
import json
import re
import subprocess

rc_type = 'AAAA'
rc_record_RequestId = 'D4'
rc_format = 'json'
get_IPv6_site = 'ipv6.ip.sb'
aliyunEndpoint = 'cn-hangzhou'
def check_records(dns_domain):
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyunEndpoint)
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request)
    print(result.decode())
    return result


def old_ip(rc_record_id):
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyunEndpoint)
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(rc_record_id)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request)
    result = json.JSONDecoder().decode(result.decode())
    result = result['Value']
    return result


def update_dns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    print(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format)
    clt = client.AcsClient(accessKeyId, accessKeySecret, aliyunEndpoint)
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
    get_IPV6_process = subprocess.Popen(["curl", "-6", get_IPv6_site], stdout=subprocess.PIPE)
    output = (getIPV6_process.stdout.read())
    m = output.decode().split("\n")[0]
    if m != '':
        return m
    else:
        return None


if __name__ == '__main__':
    if i_know_record_id == 'n':
        for rc_domain_e in rc_domain:
          check_records(rc_domain_e);
    elif i_know_record_id == 'y':
        rc_value = get_local_IPv6_address()
        for domain in rc_domain:
            for info in rc_info[domain]:
                rc_rr = info['rc_rr']
                rc_record_id = info['rc_record_id']
                rc_ttl = info['rc_ttl']
                rc_value_old = old_ip(rc_record_id)
                if rc_value is None:
                    raise Exception('You do not have ipv6 address')
                print(rc_value, rc_value_old)
                if rc_value_old == rc_value:
                    print('The specified value of parameter Value is the same as old')
                else:
                    update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format)