import json
import logging
from random import choice
from time import sleep
import requests
from proxy_pool import IpPool
import threading


class Data5UProxy(IpPool):
    def __init__(self, api_url):
        super().__init__(api_url)
        self.refresh_thread = GetIpThread(self.api_url, self.ip_pool, self.cond)

    def start(self):
        self.refresh_thread.start()

    def _request_ip(self):
        logging.info("请求新的ip")
        res = requests.get(self.api_url).content.decode()
        res = json.loads(res)
        if res['success']:
            all_data = res['data']
            for dd in all_data:
                self.ip_pool.add(f"{dd['ip']}:{dd['port']}")
                with self.cond:
                    self.cond.notify_all()
                logging.info("请求成功")

    def get_ip(self):
        with self.cond:
            self.cond.wait_for(self._has_ip)
            return choice(list(self.ip_pool))

    def report_baned_ip(self, ip):
        logging.debug(f"remove {ip} from pool!")
        self.ip_pool.discard(ip)
        logging.debug(f"now the pool is {self.ip_pool}")

    def report_bad_net_ip(self, ip):
        pass

    def close(self):
        self.refresh_thread.terminate()


class GetIpThread(threading.Thread):
    def __init__(self, api_url, ip_pool: set, cond: threading.Condition):
        super().__init__(daemon=True)
        self.url = api_url
        self.ip_pool = ip_pool
        self.cond = cond
        self.keep_run = True

    def run(self) -> None:
        while self.keep_run:
            if len(list(self.ip_pool)) < 5:
                logging.debug("刷新新的ip")
                res = requests.get(self.url).content.decode()
                res = json.loads(res)
                if res['success']:
                    all_data = res['data']
                    for dd in all_data:
                        self.ip_pool.add(f"{dd['ip']}:{dd['port']}")
                        logging.debug("请求成功")
                        with self.cond:
                            self.cond.notify_all()
            sleep(5)

    def terminate(self):
        self.keep_run = False
        logging.debug("关闭刷新ip线程")
