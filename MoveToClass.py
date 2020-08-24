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
    linkNow = FindSubjectList(st) # linkNow는 이제 string list, 0번 항목은 과목이름, 1번 항목부터는 과목 링크.
    print(str(subjectnum) + '교시 : ' + st)
    linknum = 0
    for i in linkNow[1:]: # 모든 링크 표시를 위한 반복.
        if linknum == 0:
            print('링크 주소 : ' + i)
            linknum = 1
        else:
            print('            ' + i)
    if configs[2] == 'N': y = input('링크로 들어가시려면 Enter 키를 눌러주세요...')
    else: print('링크를 엽니다...')
    linknum = 1
    while(True): # 한 시간 안에 여러 링크가 있을 경우를 위한 반복.
        webbrowser.open(linkNow[linknum])
        if linknum + 1 == len(linkNow): break # 모든 링크를 열었을 때 나가기.
        linknum += 1
        if configs[2] == 'N' and configs[3] == 'N': y = input('다음 링크로 들어가시려면 Enter 키를 눌러주세요...')

#Const 변수 설정.
DAYS = ('월','화','수','목','금','토','일')
MY_PATH = os.path.abspath(os.path.dirname(__file__))

# Config 파일 관리.
path = os.path.join(MY_PATH, 'Config.txt')
configfile = open(path,'r')
originalconfigs = configfile.readlines()
configs = [RemoveEnter(ss).split(' : ')[-1] for ss in originalconfigs]
configfile.close()

# 설정 커스터마이징 설정.
conutilint = 0
conutilinn = 0
if configs[-1] == 'Y': # 마지막 설정이 '예' 일때 (모든 설정을 직접 설정할 때)
    for x in originalconfigs[:-1]:
        while True:
            configtemp = input(str(x.split(' : ')[:-1]) + ' (Y 또는 N) : ')
            if(configtemp == 'Y' or configtemp == 'N'): # Y나 N을 써야 나갈 수 있음.
                configs[conutilint] = configtemp
                break
        conutilint += 1
elif configs[-1] != 'N': # 마지막 설정이 '아니오' 가 아닐 때 (몇몇 설정을 직접 설정할 때)
    tempconnumbers = [int(num) for num in configs[-1].split()] # 설정 번호 숫자들 직접 추출
    for x in [originalconfigs[num] for num in tempconnumbers]: # 추출된 번호들마다의 문장들로 반복
        conutilint = tempconnumbers[conutilinn] # 문장 번호 넣기
        while True:
            print(configs[-1])
            configtemp = input(str(x.split(' : ')[:-1]) + ' (Y 또는 N) : ')
            if(configtemp == 'Y' or configtemp == 'N'): # Y나 N을 써야 나갈 수 있음.
                configs[conutilint] = configtemp
                break
        conutilinn += 1

#ClassInfo 파일 관리.
path = os.path.join(MY_PATH, 'ClassInfo.txt')
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
        if dayofweek > len(DAYS): 
            print('요일이 너무 많습니다. ' + str(len(DAYS)) + '개를 초과하는 요일 테이터는 무시됩니다.')
            break
        dayofweek += 1 # 단순히 시간표의 요일 개수만을 받는 변수.
        splitscajul.append(x.split())
if configs[5] == 'Y': splitscajul.append(input('오늘의 시간표를 입력해주세요 : ').split())
elif configs[6] == 'Y': splitscajul.append([subject[k][0] for k in range(len(subject))])
if configs[0] == configs[1] == 'N':
    print('데이터가 확인되었습니다.')
else:
    print('데이터가 확인되었습니다 : ')
if configs[0] == 'Y': 
    u = 0
    bowlingString = ''
    for x in subject:
        u += 1
        bowlingString += (str(u) + ' : ' + x[0] + '  ')
    print(bowlingString)
if configs[1] == 'Y': 
    u = 0
    bowlingString = ''
    for x in splitscajul:
        u += 1
        bowlingString += (str(u) + '교시 : ' + x[0]+ '  ')
    print(bowlingString)
if configs[5] == 'Y': 
    todayint = len(splitscajul) - 1
elif configs[6] == 'Y':
    todayint = len(splitscajul) - 1
else: todayint = time.localtime().tm_wday
print('오늘의 요일을 확인합니다 : ')
if((configs[5] == 'N' and configs[6] == 'N') and time.localtime().tm_wday > len(splitscajul)): # 선언한 요일 변수 개수와 요일을 비교.
    print('오늘은 ' + DAYS[time.localtime().tm_wday] + '요일 입니다. 오늘은 수업이 없습니다.')
elif(len(splitscajul[todayint]) == 0): # 요일의 과목 문자열 길이가 0이면.
    print('오늘은 ' + DAYS[time.localtime().tm_wday] + '요일 입니다. 오늘은 수업이 없습니다.')
else:
    print('오늘은 ' + DAYS[time.localtime().tm_wday] + '요일 입니다.')
    if configs[7] == 'Y': 
        while(True):
            try:
                timestart = int(input('시작할 시간의 번호를 골라주세요 : '))
                if timestart < 0:
                    print('번호는 0보다 작지 않은 정수로 입력해 주십시오. ')
                else: break
            except ValueError:
                print('번호는 0보다 작지 않은 정수로 입력해 주십시오. ')
    else: timestart = 0
    if configs[4] == 'Y' and timestart == 0: 
        LinkOpenByName('출석', 0) # 5번 설정이 Y면 출석 링크 열
        timestart += 1
    subnum = 0 # 시간을 나타내는 변수. 1교시에 1, 2교시에 2..
    for x in splitscajul[todayint][timestart - 1:]: # 오늘의 스케줄을 반복.
        subnum += 1
        LinkOpenByName(x,subnum + timestart - 1)

y = input('오늘의 페이지는 여기까지입니다. 그만하시려면 Enter 키를 눌러주세요...')
