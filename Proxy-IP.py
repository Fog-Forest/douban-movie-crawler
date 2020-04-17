#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import time
import html5lib
import requests
import threading
from bs4 import BeautifulSoup

# 全局变量
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

proxy_ip = []  # 代理IP数组
proxy_ok_ip = []  # 验证后的代理IP数组


# 复写Thread类
class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


# 使用正则获取代理IP函数(API提取形式):API提取链接、备注名称
def ip_json(link, text):
    global proxy_ip
    ip_num = 0
    try:
        url = str(link)
        response = requests.get(url, headers=headers, timeout=8)
        temp = re.findall(r'(\d+.\d+.\d+.\d+:\d+)', response.text)
        for ip in temp:
            ip_num += 1  # 自增计算IP数
            proxy_ip.append(ip)
    except Exception as e:
        print(e)
    print(str(text) + "获取到" + str(ip_num) + "个代理IP")


# 使用HTML解析获取代理IP函数【一】(源码IP和端口在一起且在第1个<td>标签内):网页链接、备注名称、爬取页数、爬取速度
def ip_html1(link, text, page, speed):
    global proxy_ip
    ip_num = 0
    try:
        for a in range(1, page):  # 爬取多少页
            url = str(link) + str(a)
            response = requests.get(url, headers=headers, timeout=8)
            # print(response.text)
            soupIP = BeautifulSoup(response.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                ip_num += 1  # 自增计算IP数
                tds = tr.find_all('td')
                # print(tds)
                ip = tds[0].text.strip()
                proxy_ip.append(ip)
            time.sleep(speed)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception as e:
        print(e)
    print(str(text) + "获取到" + str(ip_num) + "个代理IP")


# 使用HTML解析获取代理IP函数【二】(源码IP和端口不在一起,IP在第1个<td>标签内,端口在第2个<td>标签内):网页链接、备注名称、爬取页数、爬取速度
def ip_html2(link, text, page, speed):
    global proxy_ip
    ip_num = 0
    try:
        for a in range(1, page):  # 爬取多少页
            url = str(link) + str(a)
            response = requests.get(url, headers=headers, timeout=8)
            # print(response.text)
            soupIP = BeautifulSoup(response.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                ip_num += 1  # 自增计算IP数
                tds = tr.find_all('td')
                # print(tds)
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxy_ip.append(ip + ':' + port)
            time.sleep(speed)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception as e:
        print(e)
    print(str(text) + "获取到" + str(ip_num) + "个代理IP")


# 使用HTML解析获取代理IP函数【三】(源码IP和端口不在一起,IP在第2个<td>标签内,端口在第3个<td>标签内):网页链接、备注名称、爬取页数、爬取速度
def ip_html3(link, text, page, speed):
    global proxy_ip
    ip_num = 0
    try:
        for a in range(1, page):  # 爬取多少页
            url = str(link) + str(a)
            response = requests.get(url, headers=headers, timeout=8)
            # print(response.text)
            soupIP = BeautifulSoup(response.text, 'html5lib')
            trs = soupIP.find_all('tr')
            for tr in trs[1:]:
                ip_num += 1  # 自增计算IP数
                tds = tr.find_all('td')
                # print(tds)
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                proxy_ip.append(ip + ':' + port)
            time.sleep(speed)  # 控制访问速度(很重要，如果访问太快被封IP就不能继续爬了)
    except Exception as e:
        print(e)
    print(str(text) + "获取到" + str(ip_num) + "个代理IP")


# 获取普通代理IP函数
def get_ip():
    # 定义一个获取IP的线程池，如果你有其他接口可以往里加
    threads_ip = [MyThread(ip_json, args=('http://www.66ip.cn/mo.php?sxb=&tqsl=7000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=', '66免费代理')),
                  MyThread(ip_html3, args=('https://www.xicidaili.com/nt/', '西刺代理', 5, 6)),
                  MyThread(ip_html2, args=('https://www.kuaidaili.com/free/intr/', '快代理', 20, 2)),
                  MyThread(ip_html2, args=('http://www.ip3366.net/free/?stype=2&page=', '云代理', 7, 0)),
                  MyThread(ip_json, args=('http://www.89ip.cn/tqdl.html?api=1&num=3000&port=&address=&isp=', '89免费代理（不知道是不是高匿）')),
                  MyThread(ip_html1, args=('http://www.nimadaili.com/putong/', '泥马代理', 100, 1)),
                  MyThread(ip_html1, args=('http://www.xiladaili.com/putong/', '西拉代理', 100, 1))]
    for b in threads_ip:
        b.start()
    for b in threads_ip:
        b.join()
    # 推荐个小幻代理(防爬但有手动提取接口):https://ip.ihuan.me/


# 获取匿名代理IP函数
def get_anonymous_ip():
    # 定义一个获取IP的线程池，如果你有其他接口可以往里加
    threads_ip = [MyThread(ip_json, args=('http://www.66ip.cn/nmtq.php?getnum=3000&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip', '66免费代理')),
                  MyThread(ip_html3, args=('https://www.xicidaili.com/nn/', '西刺代理', 5, 6)),
                  MyThread(ip_html2, args=('https://www.kuaidaili.com/free/inha/', '快代理', 20, 2)),
                  MyThread(ip_html2, args=('http://www.ip3366.net/free/?stype=1&page=', '云代理', 7, 0)),
                  MyThread(ip_json, args=('http://www.89ip.cn/tqdl.html?api=1&num=3000&port=&address=&isp=', '89免费代理（不知道是不是高匿）')),
                  MyThread(ip_html1, args=('http://www.nimadaili.com/gaoni/', '泥马代理', 100, 1)),
                  MyThread(ip_html1, args=('http://www.xiladaili.com/gaoni/', '西拉代理', 100, 1)),
                  MyThread(ip_html2, args=('https://www.7yip.cn/free/?action=china&page=', '齐云代理', 90, 0)),
                  MyThread(ip_html2, args=('https://ip.jiangxianli.com/?page=', '高可用全球免费代理库', 8, 0))]
    for b in threads_ip:
        b.start()
    for b in threads_ip:
        b.join()
    # 推荐个小幻代理(防爬但有手动提取接口):https://ip.ihuan.me/


# 验证输入正确函数
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


# 验证代理函数
def test_ip(lists, site, word, code):
    global proxy_ok_ip
    for ip in lists:
        proxy_host = ip
        try:
            proxy_temp = {"http": proxy_host, "https": proxy_host}
            res = requests.get(site, headers=headers, proxies=proxy_temp, timeout=5)  # 验证超时时间，默认5秒
            if code == "2":
                res.encoding = 'gbk'
            else:
                res.encoding = 'utf-8'
            if word in res.text:  # 判断关键词是否在网站源码中
                print(res, proxy_host + "  is OK")
                proxy_ok_ip.append(proxy_host)
            else:
                print(proxy_host + "  is BOOM")
        except:  # 超时或异常
            print(proxy_host + "  is BOOM")
            continue


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
    if choose == '2':
        print("正在获取高匿代理IP中请稍等片刻，大概3分钟...(≡•̀·̯•́≡)认真脸")
        get_anonymous_ip()
        ip_list = ip_list(proxy_ip)  # 去重
    else:
        print("正在获取普通代理IP中请稍等片刻，大概3分钟...(≡•̀·̯•́≡)认真脸")
        get_ip()
        ip_list = ip_list(proxy_ip)  # 去重

    # 是否验证可用性？
    value = input("\n去重后共获取到" + str(len(ip_list)) + "个代理IP，是否验证可用性（默认否，输入任意字符开始验证）：")

    if value:  # 验证可用性✔
        while True:  # 首次验证检测输入是否正确，不使用代理IP
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
        threads = []  # 定义一个线程池
        for i in range(thread_num):
            i *= thread_count
            # 创建新线程,添加到线程池
            threads.append(MyThread(test_ip, args=(ip_list[i+1:i+thread_count], site, word, code)))
        # 开启所有线程
        for t in threads:
            t.start()
        # 等待所有线程完成
        for t in threads:
            t.join()
        print("可用IP总数为" + str(len(proxy_ok_ip)) + "个")
        text_save("验证过的IP列表.txt", proxy_ok_ip)

    else:  # 不验证可用性×
        # print(ip_list)
        text_save("未验证的IP列表.txt", ip_list)
    input()