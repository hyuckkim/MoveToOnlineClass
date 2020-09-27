# coding=utf-8
import os.path
import time
import re
import webbrowser
from selenium import webdriver
from bs4 import BeautifulSoup
    
def login():
    driver.get(site)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="j_username"]').send_keys(studentid);
    driver.find_element_by_xpath('//*[@id="j_password"]').send_keys(studentpassword);
    driver.find_element_by_xpath('/html/body/div/div[2]/div/form/div/div[1]/fieldset/div/button').click();
    alert = driver.switch_to_alert()
    alert.accept()

def CheckStatus(link):
    driver.execute_script('window.open("about:blank", "_blank");')
    driver.switch_to_window(driver.window_handles[-1])
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for x in soup.select('li > span:nth-child(2)')[1:]:
        FindResult(checkResult[-1],re.findall(regex, str(x)))
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
def FindResult(li, st):
    for x in li:
        if(x[0] == st):
            x[1] += 1
            return
    li.append([st,1])
    
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
    linknum = 1

    checkResult.append([st])
    while(True): # 한 시간 안에 여러 링크가 있을 경우를 위한 반복.
        print(linkNow)
        CheckStatus(linkNow[linknum])
        if linknum + 1 == len(linkNow): break # 모든 링크를 열었을 때 나가기.
        linknum += 1

#Const 변수 설정.
DAYS = ('월','화','수','목','금','토','일')
MY_PATH = os.path.abspath(os.path.dirname(__file__))
regex = r'[가-힇]+'

#ClassInfo 파일 관리.
path = os.path.join(MY_PATH, 'ClassInfo.txt')
classfile = open(path,'r')
lines = classfile.readlines()
classfile.close()

filterdlines = []
subject = []
splitscajul = []
subjectResult = []
checkResult = []

#config 파일 관리
configpath = os.path.join(MY_PATH, 'config.txt')
configfile = open(configpath,'r',encoding='UTF-8')
originalconfigs = [RemoveEnter(x) for x in configfile.readlines()]

site = originalconfigs[0]
webroute = originalconfigs[1]
browser = originalconfigs[2]
studentid = originalconfigs[3]
studentpassword = originalconfigs[4]

if browser == "chrome":
    driver = webdriver.Chrome(webroute)
elif browser =="edge":
    driver = webdriver.Edge(webroute)
elif browser =="firefox":
    driver = webdriver.Firefox(executable_path=webroute)
elif browser =="safari":
    driver = webdriver.Safari(webroute)

login();

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
print('데이터가 확인되었습니다 : ')
bowlingString = ''
u = 0
for x in subject:
    u += 1
    bowlingString += (('' if u == 1 else ', ') + x[0])
print(bowlingString)
u = 0
bowlingString = ''
for x in splitscajul:
    u += 1
    bowlingString += (str(u) + '교시 : ' + x[0]+ '  ')
print(bowlingString)
timestart = 1
subnum = 0 # 시간을 나타내는 변수. 1교시에 1, 2교시에 2..
print(splitscajul)
for x in splitscajul[timestart - 1:]: # 오늘의 스케줄을 반복.
    subnum += 1
    LinkOpenByName(x,subnum + timestart - 1)
print(checkResult)
q = 0
for x in splitscajul[timestart - 1:]:
    print(checkResult[q])
    q += 1
y = input('press any key to continue...')
