#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import httpretty
import json
from pyzbx import ZabbixAPI


class Testpyzbx(unittest.TestCase):

    zabbix_url = "http://example.com"
    zabbix_user = "Admin"
    Zabbixpw_pw = "zabbix"

    @httpretty.activate
    def test_login(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://example.com/api_jsonrpc.php",
            body=json.dumps({
                "jsonrpc": "2.0",
                "result": "5800f2978690fb5d72437b4a19dd7ac9",
                "id": 0
            }),
        )

        zabbix_api = ZabbixAPI(self.zabbix_url, self.zabbix_user, self.Zabbixpw_pw)

        # Check request
        self.assertEqual(
            json.loads(httpretty.last_request().body.decode("utf-8")),
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {"user": "Admin", "password": "zabbix"},
                "auth": None,
                "id": 1,
            }
        )
        self.assertEqual(
            httpretty.last_request().headers["content-type"],
            "application/json-rpc"
        )
        self.assertEqual(
            httpretty.last_request().headers["user-agent"],
            "python/pyzbx"
        )

    @httpretty.activate
    def test_host_get(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://example.com/api_jsonrpc.php",
            body=json.dumps({
                "jsonrpc": "2.0",
                "result": "5.2.6",
                "id": 0
            }),
        )

        zabbix_api = ZabbixAPI(self.zabbix_url, self.zabbix_user, self.Zabbixpw_pw)
        test_json = {
                "jsonrpc": "2.0",
                "method": "apiinfo.version",
                "params": [],
                "auth": "",
                "id": 0
        }
        test_datas = zabbix_api.call_api(test_json)

        # Check request
        self.assertEqual(
            json.loads(httpretty.last_request().body.decode('utf-8')),
            {
                "jsonrpc": "2.0",
                "method": "apiinfo.version",
                "params": [],
                "id": 0
            }
        )

        # Check response
        self.assertEqual(test_datas, "5.2.6")
