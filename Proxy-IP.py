#!/usr/bin/env python3
# -*- coding:gbk -*-

import re
import requests
import threading

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}


# ��дThread��,��ȡ���̵߳ķ���ֵ
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


# ��ȡ����IP�б���
def get_ip():
    url = "http://www.66ip.cn/mo.php?sxb=&tqsl=7000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
    ip = requests.get(url, headers=headers)
    proxy_ip = re.findall(r'\d.*?(?=<br)', ip.text)
    return proxy_ip  # ���������Ĵ���IP�б�


# ��֤�����Ƿ���ú���
def test_ip(lists, site):
    proxy_ok_ip = []
    for ip in lists:
        proxy_host = ip
        try:
            proxy_temp = {"http": proxy_host, "https": proxy_host}
            res = requests.get(site, headers=headers, proxies=proxy_temp, timeout=5).status_code
            if 200 <= res < 300:  # �ж���վ���ص�״̬��
                print(res, proxy_host + "  is OK")
                proxy_ok_ip.append(proxy_host)
            else:
                print(proxy_host + "  is GG")
        except Exception:
            print(proxy_host + "  is GG")
            continue
    return proxy_ok_ip  # ����ͨ����֤�Ĵ���IP�б�


# �б�д��TXT�ļ�������filenameΪд��TXT�ļ���·����dataΪҪд�������б�Ĭ�ϱ���������Ŀ¼�µġ�ip.txt��
def text_save(filename, data):
    file = open(filename, 'w+')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # ȥ��[],�����а����ݲ�ͬ������ѡ��
        s = s.replace("'", '').replace(',', '') + '\n'  # ȥ�������ţ����ţ�ÿ��ĩβ׷�ӻ��з�
        file.write(s)
    file.close()
    print("������Ϣ�����ļ��ɹ�!")


if __name__ == '__main__':
    print("���ڻ�ȡ����IP�����Ե�Ƭ��..." + '\n' + "��û�н�������Ƿ���Է���http://www.66ip.cn/")
    ip_list = get_ip()
    value = input("����ȡ��" + str(len(ip_list)) + "������IP���Ƿ���֤�����ԣ�Ĭ�Ϸ����������ַ���ʼ��֤����")
    if value:
        site = input("������Ҫ���ʵ�վ�㣺")
        thread_num = 500  # Ĭ��500�߳�
        thread_count = len(ip_list) // thread_num  # һ���߳���֤IP��
        final = []  # ��Ŷ��߳̽�����Ķ�ά�б�
        one = []  # ���ô���IP��һά�б�

        threads = []  # ����һ���̳߳�
        for i in range(thread_num):
            i *= thread_count
            # �������߳�,��ӵ��̳߳�
            threads.append(MyThread(test_ip, args=(ip_list[i+1:i+thread_count], site)))

        # �������߳�
        for t in threads:
            t.start()

        # �ȴ������߳����
        for t in threads:
            t.join()

        # �ϲ�����̵߳��б�
        for t in threads:
            final.append(t.get_result())

        # ������ά�б�
        for j in final:
            for k in j:
                one.append(k)
        # print(one)
        text_save("��֤����IP�б�.txt", one)
    else:
        # print(ip_list)
        text_save("δ��֤��IP�б�.txt", ip_list)