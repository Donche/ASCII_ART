# -*- coding: utf-8 -*- 
from PIL import Image
import os
import cv2
import time
from threading import Thread
import threading
from playsound import playsound
import curses

CODE_LIB = r"@B%8&WM#ahdpmZOQLCJYXzcunxrjft/\|()1[]?-_+~<>i!I;:,    "
count = len(CODE_LIB)

def transform_ascii(image_file): 
    image_file = image_file.convert("L") 
    code_pic = '' 
    for h in range(0,image_file.size[1]):
        for w in range(0,image_file.size[0]): 
            gray = image_file.getpixel((w,h))
            code_pic = code_pic + CODE_LIB[int(((count-1)*gray)/256)]
        code_pic = code_pic + "\n" 
    return code_pic

def play_music(filename):
    playsound(filename)

def convert_image():
    fn = input("input file name : ")
    hratio = float(input("input height zoom ratio(default 1.0) : ") or "1.0")
    wratio = float(input("input width zoom ratio(default 1.0) : ") or "1.0")
    fp = open(fn,'rb')
    image_file = Image.open(fp)
    image_file=image_file.resize((int(image_file.size[0]*wratio), int(image_file.size[1]*hratio)))
    print(u'Size info:',image_file.size[0],' ',image_file.size[1],' ')
    tmp = open('result.txt','w')
    trans_data = transform_ascii(image_file)
    print(trans_data)
    tmp.write(trans_data)
    tmp.close()

def convert_video():
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
        k = cv2.waitKey(5)

        os.system('cls') 
        i += 1
        tmp = open('./out/BA('+str(i)+').txt','w') 
        frame = cv2.resize(frame, (0,0), fx=wratio, fy=hratio)
        frame = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)) 
        trans_data = transform_ascii(frame) 
        print(trans_data) 
        tmp.write(trans_data) 
        tmp.close() 

        if (k & 0xff == ord('q')): 
            break 
    cap.release() 
    cv2.destroyAllWindows() 

def play_ascii_video():
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
        except IOError:
            break

if __name__ == '__main__':
    vflag = int(input("select type: \n1.Convert Image\t2.Convert Video\t3.Play Converted Video:\n"))

    if(vflag == 1 or vflag == 2):
        v = input("Use default dictionary(y/n):")
        if(v == 'n'):
            CODE_LIB = input("select dictionary:")
            count = len(CODE_LIB)

    if(vflag == 1):
        convert_image()
    elif(vflag == 2):
        convert_video()
    else:
        play_ascii_video()

    os.system('pause')