# DDNSv6-Aliyun
使用阿里云解析的简易 IPv6 DDNS 客户端。

原作者的版本仅适用于 Python3，Windows，这个版本稍作了一点改进，使其得以支持 Linux/macOS，并优化了程序结构。

这个项目目前没有稳定版本，仍处于测试阶段。

### Requirements
- Python 3.x
- Crypto 库
- curl with IPv6 support

### Manual
复制 `config_sample.json` 为 `config.json`。  

在 `config.json` 中根据要求填写配置文件。  

保证当前工作目录下存在 `config.json` 的情况下执行 `app.py`。

### Configuration
#### 示例
```json
{
    "accessKeyId": "KEYKKKKKKKKKK",
    "accessKeySecret": "SECRETSSSSSSSSSSSSS",
    "rc_info": {
        "domain1.com": [
            {
                "rc_rr": "@",
                "rc_ttl": "120",
                "rc_record_id": null
            }
        ],
        "domain2.com": [
            {
                "rc_rr": "@",
                "rc_ttl": "120",
                "rc_record_id": null
            },
            {
                "rc_rr": "ipv6",
                "rc_ttl": "360",
                "rc_record_id": null
            }
        ]
    },
    "get_IPv6_site": "ipv6.ip.sb",
    "aliyun_endpoint": "cn-hangzhou"
}
```
#### 字段解释
`accessKeyId` 和 `accessKeySecret` 是 API 密钥，请在阿里云申请后正确填入。  
`rc_info` 是主要的字段，其结构是一个字典。  
这个字典每一项的 key 代表主域名，key 对应的 value 是一个数组，数组的元素类型为字典，代表多个不同的子域名。  
子域名字典的结构是:
- `rc_rr`: 子域名名称，如果为根域则填写 `@`，在使用这个程序之前，您需要先创建一个该子域的 AAAA 记录。
- `rc_ttl`: 子域名解析记录 TTL，单位是秒。
- `rc_record_id`: 子解析记录 ID，您可能不知道解析记录 ID 是什么，如果您不需要对该子域名解析多个 AAAA 记录，则可以填写 `null` 让程序自动为您更新。请注意，如果您有多个 AAAA 记录，那么您需要先将这个字段置 null，然后在 `config.json` 存在的目录下执行 `get_record_id.py` 来获取解析记录 ID 并填入，否则可能第一个发现的 AAAA 记录会被更新。

`get_IPv6_site` 字段是获取您的 IPv6 地址的 URL，您也可以自行搭建 IPv6 地址获取 API，我们默认使用 `ipv6.ip.sb`。

`aliyun_endpoint` 字段是使得程序请求这个字段规定地域的阿里云 API 服务器。
### Todo List
- [x] 自动获取解析记录 ID
- [x] 配置文件改用更加容易编写的 JSON 格式

~~考完 NOIP 我会回来继续更新的。（咕咕咕警告~~  
我没咕，我没咕！
### License
GNU Affero General Public License 3.0