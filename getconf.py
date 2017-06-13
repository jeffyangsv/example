#!/usr/bin/python
# _*_ coding:utf-8 _*_
import re
import paramiko
import time
import threading

# 此类定义一个日志的详细信息
class LOGINFO:
    # 主机地址
    host = None
    # 端口号
    port = 22
    # 用户名
    user = None
    # 密码
    password = None
    # 待分析日志存放目录
    path = None
    # 待分析日志名
    filename = None
    
    def _init_(self):pass

#------------------server.txt文件内容格式如下---------------------------------
'''
172.28.3.194,/opt/TianShan/logs,RtspProxy.log,ghxormedia,ghxormedia,
172.28.166.98,/opt/TianShan/logs,RtspProxy.log,root,P@ssw0rd,
''' 
#----------------------------------------------------

# 获取所有待分析的日志列表,并校验信息是否合法
def getloglist():
   
    filename = r'C:/Users/Administrator/Desktop/watchdog-master/conf/server.txt'
    fileHandle = open(filename, 'r')
    
    loglist = []
    for line in fileHandle:
        conf = line.split(',')
        length = len(conf)
        if(length >= 5):
            try:
                ser = LOGINFO()
                ser.host = conf[0]
                ser.path = conf[1]
                ser.filename = conf[2]
                ser.user = conf[3]
                ser.password = conf[4]
                loglist.append(ser)                
            except IndexError:
                print "list index out of range!" 
        else:
            print line + " Error, information is not enough!"
    
    fileHandle.close();
    return loglist


#----------------------------
def dowords(fileHandle, filename):
    keylist = []
#    setup_re=re.compile(r'([01][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]{3}).*?(\d+.\d+.\d+.\d+:\d+) SETUP rtsp://.*?asset=(\S+)&.*?smartcard-id=(\d+).*')
    setup_re=re.compile(r'(?P<datetime>[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]{3}).*?SOCKET:\s(\d+)\s(\d+.\d+.\d+.\d+:\d+) (SETUP) rtsp://.*?asset=(\S+)&folder.*?smartcard-id=(\d+).*')
    for line in fileHandle:
        setuplist=setup_re.search(line)
        if setuplist:
            #dict = setuplist.groupdict()
            #time = dict['datetime']
            keylist.append(setuplist.groups())
    
    return keylist

#----------------------------                    
def show_rtsp(fileHandle,keylist):
    for i in keylist:
        print i
    print "################################################"
    ip_port=raw_input("Input your check ip:")
#    print ip_port
    rtsp_re = re.compile(r'%s'% ip_port)
    for line in fileHandle:
        if rtsp_re.findall(line):
            print line
#----------------------------  
def get_status(fileHandle,keylist):
    status = 'None'
    #ssm_session = 'None'
    status_re = re.compile(r'SOCKET:\s%s\s%s\s\S+\s(\d{1,4})\s.*?%s' % (keylist[1],keylist[2],keylist[3]))
    for line in fileHandle:
        if status_re.findall(line):
            keylist.append(status_re.findall(line)[0])
            #ssm_session = status_re.group(2)
            break
    return keylist    
                
            
#---------------------------- 
def analyze(host, path, filename, username, password, port):
    
    print 'start to analyze ' + host + '-' + filename + '\n'
    start = time.time()
    #paramiko遵循SSH2协议,支持以加密和认证的方式,进行远程服务器的连接
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    #sftp.put(LOCAL_PATH,REMORE_PATH)   #sftp将本地路径LOCAL_PATH的文件上传到远程服务器的 REMORE_PATH路径下
    #sftp.get(REMORE_PATH,LOCAL_PATH)   #从远程服务器取文件到本地
    sftp.chdir(path)
    fileHandle = sftp.open(filename, 'r')
    fileHandle1 = fileHandle.readlines()
    #调用dowords fuction并赋值给keylist
    keylist=dowords(fileHandle1, filename)
    show_rtsp(fileHandle1,keylist)
    fileHandle.close()
    transport.close()
    
    end = time.time();
    print 'finished to analyze' + host + '-' + filename
    print ',total time is %f \n' % (end - start)
#---------------------------- 

   
serverlist = getloglist()
for s in serverlist:
#	  print s.host, s.path, s.filename, s.user, s.password, s.port
    th = threading.Thread(target=analyze, args=(s.host, s.path, s.filename, s.user, s.password, s.port))
    th.start()      