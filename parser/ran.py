import urllib.parse
import urllib.request
import sys, time, threading, os
from time import gmtime, strftime
import lin,random

def retrieve_data(url,num,maxn):
    #url = 'https://wwwmail.ccu.edu.tw/'
    try:
         values = { }
         data = urllib.parse.urlencode(values)
         data = data.encode('utf-8')
         req = urllib.request.Request(url, data)
         with urllib.request.urlopen(req) as response:
             backpage = response.read()
         #print(backpage)
         tt = random.randint(0,999999)
         ts = strftime("%H%M%S", gmtime())
         filename = 'page'+str(tt)+'.txt'
         filename = './page_file/'+filename
         fw = open(filename,'w')
         fw.write(backpage.decode("utf-8"))
         fw.close()
         lin.read_file(filename,url,num,maxn)

         print(ts + ' retrieve at ' + url)
         #========================
         #num += 1
         #if num == 200:
             #sys.exit()
         #print(num)
         #========================
         #t = threading.Thread(target=retrieve_data , args = (url,num))
         #t.sart()
    except:
         nothing=0
         #print('error in retrieve  ' + str(num) +' '+url)
def check_id(idnum, urls):
    try:
        #print('**'+idnum+'**')
        allnum = ''
        if(len(idnum)!=10):
             return False
        if(idnum[0:1].isdigit()):
             return False
        headword = idnum[0:1]
        if not(idnum[1:10].isdigit()):
             return False
        #print(str(idnum[1:2]))
        if(idnum[1:2] != '2' and idnum[1:2] !='1'):
             return False
        for ii in "ABCDEFGHJKLMNPQRSTUVWXYZ":
             if ii == headword:
                 allnum = str(ord(headword)-55) + idnum[1:10]
        for ii in "abcdefghjklmnpqrstuvwxyz":
             if ii == headword:
                 allnum = str(ord(headword)-87) + idnum[1:10]
        if(headword == 'I' or headword == 'i'):
             allnum = '34' + idnum[1:10]
        if(headword == 'O' or headword == 'o'):
             allnum = '35' + idnum[1:10]
 
        totalnum = int(allnum[0:1]) + int(allnum[1:2])*9 + int(allnum[2:3])*8 + int(allnum[3:4])*7 + int(allnum[4:5])*6 + int(allnum[5:6])*5 + int(allnum[6:7])*4 + int(allnum[7:8])*3 + int(allnum[8:9])*2 + int(allnum[9:10])*1 + int(allnum[10:11])
        #print(str(totalnum))
        if (totalnum % 10)!=0:
            return False
        else:
            pri_str = ' Data : ' +idnum+ '  from : ' + urls
            print('\n\n'+pri_str+'\n\n')
            sdoi = open('sensitive_data_of_id.txt','a')
            pri_str = pri_str + '\n'
            sdoi.write(pri_str)
            sdoi.close()
            return True
    except:
        nothing=0
        #print('error in check_id')

def check_phone(phone, urls):
    try:
        allnum = '09'
        if(phone[0:2]=='09'):
            start_num = 2
            while(len(allnum)!=10 and start_num < 12):
                if(phone[start_num:start_num+1].isdigit()):
                    allnum = allnum + str(phone[start_num:start_num+1])
                start_num +=1
        #print(allnum)
            if(len(allnum)==10):
                pri_str = ' Data : ' +allnum+ '  from : ' + urls
                print('\n\n'+pri_str+'\n\n')
                sdop = open('sensitive_data_of_phone.txt','a')
                pri_str = pri_str + '\n'
                sdop.write(pri_str)
                sdop.close()

        else:
            return False
    except:
        nothing=0
        #print('error in check_phone')  

def check_list(url):
    wi = url +'\n'
    flag = 0
    file = open('weblist.txt','r')
    for line in file.readlines():
        #print('u***'+wi+'***')
        #print('***'+line+'***')
        if(line == wi):
           flag = 1
    file.close()
    if(flag == 0):
        log = open('weblist.txt','a')
        log.write(wi)
        log.close()
    if(flag == 0):
        return True
    else:
        return False

def check_last(url):
    lennum = len(url)
    flag = 0
    ss = url[lennum-3:lennum]
    #print(url[lennum-3:lennum])
    if(ss == 'doc' or ss=='gif' or ss =='jpg' or ss == 'png' or ss == 'css' or ss == 'pdf' or ss == 'ico' or ss =='rar' or ss =='ocx' or ss =='ppt'):
        flag = 1
    if flag ==1:
        return False
    else:
        return True

def clean_page():
    try:
        tt = strftime("%S", gmtime())
        if tt == '59':
            oscmd = 'rm ./page_file/page*'
            os.system(oscmd)
    except:
        nothing = 0    

def count_q(url):
    ll = len(url)
    init = 0
    count = 0
    while(init<ll):
       init +=1
       if(url[init:init+1]=='?'):
           count+=1
    return count

def count_f(url):
    ll = len(url)
    init = 0
    count = 0
    while(init<ll):
       init +=1
       if(url[init:init+1]=='/'):
           count+=1
    return count


def check_sharp(url):
    flag = 0
    try:
        if(url.index('#')>10):
            flag = 1
    except:
        noth = 0

    try:
        if(url.index('./.')>10):
            flag = 1
    except:
        noth = 0

    try:
        if(url.index('/./')>10):
            flag = 1
    except:
        noth = 0

    try:
        if(url.index(' ')>10):
            flag = 1
    except:
        noth = 0

    try:
        if(url.index('..')>10):
            flag = 1
    except:
        noth = 0
    return flag
if __name__ == '__main__':
    __author__ = 'RangeWang'
    url = input('Input the URL: ')
    if check_id(url,'a'):
        print('ok')
    #check_phone(url,'t')
    #if check_id(url):
        #print('OK')
    #retrieve_data(url)
    #num = 1
    #t = threading.Thread(target=retrieve_data , args = (url,num))
    #t.start()
    #print('HI*********************************************************')
