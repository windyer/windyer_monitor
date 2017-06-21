#coding=utf-8
import time
import requests
#requests.post("http://127.0.0.1:8080/push",{'time':111})
#ProStatus().makelines("sssssssssssss")
import random
class Amonitor():
    def __new__(cls, *args, **kwd):
        if Amonitor.__instance is None:
            Amonitor.__instance = object.__new__(cls, *args, **kwd)
            return Amonitor.__instance

    def __init__(self):
        print "2"*100
        i=1
        j=100
        while True:
            requests.post("http://127.0.0.1:8080/push", {j+1:i,j:i},timeout=0.5)
            time.sleep(2)
            i=random.randint(1,100)
            j=random.randint(1,100)
Amonitor()