#!/usr/bin/env python3
# -*- coding:gbk -*-

import re
import requests
import threading

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}


# 复写Thread类,获取多线程的返回值
class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# 获取代理IP列表函数
def get_ip():
    url = "http://www.66ip.cn/mo.php?sxb=&tqsl=7000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
    ip = requests.get(url, headers=headers)
    proxy_ip = re.findall(r'\d.*?(?=<br)', ip.text)
    return proxy_ip  # 返回爬到的代理IP列表


# 验证代理是否可用函数
def test_ip(lists, site):
    proxy_ok_ip = []
    for ip in lists:
        proxy_host = ip
        try:
            proxy_temp = {"http": proxy_host, "https": proxy_host}
            res = requests.get(site, headers=headers, proxies=proxy_temp, timeout=5).status_code
            if 200 <= res < 300:  # 判断网站返回的状态码
                print(res, proxy_host + "  is OK")
                proxy_ok_ip.append(proxy_host)
            else:
                print(proxy_host + "  is GG")
        except Exception:
            print(proxy_host + "  is GG")
            continue
    return proxy_ok_ip  # 返回通过验证的代理IP列表


# 列表写入TXT文件函数：filename为写入TXT文件的路径，data为要写入数据列表，默认保存至运行目录下的‘ip.txt’
def text_save(filename, data):
    file = open(filename, 'w+')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("代理信息保存文件成功!")


if __name__ == '__main__':
    print("正在获取代理IP中请稍等片刻..." + '\n' + "如没有结果请检查是否可以访问http://www.66ip.cn/")
    ip_list = get_ip()
    value = input("共获取到" + str(len(ip_list)) + "个代理IP，是否验证可用性（默认否，输入任意字符开始验证）：")
    if value:
        site = input("请输入要访问的站点：")
        thread_num = 500  # 默认500线程
        thread_count = len(ip_list) // thread_num  # 一个线程验证IP数
        final = []  # 存放多线程结束后的多维列表
        one = []  # 可用代理IP的一维列表

        threads = []  # 定义一个线程池
        for i in range(thread_num):
            i *= thread_count
            # 创建新线程,添加到线程池
            threads.append(MyThread(test_ip, args=(ip_list[i+1:i+thread_count], site)))

        # 开启新线程
        for t in threads:
            t.start()

        # 等待所有线程完成
        for t in threads:
            t.join()

        # 合并多个线程的列表
        for t in threads:
            final.append(t.get_result())

        # 遍历多维列表
        for j in final:
            for k in j:
                one.append(k)
        # print(one)
        text_save("验证过的IP列表.txt", one)
    else:
        # print(ip_list)
        text_save("未验证的IP列表.txt", ip_list)