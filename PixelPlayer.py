from time import sleep
from platform import platform
import cv2
import wave
import pyaudio
import os
from ctypes import *
import time
try:
    cc=windll.LoadLibrary(".\\ConsoleClear.dll")
except:
    cc=None
def ConsoleClear():
    if(platform().lower().startswith("windows")):
        cc.ConsoleClear()
    else:
        os.system("clear")
ConsoleClear()
def rgb(red, green, blue, string):
    return f'\x1b[38;2;{red};{green};{blue}m{string}'
def GetConsoleXY():
    return os.get_terminal_size().columns,os.get_terminal_size().lines
cap = cv2.VideoCapture('a.mp4')
fps=cap.get(cv2.CAP_PROP_FPS)
#wav = wave.open('a.wav','rb')
#output_dev=pyaudio.PyAudio()
#stream=output_dev.open(format=pyaudio.paInt16,channels=1,rate=wav.getframerate(),output=True)
#chunk=int(params[2]*0.05)
assert cap.isOpened(), 'Cannot capture source'
t=0
while(1):
    t+=1
    start=time.time()
    if((t%2==0) or 1):
        ret, frame = cap.read()
        #afme=wav.readframes(chunk)
        #stream.write(afme)
        if ret == False:
            break
        x,y=GetConsoleXY()
        fme=cv2.resize(frame,(x//2,y-1))#最后的\n可能会使画面抖动，所以去掉最后一行
        ConsoleClear()
        s=""
        for i in fme:
            for j in i:
                print(rgb(j[2],j[1],j[0],"██"),end="")
            print()
    else:
        cap.read()
    end=time.time()
    #print(s,end="")
    #sleep(0.1)
    #sleep(1/fps)
    #delay
    sleep(max(0,1/fps-end+start))
cap.release()
#stream.stop_stream()
#stream.close()
#output_dev.terminate()
