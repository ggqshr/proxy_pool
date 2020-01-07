import proxy_pool as proxy

if __name__ == '__main__':
    a = proxy.XunProxy(
        "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=2eeedc14918546f087abcddafd5ee37d&orderno=YZ20196121637TQppQw&returnType=2&count=3")
    a.start()
    b = a.get_ip()
    print(b)
