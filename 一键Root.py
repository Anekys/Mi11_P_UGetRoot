import os
import requests
import time
from bs4 import BeautifulSoup


class Phone():
    def runcode(code):
        popen = os.popen(code)
        res = popen.read()
        popen.close()
        return res

    def checkphone(self):
        Phone.runcode('fastboot.exe wait-for-device')
        Phone.runcode('cls')
        res = Phone.runcode('fastboot.exe devices')
        if res != "":
            return True
        else:
            return False

    def flushimg(self, imgname):
        try:
            result = Phone.runcode(f'fastboot.exe flash boot {imgname}')
            if 'OKEY' in result:
                return True
            else:
                return False
        except Exception as error:
            print(f'刷入失败:{error}')
            return False

    def reboot(self):
        try:
            Phone.runcode('fastboot.exe reboot')
        except Exception as error:
            print(f'错误:{error}')


class Computer():
    def __init__(self):
        self.version = '1.0'

    def checkversion(self):
        url = "http://bootimg.6847m.cn/readme.md"
        version = requests.get(url)
        if self.version != version.text:
            up = input("发现新版本是否更新(Y/N):")
            if up == 'Y' or up == "":
                self.Download('http://bootimg.6847m.cn/root.zip', 'root.zip')
                print("最新版以下载至根目录,请手动解压覆盖进行更新~")

    def pickimg(self, model="Mi11"):
        url = "http://bootimg.6847m.cn/" + model
        res = requests.get(url)
        html = BeautifulSoup(res.text, 'html.parser')
        trlist = html.find_all('tr')[3:-1]
        if trlist == []:
            return False
        choice = []
        for num, tr in enumerate(trlist):
            print(num, end="  ")
            for number, td in enumerate(tr):
                print(td.text, end='    ')
                if number == 0:
                    choice.append(td.text)
            print("")
        select = int(input("请输入手机系统版本对应的序号:"))
        while select < 0 or select >= len(choice):
            select = int(input("没有这个序号,请重新输入:"))
        return choice[select]

    def Download(self, url, filename=""):
        start = time.time()  # 下载开始时间
        response = requests.get(url, stream=True)  # stream=True必须写上
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        try:
            if response.status_code == 200:  # 判断是否响应成功
                print('Start download,[File size]:{size:.2f} MB\n\n'.format(
                    size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                if filename == "":
                    filepath = url[url.rfind("/") + 1:]
                else:
                    filepath = filename
                with open(filepath, 'wb') as file:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        print('\r' + '[下载进度]:%s%.2f%%' % (
                        '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
                    print("")
                    end = time.time()  # 下载结束时间
                print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
            else:
                print('服务器无响应,请检查你的网络环境后再重新下载')
                exit()
        except Exception as error:
            print("下载失败\n错误代码:", error)
            exit()


if __name__ == '__main__':
    os.system("TITLE Xiaomi 11系列 一键ROOT  By Ane")
    os.system("color 3f")
    info = '''
    使用本软件前置基础:一个正常的已经安装好手机驱动的Windows系统电脑
                已经解开BootLoader锁的小米11系列手机
    手机驱动在安装小米解锁(解BL锁)工具时会附带,没安装驱动的自行安装
          刷机有风险,搞机请谨慎,自己确定好情况,出问题概不负责
    '''
    print(info)
    pc = Computer()
    pc.checkversion()
    print('1 小米11\n2 小米11 Pro/Ultra')
    phone = input('请输入对应你手机机型的序号:\n')
    if phone == '1':
        model = pc.pickimg("Mi11")
        url = "http://bootimg.6847m.cn/Mi11/"
    elif phone == "2":
        model = pc.pickimg("Mi11P_U")
        url = "http://bootimg.6847m.cn/Mi11P_U/"
    mi = Phone()
    if os.path.exists(model):
        print("\n检测到文件夹中已存在boot镜像,请将手机重启至Fastboot模式连接至计算机")
        mi.checkphone()
        mi.flushimg(model)
        mi.reboot()
    else:
        print("\n文件目录中未检测到boot镜像,准备进行下载")
        pc.Download(url + model)
        print("现在开始进行刷入,请将手机重启至FastBoot模式连接至计算机")
        mi.checkphone()
        mi.flushimg(model)
        mi.reboot()
