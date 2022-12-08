#moudle:pyaudio,numpy
import wave,pyaudio,os,struct,math,sys,time,platform,contextlib,ctypes,zipfile,cv2
import numpy as np
from threading import *
from subprocess import Popen
from numpy import *

print("unzipping...")
zf=zipfile.ZipFile(sys.argv[1],'r')
mf=open("music.txt","wb")
mf.write(zf.read("music.txt"))
mf.close()
vf=open("video.mp4","wb")
vf.write(zf.read("video.mp4"))
vf.close()
def func(x):
    return np.arcsin(np.sin(x))/2#default_function
try:
    fx=zf.read("FUNC").strip().decode("utf-8")
    exec("def func(x): return "+fx)
    print("Loaded function y =",fx)
except Exception as e:
    print("Loaded default function",e)
zf.close()
e={"0":0,
   
   ".1":262,".2":294,".3":330,".4":350,".5":392,".6":440,".7":494,
   "1":523,"2":578,"3":659,"4":698,"5":784,"6":880,"7":988,
   "1.":1046,"2.":1175,"3.":1318,"4.":1400,"5.":1568,"6.":1760,"7.":1976}
#by book_rain@CSDN----------------------------------------------------------------
vol=0.05
def c(sfl,sfr,wf,time):
    db = math.pow(10, -3/20)
    framerate = 44100
    sample_width = 2
    bits_width = sample_width*8
    # seconds, long of data
    duration = time/1000
    # frequeny of sinewave
    sinewav_frequency_l = sfl
    sinewav_frequency_r = sfr
    # max value of samples, depends on bits_width
    max_val = 2**(bits_width-1) - 1
    volume = max_val*db
    #多个声道生成波形数据
    x = np.linspace(0, duration, num=int(duration*framerate))
    y_l = func(2 * np.pi * sinewav_frequency_l * x) * volume * vol
    y_r = func(2 * np.pi * sinewav_frequency_r * x) * volume * vol
    # 将多个声道的波形数据转换成数组
    y = zip(y_l,y_r)
    y = list(y)
    y = np.array(y,dtype=int)
    y = y.reshape(-1)
    # 最终生成的一维数组
    sine_wave = y
    for i in sine_wave:
        data = struct.pack('<h', int(i))
        wf.writeframesraw(data)
#---------------------------------------------------------------------------------
error=False
que=[]
start=0
def core(f):
    global e,que,echos
    for i in f:
        if(i.strip()==""):
            continue
        if(i.strip().split(" ")[0]=="echo"):
            try:
                echos.append(Echo(i.strip().split(" ")[1],0,i.strip().split(" ")[2]))
            except:
                try:
                    echos.append(Echo(i.strip().split(" ")[1],0))
                except:
                    pass
            continue
        if(i.strip().split(" ")[0]=="#"):
            continue
        else:
            l=0
            r=0
            try:
                l=e[i.strip().split(" ")[0]]
            except:
                pass
            try:
                r=e[i.strip().split(" ")[1]]
            except:
                pass
            try:
                if(len(i.strip().split(" ")[0])>1):
                    if(i.strip().split(" ")[0][0]=="r"):
                        l=int(i.strip().split(" ")[0][1:])
            except:
                pass
            try:
                if(len(i.strip().split(" ")[1])>1):
                    if(i.strip().split(" ")[1][0]=="r"):
                        r=int(i.strip().split(" ")[1][1:])
            except:
                pass
            que.append([l,r,int(int(i.strip().split(" ")[2]))])
    f.close()


def music_make(fpath):
    fname=os.path.splitext(os.path.basename(fpath))[0]
    #open
    channel_num = 2
    framerate = 44100
    sample_width = 2
    wf = wave.open("music.wav","wb")
    wf.setnchannels(channel_num)
    wf.setframerate(framerate)
    wf.setsampwidth(sample_width)
    #mix
    try:
        core(open(fpath,"r",encoding="GBK"))
        for i in range(len(que)):
            c(que[i][0],que[i][1],wf,que[i][2])
            print(str(i+1)+" "*(len(str(len(que)))-len(str(i+1)))+"/"+str(len(que))+" "+str(int((i+1)/len(que)*100))+"%",end="\r")
        wf.close()
    except Exception as e:
        print("Error(music_make)::",e.__class__.__name__+":",e)
        error=True
        os.system("pause")

music_len=0
music_pre=0#0%
main_abort=False
def music_play(fname):
    global music_len,music_pre,main_abort
    chunk = 1024
    framerate = 44100
    sample_width = 2
    wf = wave.open("music.wav","rb")
    music_len = wf.getnframes()
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
    data = wf.readframes(chunk)
    i=0
    start=time.time()
    while(len(data)>0 and main_abort==False):
        #if(t/video_time - music_pre > 0.01):
        #    wf.readframes(chunk)
        #    i+=1
        #    continue
        try:
            stream.write(data)
        except Exception as e:
            while(1):
                print(e)
        data = wf.readframes(chunk)
        i+=1
        music_pre=i*chunk/music_len
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    main_abort=True

try:
    cc=ctypes.windll.LoadLibrary(".\\ConsoleClear.dll")
    if(platform.uname()[0]=="Windows"):
        cp=ctypes.windll.kernel32.GetConsoleCP()
        path=os.path.join(os.getenv("SystemRoot"),"System32","chcp.com")#%SystemRoot%\System32\chcp.com
        p=Popen([path,str(cp),">","NUL"],shell=True,stdout=sys.stdout,cwd=os.getcwd())#重新加载codepage
        p.wait()
except:
    cc=None
def ConsoleClear():
    if(platform.uname()[0]=="Windows"):
        cc.ConsoleClear()
    else:
        sys.stdout.write("\033[0;0H")
ConsoleClear()
def rgb(red, green, blue, string):
    return f'\x1b[38;2;{red};{green};{blue}m{string}'
def GetConsoleXY():
    try:
        return os.get_terminal_size().columns,os.get_terminal_size().lines
    except:
        return 100,100
cap = cv2.VideoCapture("video.mp4")
fps=cap.get(cv2.CAP_PROP_FPS)
assert cap.isOpened(), 'Cannot capture source'
t=0
music_make("music.txt")
mfname="music.txt"
rate = cap.get(5)
frame_num =cap.get(7)
video_time=frame_num/rate*fps#视频帧数
video_start_time=time.time()#开始时间

try:
    Thread(target=music_play,args=(mfname,),daemon=False).start()
    ret, frame = cap.read()
    t=1
    while(ret):
        t+=1
        if(music_pre - t/video_time > 0.001):
            cap.read(video_time*(music_pre - t/video_time))
            continue
        while(music_pre < t/video_time and not main_abort):
            time.sleep(0.001)
        x,y=GetConsoleXY()
        fme=cv2.resize(frame,(x//2,y-1))#最后的\n可能会使画面抖动，所以去掉最后一行
        ConsoleClear()
        for i in fme:
            for j in i:
                sys.stdout.write(rgb(j[2],j[1],j[0],"██"))
            sys.stdout.write("\n")
        ret, frame = cap.read()
except KeyboardInterrupt:
    main_abort=True
except Exception as e:
    print(e.__class__.__name__,e,0)
cap.release()
try:
    os.remove("music.txt")
except Exception as e:
    print(e.__class__.__name__,e,1)
try:
    os.remove("video.mp4")
except Exception as e:
    print(e.__class__.__name__,e,2)
try:
    os.remove("music.wav")
except Exception as e:
    print(e.__class__.__name__,e,3)
