# coding=utf-8
import os.path
import time
import webbrowser

def RemoveEnter(str):
    if(str[-1] == '\n'):
        return str[0:-1]

def FindSubject(str):
    for x in subject:
        if(x[0] == str):
            return x[1]
    return ""
days = ['월','화','수','목','금','토','일']
if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6:
    print('오늘은 ' + days[time.localtime().tm_wday] + '요일 입니다. 수업이 없습니다.')
else:
    print('오늘은 ' + days[time.localtime().tm_wday] + '요일 입니다.')
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, 'ClassInfo.txt')
    classfile = open(path,'r')

    lines = classfile.readlines()
    filterdlines = []
    subject = []
    splitscajul = []

    for x in lines:
        filterdlines.append(RemoveEnter(x))
    phase = 1
    square = 0
    for x in filterdlines:
        if(phase == 1):
            if(square == 0):
                square = 1
                if(x == ""):
                    phase = 2
                else:
                    subject.append([x,""])
            else:
                square = 0
                subject[-1][1] = x
        elif(phase == 2):
            splitscajul.append(x.split())
    print('데이터가 확인되었습니다 : ')
    for x in subject:
        print(x)
    for x in splitscajul:
        print(x)
    for x in splitscajul[time.localtime().tm_wday]:
        linkNow = FindSubject(x)
        print(linkNow)
        webbrowser.open(linkNow)
        y = input('계속하시려면 Enter 키를 눌러주세요...')
    classfile.close()
y = input('계속하시려면 Enter 키를 눌러주세요...')

