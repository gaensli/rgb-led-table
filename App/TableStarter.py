#!/usr/bin/python

from App.TetrisClass import *
from App.LounchTableClass import *
from App.UDPClass import *
from App.StartClass import *
from App.TimeClass import *
from App.ClearClass import *
from App.BallClass import *
from App.TestClass import *

UDP_IP = '192.168.1.36'
UDP_PORT = 5009
BUFFER_SIZE = 1024
tetrisgame = None
lt = None
udpinstanz = None
startinstanz = None
timeinstanz = None
clearinstanz = None
ballinstanz = None
testinstanz = None

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)
s.bind((UDP_IP, UDP_PORT))
print('listening on '+UDP_IP+":"+str(UDP_PORT))
startinstanz = StartClass()
startinstanz.flashBlue()
startinstanz = None
clearinstanz = ClearClass()

while True:
    try:
        data = s.recv(BUFFER_SIZE)

        print "received packet:", data

        if str(data).startswith("TET"):
                tetrisgame =RGB_Tetris(s,str(data)[3:])
                tetrisgame.startGame()
                tetrisgame = None
                clearinstanz.clear()
        if str(data).startswith("LOU"):
                lt=LoungeTable(s,str(data)[3:6],str(data)[6:9],str(data)[9:13],str(data)[13:])
                lt.startTable()
                lt=None    
                clearinstanz.clear()
        if str(data).startswith("UDP"):
                udpinstanz=UDPTable(s)
                udpinstanz.UDPStart()
                udpinstanz=None
                clearinstanz.clear()
        if str(data).startswith("TIM"):
                timeinstanz=TimedisplayClass(s)
                timeinstanz.timeStart()
                timeinstanz=None
                clearinstanz.clear()
        if str(data).startswith("BAL"):
                ballinstanz=BallanimationClass(s)
                ballinstanz.ballStart()
                ballinstanz=None
                clearinstanz.clear()
        if str(data).startswith("TES"):
                testinstanz=TestAnimationClass(s)
                testinstanz.testStart()
                testinstanz=None
                clearinstanz.clear()
        data=""

    except: 
        pass
clearinstanz.clear()    
s.close()