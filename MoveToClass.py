# coding=utf-8
import os.path
import time
import webbrowser

def RemoveEnter(str):
    if(str[-1] == '\n'):
        return str[:-1]

def FindSubject(str):
    for x in subject:
        if(x[0] == str):
            return x[1]
    return ""
def FindSubjectList(str):
    for x in subject:
        if(x[0] == str):
            return x
    return ""
def LinkOpenByName(st, subjectnum):
    linkNow = FindSubjectList(st)
    print(str(subjectnum) + '교시 : ' + st)
    linknum = 0
    for i in linkNow[1:]:
        if linknum == 0:
            print('링크 주소 : ' + i)
            linknum = 1
        else:
            print('            ' + i)
    if configs[2] == 'N': y = input('링크로 들어가시려면 Enter 키를 눌러주세요...')
    else: print('링크를 엽니다...')
    linknum = 1
    while(True):
        webbrowser.open(linkNow[linknum])
        if linknum + 1 == len(linkNow): break
        linknum += 1
        if configs[2] == 'N' and configs[3] == 'N': y = input('다음 링크로 들어가시려면 Enter 키를 눌러주세요...')

#Const 변수 설정.
DAYS = ('월','화','수','목','금','토','일')
my_path = os.path.abspath(os.path.dirname(__file__))

# Config 파일 관리.
path = os.path.join(my_path, 'Config.txt')
configfile = open(path,'r')
originalconfigs = configfile.readlines()
configs = [RemoveEnter(ss)[-1] for ss in originalconfigs]
configfile.close()

conutilint = 0
if configs[-1] == 'Y':
    for x in originalconfigs[:-1]:
        while True:
            configtemp = input(str(x.split(' : ')[:-1]) + ' (Y 또는 N) : ')
            if(configtemp == 'Y' or configtemp == 'N'):
                configs[conutilint] = configtemp
                break
        conutilint += 1
        

#ClassInfo 파일 관리.
path = os.path.join(my_path, 'ClassInfo.txt')
classfile = open(path,'r')
lines = classfile.readlines()
classfile.close()

filterdlines = []
subject = []
splitscajul = []

for x in lines:
    filterdlines.append(RemoveEnter(x))
phase = 1
dayofweek = 0
links = 0 
obsolute = 0
for x in filterdlines: # 파일 불러오기
    if(phase == 1): # 과목 정보 입력
        if x == '': # 과목 정보의 입력을 마칠 때
            if len(subject) != 0 and links == 0: # 링크 없이 남는 과목 이름이 있다면
                print('과목 ' + subject[-1][0] + ' : 링크가 없어 무시됩니다')
                del subject[-1]
            phase = 2
        elif x[:4] == 'http': # 과목 링크를 달 때
            if(obsolute == 0): # 과목이 이미 있어 무시할 때 빼
                links += 1
                subject[-1].append(x)
        else: # 과목 이름을 입력할 때
            if len(subject) != 0 and links == 0: # 링크 없이 남는 과목 이름이 있다면
                print('과목 ' + subject[-1][0] + ' : 링크가 없어 무시됩니다')
                del subject[-1]
            if FindSubject(x) != '': # 만들려는 과목 정보가 이미 있다
                print('과목 ' + x + ' : 이미 있어 무시됩니다')
                obsolute = 1
            else: # 정상적으로 과목 정보가 만들어질 때
                obsolute = 0
                subject.append([x])
                links = 0
    elif(phase == 2): # 시간표 입력
        dayofweek += 1 # 단순히 시간표의 요일 개수만을 받는 변수.
        if dayofweek > 7: 
            print('요일이 너무 많습니다. 7개를 초과하는 요일 테이터는 무시됩니다.')
            break
        splitscajul.append(x.split())
if configs[5] == 'Y': splitscajul.append(input('오늘의 시간표를 입력해주세요 : ').split())
if configs[0] == configs[1] == 'N':
    print('데이터가 확인되었습니다.')
else:
    print('데이터가 확인되었습니다 : ')
if configs[0] == 'Y': 
    for x in subject:
        print(x)
if configs[1] == 'Y': 
    for x in splitscajul:
        print(x)
todayint = time.localtime().tm_wday
if configs[5] == 'Y': 
    todayint = len(splitscajul) - 1
print('오늘의 요일을 확인합니다 : ')
if(configs[5] == 'N' and time.localtime().tm_wday > len(splitscajul)): # 선언한 요일 변수 개수와 요일을 비교.
    print('오늘은 ' + DAYS[time.localtime().tm_wday] + '요일 입니다. 오늘은 수업이 없습니다.')
elif(len(splitscajul[time.localtime().tm_wday]) == 0): # 요일의 과목 문자열 길이가 0이면.
    print('오늘은 ' + DAYS[time.localtime().tm_wday] + '요일 입니다. 오늘은 수업이 없습니다.')
else:
    print('오늘은 ' + DAYS[time.localtime().tm_wday] + '요일 입니다.')
    if configs[4] == 'Y': LinkOpenByName('출석', 0) # 5번 설정이 Y면 출석 링크 열
    subnum = 0 # 시간을 나타내는 변수. 1교시에 1, 2교시에 2..
    for x in splitscajul[todayint]: # 오늘의 스케줄을 반복.
        subnum += 1
        LinkOpenByName(x,subnum)

y = input('오늘의 페이지는 여기까지입니다. 그만하시려면 Enter 키를 눌러주세요...')
