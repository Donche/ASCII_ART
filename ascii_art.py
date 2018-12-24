# -*- coding: utf-8 -*- 
from PIL import Image
import os
import cv2
import time
from threading import Thread
from playsound import playsound
import curses


def transform1(image_file): 
    image_file = image_file.convert("L") 
    code_pic = '' 
    for h in range(0,image_file.size[1]):
        for w in range(0,image_file.size[0]): 
            gray = image_file.getpixel((w,h))
            code_pic = code_pic + code_lib[int(((count-1)*gray)/256)]
        code_pic = code_pic + "\n" 
    return code_pic

def play_music(filename):
    playsound(filename)

vflag = int(input("select type: \n1.image\t2.video\t3.play converted video:\n"))

if(vflag == 1 or vflag == 2):
    v = input("Use default dictionary(y/n):")
    if(v == 'y'):
        code_lib = "@B%8&WM#ahdpmZOQLCJYXzcunxrjft/\|()1[]?-_+~<>i!I;:,    "
    else:
        code_lib = input("select dictionary:")
    count = len(code_lib)


if(vflag == 1):
    fn = input("input file name : ")
    hratio = float(input("input height zoom ratio(default 1.0) : ") or "1.0")
    wratio = float(input("input width zoom ratio(default 1.0) : ") or "1.0")
    fp = open(fn,'rb')
    image_file = Image.open(fp)
    image_file=image_file.resize((int(image_file.size[0]*wratio), int(image_file.size[1]*hratio)))
    print(u'Size info:',image_file.size[0],' ',image_file.size[1],' ')
    tmp = open('result.txt','w')
    transData = transform1(image_file)
    print(transData)
    tmp.write(transData)
    tmp.close()

elif(vflag == 2):
    fn = input("input file name : ")
    hratio = float(input("input height zoom ratio(default 1.0) : ") or "1.0")
    wratio = float(input("input width zoom ratio(default 1.0) : ") or "1.0")
    cap = cv2.VideoCapture(fn) 
    i = 0
    if(os.path.isdir("./out") == False):
        os.makedirs("./out")
    while(cap.isOpened()): 
        ret, frame = cap.read() 
        if ret == False:
             break
        cv2.imshow('image', frame) 
        k = cv2.waitKey(10) #q键退出 

        os.system('cls') 
        i += 1
        tmp = open('./out/BA('+str(i)+').txt','w') 
        frame = cv2.resize(frame, (0,0), fx=wratio, fy=hratio)
        frame = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)) 
        transData = transform1(frame) 
        print(transData) 
        tmp.write(transData) 
        tmp.close() 

        if (k & 0xff == ord('q')): 
            break 
    cap.release() 
    cv2.destroyAllWindows() 

elif(vflag == 3):
    i = 1
    v = float(input("Frame per second: \t"))
    pmusic = input("play music?(y/n)\t")
    if(pmusic == 'y'):
        filedir = input("input music name:\t")
        thread = Thread(target = play_music, args = (filedir,))
        thread.start()
    stdscr = curses.initscr()
    stdscr.keypad(1)
    t0 = time.time()
    while(True):
        t1 = time.time()
        i = int((t1 - t0) * v) + 1
        filename = './out/BA('+str(i)+').txt'
        try:
            with open(filename,'r') as f:
                data = f.read()
                stdscr.addstr(0,0,data)
                stdscr.addstr("Frame: %d"%i)
                stdscr.refresh()
                # os.system('cls')
                # print(data)
        except IOError:
            break

os.system('pause')