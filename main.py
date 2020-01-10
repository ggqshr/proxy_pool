import proxy_pool as proxy

if __name__ == '__main__':
    a = proxy.Data5UProxy(
        "http://api.ip.data5u.com/dynamic/get.html?order=e0dc70ee5d127a3f6c7f1013c5b28dd2&json=1&sep=3")
    a.start()
    b = a.get_ip()
    print(b)
