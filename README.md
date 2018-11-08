# DDNSv6-Aliyun
使用阿里云解析的简易 IPv6 DDNS 客户端。

原作者的版本仅适用于 Python3，Windows，这个版本稍作了一点改进，使其得以支持 Linux/macOS。

同时，配置方面有较大的变化，配置文件从 `app.py` 中分离，并且可以同时添加多个域名。

### Requirements
- Python 3.x
- Crypto 库

### Manual
在 `config_user.py` 中根据要求编写配置文件。

然后使用 `run.sh` 执行。

### Todo List
- [ ] 自动获取解析记录 ID
- [ ] 配置文件改用更加容易编写的 JSON 格式
- [ ] 添加 Windows 版启动脚本

考完 NOIP 我会回来继续更新的。~~（咕咕咕警告~~
### License
GPLv3