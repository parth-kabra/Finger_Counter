from __future__ import division, print_function
import cv2,os,time,Module as htm,sys
from io import BytesIO, IOBase
if sys.version_info[0] < 3:
    from __builtin__ import xrange as range
    from future_builtins import ascii, filter, hex, map, oct, zip
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
def print(*args, **kwargs):
    sep, file = kwargs.pop("sep", " "), kwargs.pop("file", sys.stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()
if sys.version_info[0] < 3:
    sys.stdin, sys.stdout = FastIO(sys.stdin), FastIO(sys.stdout)
else:
    sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
def getNumber(ar):
    s=""
    for i in ar:s+=str(ar[i]);
    if(s=="00000"):return (0)
    elif(s=="01000"):return(1)
    elif(s=="01100"):return(2) 
    elif(s=="01110"):return(3)
    elif(s=="01111"):return(4)
    elif(s=="11111"):return(5) 
    elif(s=="01001"):return(6)
    elif(s=="01011"):return(7) 
    else:return "No finger detected"

wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(detectionCon=0.75)
while True:
    success,img=cap.read()
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    tipId=[4,8,12,16,20]
    if(len(lmList)!=0):
        fingers=[]
        if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):fingers.append(1)
        else:fingers.append(0)
        for id in range(1,len(tipId)):
            if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):fingers.append(1)
            else :fingers.append(0)
        cv2.putText(img,str(getNumber(fingers)),(3,120),cv2.FONT_HERSHEY_SIMPLEX,5,(255, 128, 0),10)  
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.imshow("Frame",img)
    if(cv2.waitKey(1) & 0xFF== ord('q')):break