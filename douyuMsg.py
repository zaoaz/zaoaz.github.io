#-*- coding:utf-8 -*-
import threading
import socket
import time
import struct
import urllib
import win32api
import win32con

douyuMsgServer = "openbarrage.douyutv.com"
dyPort = 8601

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def connectMsgServer():
    address = (douyuMsgServer,dyPort)
    s.connect(address)




def createMsgData(msg):
    msg+="\0"
    msgLen = len(msg)
    data1 = msgLen+8
    data2 = msgLen+8
    data3 = 689
    data4 = 0
    data5 = 0
    data6 = msg
    strDate = struct.pack("iihbb"+str(msgLen)+"s",data1,data2,data3,data4,data5,data6)
    ##print repr(strDate)
    return strDate



def loginRoom(roomId):
    logindata = createMsgData("type@=loginreq/roomid@="+roomId+"/")
    s.sendall(logindata)
    data = s.recv(4096)
    ##print repr(data)    
    joinGroup(roomId)
    threading.Timer(45,keepLiveMethod).start()
    

def joinGroup(roomId):
    s.sendall(createMsgData("type@=joingroup/rid@="+roomId+"/gid@=-9999/"))
    print "joinGroup finish"
    
def keepLiveMethod():
    s.sendall(createMsgData("type@=mrkl/"))
    print "start keeplive thread(45s once)"


def douyuMsgDeCode(data):
    dataParams = repr(data[12:-1]).split("/")
    dataParamMap = {}
    for dataStr in dataParams:
        dataStrArray = dataStr.split("@=")
        if len(dataStrArray)<2:
            continue;
        key = dataStrArray[0]
        if "'" in key:
            key = key[1:]
        dataParamMap[key.replace("/","@S").replace("@","@A")]=dataStrArray[1].replace("/","@S").replace("@","@A")
    if "type" not in dataParamMap:
        return
    if cmp(dataParamMap["type"],"chatmsg")==0:
        print dataParamMap["txt"].encode("utf-8")
        #通过特定字符组合通过api控制键盘
        if "#w" in dataParamMap["txt"]:
            win32api.keybd_event(87,0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(87,0,win32con.KEYEVENTF_KEYUP,0)
            print 1
        if "#s" in dataParamMap["txt"]:
            win32api.keybd_event(83,0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
        if "#a" in dataParamMap["txt"]:
            win32api.keybd_event(65,0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
        if "#d" in dataParamMap["txt"]:
            win32api.keybd_event(68,0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(68,0,win32con.KEYEVENTF_KEYUP,0)
        if "#j" in dataParamMap["txt"]:
            win32api.keybd_event(74,0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(74,0,win32con.KEYEVENTF_KEYUP,0)
        if "#k" in dataParamMap["txt"]:
            win32api.keybd_event(75,0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(75,0,win32con.KEYEVENTF_KEYUP,0)
        
        ##f = open("aaa.txt","a")
        ##f.write(dataParamMap["txt"].decode("utf-8"))
        ##f.close()
        
    ##print dataParams

def main():
    connectMsgServer()
    loginRoom("248753")
    while True:
        data=s.recv(4096)
        if not data:
            continue
        else:
            douyuMsgDeCode(data)
    
    
    
    
main()
