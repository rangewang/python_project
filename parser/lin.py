import sys, ran, threading, os, gc


def read_file(name,string,num,maxn):
      box = []
      sin = string
      #name = input('Please enter file name:')
      file =open(name, 'r' ,encoding='UTF-8')
      count = 0
      str1='cs.ccu.edu.tw'
      for line in file.readlines():
            head = 0
            tail = 6
            id_head = 0
            id_tail = 10
            phone_head = 0
            phone_tail = 12
            #print('Length: '+ str(len(line))+line)
            while tail < len(line):
                 if(line[head:tail]=='href=\"'):
                       head +=6
                       tail = head
                       while line[tail]!= '\"':
                             tail+=1
                       tmp = ''
                       flag = 1
                       #if(line[head]=='.'):
                             #tmp = tmp+ string +line[head+2:tail]
                       if (line[head:head+4]=='http'):
                             try:
                                 flag=line.index(str1) 
                                 tmp = line[head:tail]
                             except:
                                 flag = 0 
                       else:
                             get_str = line[head:tail]
                             if(get_str[0:1] == '#' or get_str =='.'):
                                  flag = 0
                             else:
                                 if(get_str[0:1]=='.'):
                                    get_str = get_str[1:]
                                 if(get_str[0:1]=='/'):
                                    get_str = get_str[1:]
                                 if(get_str[0:6]=='mailto' or get_str[0:6]=='javasc'):
                                    flag = 0
                                 else:
                                    try:
                                       #print('tag:   '+string)
                                       pls = int(string.rfind('/'))
                                       if(pls>10):
                                           string = string[0:pls]+'/'
                                       if(string[pls-1]=='/'):
                                           string = string + '/'
                                       #print('tag:   '+string)
                                    except:
                                       notthing=0
                                       #print('tag / ')
                                 tmp = string + get_str
                                 #print('tag:   '+tmp)
                       try:
                             flag=tmp.index(str1)
                       except:
                             flag = 0

                       if(ran.count_q(tmp)>2):
                             flag = 0
                       if(ran.count_f(tmp)>9):
                             flag = 0  
                       if(ran.check_sharp(tmp)==1):
                             flag = 0
                       if(flag > 0):
                             #print('tag:   '+tmp)
                             box.append(tmp) 
                             
                       count+=1
                 head= head + 1
                 tail=tail + 1
            while id_tail < len(line): 
                 ran.check_id(line[id_head:id_tail],sin)
                 id_head +=1
                 id_tail +=1 
            while phone_tail < len(line):
                 ran.check_phone(line[phone_head:phone_tail],sin)
                 phone_head +=1
                 phone_tail +=1
      #print('tag1')
      #print('lin >> '+ str(count))
      file.close() 
      #print('tag2')
      for i in box:
           try:
               #print(str(i))
               #print('lin box ' + num)
               #print('tag1')
               num+=1
               if int(maxn)!=0:
                   if num > int(maxn):
                     sys.exit()
               #print('tag2')
               #print(str(num))
               if(ran.check_last(str(i))):
                   if(ran.check_list(str(i))):
                        gc.collect()
                        #ran.clean_page()
                        t = threading.Thread(target=ran.retrieve_data , args = (str(i),num,maxn))
                        t.start()
           except:
               #print('error in box')
               nothing = 0

if __name__ == "__main__":
      
      __author__ = 'Boris'
      sys.exit()

