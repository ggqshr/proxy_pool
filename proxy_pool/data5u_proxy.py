import json
import logging
from random import choice
from time import sleep
import yaml
import requests
from os.path import join, dirname
from proxy_pool import IpPool
import threading
import logging.config

with open(join(dirname(__file__), "logconf.yaml"), "r") as f:
    logconfig = yaml.load(f, Loader=yaml.FullLoader)  # 加载日志配置
logging.config.dictConfig(logconfig)  # 设置日志
logger = logging.getLogger("data5u")


class Data5UProxy(IpPool):
    def __init__(self, api_url,enable_log=True):
        super().__init__(api_url)
        if not enable_log:
            logger.setLevel(logging.INFO)

    def start(self):
        GetIpThread(self.api_url, self.ip_pool, self.cond).start()
        pass

    def _request_ip(self):
        logger.info("请求新的ip")
        res = requests.get(self.api_url).content.decode()
        res = json.loads(res)
        if res['success']:
            all_data = res['data']
            for dd in all_data:
                self.ip_pool.add(f"{dd['ip']}:{dd['port']}")
                with self.cond:
                    self.cond.notify_all()
                logger.info("请求成功")

    def get_ip(self):
        with self.cond:
            self.cond.wait_for(self._has_ip)
            return choice(list(self.ip_pool))

    def report_baned_ip(self, ip):
        logger.info(f"remove {ip} from pool!")
        self.ip_pool.discard(ip)
        logger.info(f"now the pool is {self.ip_pool}")

    def report_bad_net_ip(self, ip):
        pass


class GetIpThread(threading.Thread):
    def __init__(self, api_url, ip_pool: set, cond: threading.Condition):
        super().__init__(daemon=True)
        self.url = api_url
        self.ip_pool = ip_pool
        self.cond = cond

    def run(self) -> None:
        while True:
            logger.debug("刷新新的ip")
            res = requests.get(self.url).content.decode()
            res = json.loads(res)
            if res['success']:
                all_data = res['data']
                for dd in all_data:
                    self.ip_pool.add(f"{dd['ip']}:{dd['port']}")
                    logger.debug("请求成功")
                    with self.cond:
                        self.cond.notify_all()
            sleep(5)
