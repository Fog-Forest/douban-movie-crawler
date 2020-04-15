#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import time
import requests
import threading
from bs4 import BeautifulSoup

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


# 获取普通代理IP函数
def get_ip():
    proxy_ip = []
    # 66免费代理
    try:
        url1 = 'http://www.66ip.cn/mo.php?sxb=&tqsl=7000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
        ip1 = requests.get(url1, headers=headers, timeout=10)
        proxy_ip1 = re.findall(r'\d.*?(?=<br)', ip1.text)
        for a in proxy_ip1:
            proxy_ip.append(a)
    except Exception:
        pass

    # 西刺代理
    try:
        for page in range(1, 5):  # 爬取多少页
            url2 = 'https://www.xicidaili.com/nt/' + str(page)
            ip2 = requests.get(url2, headers=headers, timeout=10)
            # print(ip2.text)
            soupIP = BeautifulSoup(ip2.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                proxy_ip.append(ip + ':' + port)
            time.sleep(6)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 快代理
    try:
        for page in range(1, 6):  # 爬取多少页
            url3 = 'https://www.kuaidaili.com/free/intr/' + str(page)
            ip3 = requests.get(url3, headers=headers, timeout=10)
            # print(ip3.text)
            soupIP = BeautifulSoup(ip3.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxy_ip.append(ip + ':' + port)
            time.sleep(5)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 云代理
    try:
        for page in range(1, 7):  # 爬取多少页
            url4 = 'http://www.ip3366.net/free/?stype=2&page=' + str(page)
            ip4 = requests.get(url4, headers=headers, timeout=10)
            # print(ip4.text)
            soupIP = BeautifulSoup(ip4.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxy_ip.append(ip + ':' + port)
            time.sleep(5)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 89免费代理（不知道是不是高匿）
    try:
        url5 = 'http://www.89ip.cn/tqdl.html?api=1&num=3000&port=&address=&isp='
        ip5 = requests.get(url5, headers=headers, timeout=10)
        proxy_ip1 = re.findall(r'(\d+.\d+.\d+.\d+:\d+)', ip5.text)
        for a in proxy_ip1:
            proxy_ip.append(a)
    except Exception:
        pass

    # 小幻代理(请手动获取):https://ip.ihuan.me/
    return proxy_ip


# 获取匿名代理IP函数
def get_anonymous_ip():
    proxy_anonymous_ip = []
    # 66免费代理
    try:
        url1 = 'http://www.66ip.cn/nmtq.php?getnum=3000&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip'
        ip1 = requests.get(url1, headers=headers, timeout=10)
        proxy_ip1 = re.findall(r'\d.*?(?=<br)', ip1.text)
        for a in proxy_ip1:
            proxy_anonymous_ip.append(a)
    except Exception:
        pass

    # 西刺代理
    try:
        for page in range(1, 5):  # 爬取多少页
            url2 = 'http://www.xicidaili.com/nn/' + str(page)
            ip2 = requests.get(url2, headers=headers, timeout=10)
            # print(ip2.text)
            soupIP = BeautifulSoup(ip2.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                proxy_anonymous_ip.append(ip + ':' + port)
            time.sleep(6)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 快代理
    try:
        for page in range(1, 6):  # 爬取多少页
            url3 = 'https://www.kuaidaili.com/free/inha/' + str(page)
            ip3 = requests.get(url3, headers=headers, timeout=10)
            # print(ip3.text)
            soupIP = BeautifulSoup(ip3.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxy_anonymous_ip.append(ip + ':' + port)
            time.sleep(5)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 云代理
    try:
        for page in range(1, 7):  # 爬取多少页
            url4 = 'http://www.ip3366.net/free/?stype=1&page=' + str(page)
            ip4 = requests.get(url4, headers=headers, timeout=10)
            # print(ip4.text)
            soupIP = BeautifulSoup(ip4.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxy_anonymous_ip.append(ip + ':' + port)
            time.sleep(5)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 齐云代理
    try:
        for page in range(1, 30):  # 爬取多少页
            url5 = 'https://www.7yip.cn/free/?action=china&page=' + str(page)
            ip5 = requests.get(url5, headers=headers, timeout=10)
            # print(ip5.text)
            soupIP = BeautifulSoup(ip5.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxy_anonymous_ip.append(ip + ':' + port)
            # time.sleep(5)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception:
        pass

    # 小幻代理(请手动获取):https://ip.ihuan.me/
    return proxy_anonymous_ip


# 检测输入是否正确函数
def check_input(fsite, fword, fcode):
    check = requests.get(fsite, headers=headers, timeout=8)
    if fcode == "2":
        check.encoding = 'gbk'
    else:
        check.encoding = 'utf-8'
    if fword in check.text:  # 判断关键字符串是否在网站源码中
        print("\n验证成功，验证网址和关键字符串可用，开始代理IP验证！")
        return True
    else:
        print("\n验证失败，验证网址和关键字符串不可用，请重新输入！")
        return False


# 验证代理是否可用函数
def test_ip(lists, site, word, code):
    proxy_ok_ip = []
    for ip in lists:
        proxy_host = ip
        try:
            proxy_temp = {"http": proxy_host, "https": proxy_host}
            res = requests.get(site, headers=headers, proxies=proxy_temp, timeout=8)
            if code == "2":
                res.encoding = 'gbk'
            else:
                res.encoding = 'utf-8'
            if word in res.text:  # 判断关键词是否在网站源码中
                print(res, proxy_host + "  is OK")
                proxy_ok_ip.append(proxy_host)
            else:
                print(proxy_host + "  is BOOM")
        except Exception:  # 超时或异常
            print(proxy_host + "  is BOOM")
            continue
    return proxy_ok_ip  # 返回通过验证的代理IP列表


# 列表写入TXT文件函数：filename为写入TXT文件的路径，data为要写入数据列表
def text_save(filename, data):
    file = open(filename, 'w+')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("代理IP信息保存文件成功，请查看当前运行目录！")


# 列表去重函数
def ip_list(lists):
    temp = []
    for i in lists:
        if not i in temp:
            temp.append(i)
    return temp


if __name__ == '__main__':
    choose = input("请选择你要获取的代理IP类型(1.普通(默认) 2.高匿)：")
    if choose == 2:
        print("正在获取高匿代理IP中请稍等片刻，大概3分钟...")
        ip_list = ip_list(get_anonymous_ip())  # 去重
    else:
        print("正在获取普通代理IP中请稍等片刻，大概3分钟...")
        ip_list = ip_list(get_ip())  # 去重

    # 是否验证可用性？
    value = input("共获取到" + str(len(ip_list)) + "个代理IP，是否验证可用性（默认否，输入任意字符开始验证）：")
    if value:  # 验证可用性✔
        while 1:  # 首次验证检测输入是否正确，不使用代理IP
            site = input("请输入要访问的站点：")
            code = input("请输入验证站点的编码格式(1.UTF-8(默认) 2.GBK)：")
            word = input("请输入验证站点内的关键字符串，如 “https://www.baidu.com” 中有关键字符串 “百度一下” ：")
            if check_input(site, word, code):
                break
            else:
                print('\n\n')

        # 多线程验证开始，GO! GO! GO!
        thread_num = 500  # 默认500线程
        thread_count = len(ip_list) // thread_num  # 一个线程验证IP数

        final = []  # 存放多线程结束后的多维列表
        one = []  # 可用代理IP的一维列表
        threads = []  # 定义一个线程池
        for i in range(thread_num):
            i *= thread_count
            # 创建新线程,添加到线程池
            threads.append(MyThread(test_ip, args=(ip_list[i+1:i+thread_count], site, word, code)))

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
        print("可用IP总数为" + str(len(one)) + "个")
        text_save("验证过的IP列表.txt", one)
    else:  # 不验证可用性×
        # print(ip_list)
        text_save("未验证的IP列表.txt", ip_list)