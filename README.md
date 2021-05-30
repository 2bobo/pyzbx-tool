###### pyzbx_tool
This Python module can directly use JSON from [Zabbix API documentation](https://www.zabbix.com/documentation/current/manual/api).
It also allows you to use ZabbixSender from Python.

## Requirements
- Tested against Zabbix 5.0-5.2
- Pyhton 3.8

## Getting Started
### install
```
gft clone git@github.com:2bobo/pyzbx.git
cd pyzbx
python setup.py install
```

### API usage
```python
import pyzbxtool

zbx_api = pyzbxtool.ZabbixAPI("http://example.com", "Admin", "zabbix")
version_json = {
    "jsonrpc": "2.0",
    "method": "apiinfo.version",
    "params": [],
    "auth": "",
    "id": 1
}

version = zbx_api.call_api(version_json)
print(version)

```

### Sender usage
```python
import pyzbxtool

zbx_sender = pyzbxtool.ZabbixSender("zabbix_server_ip", "10051")
zbx_sender.add("host", "key", "value")
result = zbx_sender.send()
print(result)

```
