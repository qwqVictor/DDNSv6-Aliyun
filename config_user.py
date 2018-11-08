# -*- coding: utf-8 -*-
# 请先填写
accessKeyId = "KEYKKKKKKKKKK"
accessKeySecret = "SECRETSSSSSSSSSSSSS"

# 如果选择n，则运行程序后仅显示域名信息，并不会更新记录，用于获取解析记录ID。
# 如果选择y，则运行程序后不显示域名信息，仅更新记录
i_know_record_id = 'n'

# 请填写你的一级域名
rc_domain = ['domain1.com', 'domain2.org']

# 请填写你的解析记录
rc_info = {\
    'domain1.com': [\
        { 'rc_rr': '@', 'rc_record_id': '2002200220022002', 'rc_ttl': '120'}\
    ],\
    'domain2.org': [\
        { 'rc_rr': '@', 'rc_record_id': '2002200220022002', 'rc_ttl': '120'},\
        { 'rc_rr': 'ipv6', 'rc_record_id': '2002200220022002', 'rc_ttl': '360'}\
    ]\
}