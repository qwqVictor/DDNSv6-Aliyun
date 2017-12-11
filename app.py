from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest
from aliyunsdkcore import client
import json
import re
import subprocess

# 请先填写
accessKeyId = ""
accessKeySecret = ""

# 如果选择n，则运行程序后仅现实域名信息，并不会更新记录，用于获取解析记录ID。
# 如果选择y，则运行程序后不显示域名信息，仅更新记录
i_know_record_id = 'n'

# 请填写你的一级域名
rc_domain = 'xxx.xxx'

# 请填写你的解析记录
rc_rr = ''

# 请填写你的记录类型
rc_type = 'AAAA'

# 请填写解析记录ID，如果没有请将i_know_record_id 设置为n以获取rc_record_id
rc_record_id = ''
rc_record_RequestId = 'D4'
# 请填写解析有效生存时间TTL，单位：秒
rc_ttl = '600'

rc_format = 'json'


def check_records(dns_domain):
    clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request)
    print(result.decode())
    return result


def old_ip():
    clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(rc_record_id)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request)
    result = json.JSONDecoder().decode(result.decode())
    result = result['Value']
    return result


def update_dns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    print(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format)
    clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(dns_rr)
    request.set_Type(dns_type)
    request.set_Value(dns_value)
    request.set_RecordId(dns_record_id)
    request.set_TTL(dns_ttl)
    request.set_accept_format(dns_format)
    result = clt.do_action_with_exception(request)
    return result


def get_Local_ipv6_address():
    getIPV6_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
    output = (getIPV6_process.stdout.read())
    ipv6_pattern = '(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'
    m = re.search(ipv6_pattern, str(output))
    if m is not None:
        return m.group()
    else:
        return None


if __name__ == '__main__':
    if i_know_record_id == 'n':
        check_records(rc_domain)
    elif i_know_record_id == 'y':
        rc_value_old = old_ip()
        rc_value = get_Local_ipv6_address()
        if rc_value is None:
            raise Exception('You do not have ipv6 address')
        print(rc_value, rc_value_old)
        if rc_value_old == rc_value:
            print('The specified value of parameter Value is the same as old')
        else:
            update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format)
