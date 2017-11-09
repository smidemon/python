# -*- coding: UTF-8 -*-
import paramiko,os,pexpect,time
from pysphere import VIServer
from pysphere import VIException, VIApiException,FaultTypes
#import esxi_exception

cluster_list = ["Fqj-EkOS-deploy","Fqj-EkOS-master","Fqj-EkOS-node"]

server = VIServer()
dict = {}
user = "root"
ip = "192.168.22.2"
mypassword = "password"

#连接虚拟机服务器
def connect_server(ip,name,pwd):
  server.connect(ip,name,pwd)
  flag = server.is_connected()
  return flag

#获取虚拟机对象
def get_the_vm():
  flag = connect_server("192.168.1.243","root","P@ssw0rd")
  vms = []
  if flag:
    try:
      print cluster_list
      for i in cluster_list:
        vm = server.get_vm_by_name(i)
        print vm
        vms.append(vm)
    except:
      print "failed to get name!"
  else:
    return None
  
  return vms

#恢复到最新快照
def revert_to_snapshot1():
  vms = get_the_vm()
  print vms
  for vm in vms:
    try:
      vm.revert_to_snapshot()
    except:
      print "failed to revert!"
      return 
  print "success to revert"

#开启虚拟机
def start_vm():
  vms = get_the_vm()
  for vm in vms:
    #vm.power_on()
    #dict[vm] = null
    status = vm.get_status()
    #dict[vm]=status
    #print status
    if status != "POWERED ON":
      vm.power_on()
      time.sleep(5)
    else:
      dict[vm] = vm.get_status()
  return dict


#执行安装命令
def exec_cmd():
  dict = start_vm()
  keys = dict.keys()
  for key in keys:
    if dict[key] != "POWERED ON":
      exec_cmd()
    else:
      continue
  count = 0
  flag = True
  cmd = "bash /root/aaa.sh"
  #os.system("scp /root/Python/python_code/aaa.sh root@192.168.22.2:/root/")
  while flag:
    if os.system("ping 192.168.22.2 -c 1") == 0:
      flag = False
      time.sleep(7)
      try:
        child = pexpect.spawn('scp -o "StrictHostKeyChecking no" /root/python_code/fqj/aaa.sh %s@%s:/root/' % (user,ip))
        
        child.expect ('password:')
        os.system('echo "开始输入密码"')
        child.sendline (mypassword)
        os.system('echo "执行脚本已经上传成功"')
        time.sleep(5)
        # os.system("scp /home/wjx.py/installceph.sh root@192.168.13.45:/root/")
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        os.system('echo "远程连接deploy"')
        ssh.connect('192.168.22.2',port=22,username='root',password='password')
        os.system('echo "开始执行安装脚本"')
        
        os.system('echo -e "安装中\c" && echo -e "\033[5m...\033[m"')
        #ssh.connect('192.168.13.45',port=22,username='root',password='password')
        stdin, stdout, stderr = ssh.exec_command(cmd) 
        print stdout.read()
   
      except:
        print("连接主机失败")
    else:
      count += 2
      print count
      time.sleep(2)

#get_the_vm()
revert_to_snapshot1()#调用回滚函数
start_vm() #调用开启虚拟机函数


#循环取出所有虚拟机的状态
keys = dict.keys()
for key in keys:
  print dict[key]

#reboot_vm()
#revert_to_snapshot1()

exec_cmd()#调用执行命令函数，开始拷贝安装脚本到远程主机并执行

