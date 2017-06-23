#coding=utf8
import psutil,time
from operator import itemgetter

def getProcessInfo(p):
    """取出指定进程占用的进程名，进程ID，进程实际内存, 虚拟内存,CPU使用率
    """
    try:
        cpu = int(p.cpu_percent(interval=0))
        memory = p.memory_percent()
        name = p.name()
        cmd = p.cmdline()
        pid = p.pid
    except Exception as ex:
        print ex
        name = "Closed_Process"
        pid = 0
        memory = 0
        cpu = 0
        cmd =0

    return {"name":name,"cmd":cmd,"pdi":pid,"memory":memory, "cpu":cpu}

def getAllProcessInfo():
    """取出全部进程的进程名，进程ID，进程实际内存, 虚拟内存,CPU使用率
    """
    instances = []
    all_processes = list(psutil.process_iter())
    for proc in all_processes:
        try:
            proc.cpu_percent(interval=0)
        except Exception as e:
            print e
    #此处sleep1秒是取正确取出CPU使用率的重点
    time.sleep(1)
    for proc in all_processes:
        instances.append(getProcessInfo(proc))
    return instances

#while  True:
#    s= getAllProcessInfo()
#    sorted_x = sorted(s, key=itemgetter('memory'),reverse=True)
#    for i in sorted_x[:10]:
#        print i
#        if i['cpu'] > 100:
#            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#    print "="*100
# Cpu使用率
#while True:
#    print str(psutil.cpu_percent(1))