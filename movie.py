#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import json
import time
import requests
from fake_useragent import UserAgent
import sql

# User-Agent池
ua = UserAgent()
headers = {'User-Agent': ua.chrome}

# 代理IP池(有时效性)
proxies = ['49.86.75.105:39187', '110.86.176.186:44587', '27.152.195.115:29933', '1.194.148.210:30077',
           '123.54.231.164:48890', '106.122.169.251:48471', '100.86.35.31:47038', '49.85.111.243:23859',
           '183.166.125.46:35662', '49.85.105.104:25124', '122.241.218.254:20164', '220.185.209.203:45233',
           '125.109.195.79:22384', '125.123.64.194:21925', '117.93.181.43:44142', '180.125.70.163:42062']

# 全局变量
times = 0


# 豆瓣电影分类函数(tag)
def douban_tags():
    response = requests.get("https://movie.douban.com/j/search_tags", headers=headers)
    tags = json.loads(response.text)
    return tags["tags"]  # 返回豆瓣电影分类列表


# 豆瓣电影信息函数(ID、标题、评分、图链)
def douban_movie(mv_tag, mv_num):
    temp = []
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=" + str(mv_tag) + "&sort=recommend&page_limit=" + \
          str(mv_num) + "&page_start=0"
    response = requests.get(url, headers=headers, timeout=10)
    movie_json = json.loads(response.text)
    for info in movie_json["subjects"]:  # 遍历豆瓣JSON信息得到字典数据
        temp.append([info["id"], info["title"], info["rate"], info["cover"]])
    return temp  # 返回各分类所有电影的信息数组


# 豆瓣电影详情函数(日期、简介、导演、作者、演员、类型)
def douban_info(id, mv_id, you_ip):
    url = "https://movie.douban.com/subject/" + str(mv_id)
    proxy_host = you_ip  # 代理IP
    response = requests.get(url, headers=headers, proxies={"http": proxy_host, "https": proxy_host}, timeout=10)
    movie_json = re.search(r'application/ld\+json">([\s\S]*?)</script', response.text)
    movie_json = movie_json.group()  # 得到正则取到的内容
    movie_json = movie_json.replace('application/ld+json">', '').replace('</script', '').replace('\n', '').\
        replace('\t', '').replace('\r', '')  # 删除多余的内容
    info = json.loads(movie_json)
    description = info["description"].replace("'", "\\'").\
        replace('黃子華棟篤笑之金盤𠺘口', '黄子华栋笃笑之金盆啷口').replace('􅶫', '')  # 替换一些特殊字符！
    director = str(info["director"]).replace("'", "\\'")  # 豆瓣电影导演
    author = str(info["author"]).replace("'", "\\'")  # 豆瓣电影编剧
    actor = str(info["actor"]).replace("'", "\\'")  # 豆瓣电影演员
    genre = str(info["genre"]).replace("'", "\"")  # 豆瓣电影类别
    # 信息插入数据库
    sql.insert_info(str(id), info["datePublished"], description, director, author, actor, genre)


# 免费代理IP轮换
def free_ip():
    global times
    while True:  # 轮换免费代理IP
        try:
            proxy_host = proxies[times]
            times += 1
            break
        except Exception:
            times = 0
            proxy_host = proxies[times]
            times += 1
            break
    return proxy_host


# 付费代理IP轮换,讯代理独享IP
def pay_ip():
    url = "http://api.xdaili.cn/xdaili-api//newExclusive/getIp?spiderId=706009a6d1ca46a0a3ff72a496a06a34&orderno=" \
          "DX20204177028FdsijZ&returnType=1&count=1&machineArea="
    response = requests.get(url, headers=headers, timeout=10)
    return response.text.split()[0]


# 列表去重函数
def list(lists):
    temp = []
    for i in lists:
        if not i in temp:
            temp.append(i)
    return temp


if __name__ == '__main__':
    # 遍历豆瓣所有电影
    sql.create_db()
    sql.create_table()
    print("开始遍历数据，请耐心等候~")
    one = []
    for tag in douban_tags():
        for mv in douban_movie(tag, 500):
            one.append(mv)
    final = list(one)
    print("遍历完成，重复数据已去除,开始插入数据库~")

    # 插入数据库 ID、标题、评分、图链
    key = 1  # 数据库主键
    try:
        for x in final:
            # 替换一些特殊字符！
            title = x[1].replace('黄子华栋笃笑之金盆𠺘口', '黄子华栋笃笑之金盆啷口').replace("'", "\\'")
            sql.insert_data(str(key), str(x[0]), title, str(x[2]), x[3])
            key += 1
        print("第一轮爬取写入数据库完成~")
    except Exception as e:
        print(e)

    # 插入数据库 日期、简介、导演、作者、演员、类型
    key2 = 1  # 数据库主键
    ip = pay_ip()
    for y in final:
        while True:
            try:
                douban_info(key2, y[0], ip)
                break
            except Exception as e:
                time.sleep(15)  # 付费IP等15秒换IP
                ip = pay_ip()
                print(e)
        key2 += 1
    print("第二轮详情爬取写入数据库完成~")
    print("任务完成！")