from socket import *
import sys
import time

# # 全局变量
# HOST = '0.0.0.0'


# 具体功能
class FtpClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L ')  # 发送请求
        #  等待回复
        data = self.sockfd.recv(128).decode()
        # 'OK'表示请求成功
        if data == 'OK':
            data = self.sockfd.recv(1024)
            print(data.decode())
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q ')
        self.sockfd.close()
        sys.exit('谢谢使用')

    def do_get(self,filename):
        # 发送请求
        self.sockfd.send(('G ' + filename).encode())   #  加括号避免.encode优先执行
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            # 循环接收内容写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        # 上传前检查本地是否有该文件
        try:
            f = open(filename,'rb')
        except Exception:
            print('没有该文件')
            return

        # 切割出真正的文件名
        filename = filename.split('/')[-1]
        # 发送请求
        self.sockfd.send(('P ' + filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)

# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)
    while True:
        print('\n=======命令选项==========')
        print('********* list ***********')
        print('******** get file ********')
        print('******** put file ********')
        print('********** quit **********')
        print('==========================')

        cmd = input('输入命令:')
        if cmd.strip() == 'list':   #  stirp函数切割掉左右的空格
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(' ')[-1]   #
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put(filename)

        # if cmd == 'get file':
        #     sockfd.send(cmd.encode())
        # if cmd == 'put file':
        #     sockfd.send(cmd.encode())
        # if cmd == 'get file':
        #     sockfd.send(cmd.encode())

# 网络链接
def main():
    # 服务器地址
    ADDR = ('127.0.0.1',8880)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print('链接服务器失败')
        return
    else:
        print('''
                ******************************
                    Data    File    Image
                ****************************** 
        ''')
        cls = input('请输入文件种类:')
        if cls not in ['Data','File','Image']:
            print('Sorry input Error!!!')
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)      #　发送具体请求

if __name__ == '__main__':
    main()