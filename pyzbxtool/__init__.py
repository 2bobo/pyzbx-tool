#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Zabbix API

"""

import urllib
import requests
import json
import datetime
import socket
import struct
import time
import re


class ZabbixAPI(object):
    """Zabbix API 利用クラス
    Zabbix APIを利用するためのクラス

    """

    def __init__(
            self,
            zbx_url="http://localhost/zabbix",
            zbx_userid="",
            zbx_passwd=""
    ):
        """
        get Zabbix API auth key

        Args:
            zbx_url (str): Zabbix Server URL
            zbx_userid(str): API user
            zbx_passwd(str): API user password
        """

        self.zbx_url = urllib.parse.urljoin(zbx_url, "api_jsonrpc.php")
        self.zbx_auth = None
        self.headers = {"Content-Type": "application/json-rpc", "user-agent": "python/pyzbx"}

        # Create JSON for auth key generation
        auth_post = {
            'jsonrpc': '2.0',
            'method': 'user.login',
            'params': {
                'user': zbx_userid,
                'password': zbx_passwd},
            'auth': self.zbx_auth,
            'id': 1}
        # Create auth key
        self.zbx_auth = self.call_api(auth_post)
        if type(self.zbx_auth) == int:
            print(f"http Error [{ self.zbx_auth }]" )
            exit()
        self.cookie = dict(zbx_sessionid=self.zbx_auth)

    def call_api(self, apireq):
        """API 実行関数
        JSONの詳細はZabbix ドキュメントを参照
        https://www.zabbix.com/documentation/3.0/manual/api

        Args:
            apireq (str): APIリクエストJSON
        Returns:
            str: API実行結果JSON
        """
        if apireq["method"] == "apiinfo.version":
            apireq.pop("auth")
        else:
            apireq["auth"] = self.zbx_auth

        apireq_json = json.dumps(apireq)
        r = requests.post(self.zbx_url, data=apireq_json, headers=self.headers)
        if r.status_code != 200:
            return r.status_code
        else:
            rjsondata = r.json()

        if "error" in rjsondata:
            return rjsondata["error"]
        elif "result" in rjsondata:
            return rjsondata["result"]
        else:
            return None

    # グラフ取得
    def get_chart(
            self,
            g_period="3600",
            g_stime="20180704103038",
            g_itemids="",
            g_type="0",
            g_updateprofile="1",
            g_profileidx="web.item.graph",
            g_profileidx2="",
            g_width="1782"
    ):
        """Zabbix2系 最新の値のグラフ取得関数
        Zabbix2系までの最新の値で表示されるグラフの画像を取得

        Args:
            g_period (str): グラフ期間
            g_stime (str): グラフ開始時間
            g_itemids (str): アイテムID
            g_type (str): タイプ
            g_updateprofile (str):
            g_profileidx (str):
            g_profileidx2 (str):
            g_width (str): 画像の横幅

        Returns:
            bytearray: グラフ画像データ

        """

        graph_url = urllib.parse.urljoin(self.zbx_url, "chart.php")
        params = {
            "period": g_period,
            "stime": g_stime,
            "itemids[0]": g_itemids,
            "type": g_type,
            "updateProfile": g_updateprofile,
            "profileIdx": g_profileidx,
            "profileIdx2": g_profileidx2,
            "width": g_width
        }
        graph = requests.get(graph_url, cookies=self.cookie, params=params)
        return graph.content

    def get_chart3(
            self,
            g_graphid="",
            g_period="3600",
            g_stime="20180704103038",
            g_updateprofile="1",
            g_profileidx="web.item.graph",
            g_profileidx2="",
            g_width="1782"
    ):
        """Zabbix3系 グラフ取得関数
        Zabbix3系以上でグラフの画像を取得

        Args:
            g_graphid (str): グラフID
            g_period (str): グラフ期間
            g_stime (str): グラフ開始時間
            g_itemids (str): アイテムID
            g_type (str): タイプ
            g_updateprofile (str):
            g_profileidx (str):
            g_profileidx2 (str):
            g_width (str): 画像の横幅

        Returns:
            bytearray: グラフ画像データ

        """

        graph_url = urllib.parse.urljoin(self.zbx_url, "chart2.php")
        params = {
            "graphid": g_graphid,
            "period": g_period,
            "stime": g_stime,
            "updateProfile": g_updateprofile,
            "profileIdx": g_profileidx,
            "profileIdx2": g_profileidx2,
            "width": g_width
        }
        graph = requests.get(graph_url, cookies=self.cookie, params=params)
        return graph.content

    def get_chart4(
            self,
            g_graphid="",
            g_from="2019-06-01 00:00:00",
            g_to="2019-07-01 00:00:00",
            g_profileidx="web.graphs.filter",
            g_profileidx2="",
            g_width="1782"
    ):
        """Zabbix4系以降用 グラフ取得関数
        Zabbix4系以上でグラフの画像を取得

        Args:
            g_graphid (str): グラフID
            g_from (str): グラフ開始日時
            g_to (str): グラフ終了日時
            g_profileidx (str):
            g_profileidx2 (str):
            g_width (str): グラフ画像幅

        Returns:
            bytearray: グラフ画像データ
        """

        graph_url = urllib.parse.urljoin(self.zbx_url, "chart2.php")
        params = {
            "graphid": g_graphid,
            "from": g_from,
            "to": g_to,
            "profileIdx": g_profileidx,
            "profileIdx2": g_profileidx2,
            "width": g_width
        }
        graph = requests.get(graph_url, cookies=self.cookie, params=params)
        return graph.content


class ZabbixSender(object):
    """Zabbix Sender クラス
    ZabbixSenderを利用可能にするクラス
    """

    def __init__(self, server='127.0.0.1', port='10051'):
        """
        データを送信するZabbixサーバーの情報を指定

        Args:
            server (str): ZabbixServerのIP/hostname(デフォルト値:127.0.0.1)
            port (ste): Zabbixのポート番号(デフォルト値:10051)
        """

        self.server = server
        self.port = port
        self.zbx_sender_data = {u'request': u'sender data', u'data': []}

    def add(self, host, key, value, clock=None):
        """データ追加関数
        ZabbixSenderで送信するデータを追加する関数

        Args:
            host (str): Zabbixホスト名
            key (str): 送信するアイテムのキー
            value (str): 送信するアイテムの値
            clock (int):

        Returns: None

        """
        if clock is None:
            clock = datetime.datetime.now().timestamp()

        data = {"host": str(host),
                "key": str(key),
                "value": str(value),
                "clock": int(clock)
                }
        self.zbx_sender_data["data"].append(data)

    def clean_packet(self):
        """データクリア関数
        addで追加されたデータをすべて削除する関数

        Args: None
        Returns: None

        """

        self.zbx_sender_data = {u'request': u'sender data', u'data': []}

    def send(self):
        """送信関数
        addされたデータをZabbixへ送信する関数

        Args: None
        Returns:
            json: 送信結果データ

        """
        s = socket.socket()
        try:
            s.connect((self.server, int(self.port)))
        except Exception as e:
            print(e)
        data = str(json.dumps(self.zbx_sender_data)).encode('utf-8')
        packet = b"ZBXD\1" + struct.pack('<Q', len(data)) + data
        s.send(packet)
        time.sleep(1)

        status = s.recv(1024).decode('utf-8')
        re_status = re.compile('(\{.*\})')
        status = re_status.search(status).groups()[0]

        self.clean_packet()
        s.close()

        return status
        #return json.loads(status)

