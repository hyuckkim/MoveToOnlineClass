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
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, 'ClassInfo.txt')
print(path)
classfile = open(path,'r')

lines = classfile.readlines()
filterdlines = []
subject = []
splitscajul = []

for x in lines:
    filterdlines.append(RemoveEnter(x))
phase = 1
square = 0
alldays = 0
obsolute = 0
for x in filterdlines:
    if(phase == 1):
        if(square == 0):
            square = 1
            if(x == ""):
                phase = 2
            else:
                if FindSubject(x) == "":
                    subject.append([x,""])
                else:
                    print('과목 ' + x + ' : 이미 있어 무시됩니다')
                    obsolute = 1
        else:
            square = 0
            if(x != ""):
                if obsolute == 0:
                    subject[-1][1] = x
            else:
                if obsolute == 0:
                    print('과목 ' + subject[-1][0] + '에 대한 링크가 없어 과목이 누락되었습니다.')
                del subject[-1]
                phase = 2
    elif(phase == 2):
        alldays += 1
        if alldays == 8:
            print('요일이 너무 많습니다. 7개를 초과하는 요일 테이터는 무시됩니다.')
            break
        splitscajul.append(x.split())
print('데이터가 확인되었습니다 : ')
for x in subject:
    print(x)
for x in splitscajul:
    print(x)
classfile.close()

print('오늘의 요일을 확인합니다 : ')
if(time.localtime().tm_wday > len(splitscajul)):
    print('오늘은 ' + days[time.localtime().tm_wday] + '요일 입니다. 오늘은 수업이 없습니다.')
else:
    print('오늘은 ' + days[time.localtime().tm_wday] + '요일 입니다.')
    
for x in splitscajul[time.localtime().tm_wday]:
    linkNow = FindSubject(x)
    print(linkNow)
    webbrowser.open(linkNow)
    y = input('계속하시려면 Enter 키를 눌러주세요...')

y = input('오늘의 페이지는 여기까지입니다. 그만하시려면 Enter 키를 눌러주세요...')

