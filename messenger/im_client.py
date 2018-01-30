
import sys, socket, select,string,os

def get_cmd(ori_user,str):
    #print('cmd ***' + str)
    if(str[0:5] == 'block'):
       print('login failure')
       sys.exit()
    if(str[0:5] == 'login'):
       print('login successfully')
    if(str[0:5] == 'logim'):
       print(str)
    if(str[0:4] == 'send'):
       fun_send(ori_user,str)
    if(str[0:9] == 'broadcast'):
       fun_broadcast(str)
    if(str[0:5] == 'listO'):
       fun_listuser(ori_user,str)
    if(str[0:4] == 'poke'):
       fun_poke(ori_user,str)

def fun_poke(ori_user,str):
    box = str.split()
    if(ori_user == box[1]):
        print(box[2]+' poke you !! ')

def fun_block():
    while True:
        m=0

def fun_listuser(ori_user,str):
    box = str.split()
    if(len(box)<3):
        print('Error split')
    #print(ori_user + ' ** ' + box[len(box)-1])
    if(ori_user == box[len(box)-1]):
       totalsaynum = 1
       totalsay = ''
       while(totalsaynum<(len(box)-1)):
           totalsay = totalsay + box[totalsaynum] + ' '
           totalsaynum +=1
       print(totalsay)

def fun_send(ori_user,str):
    box = str.split()
    if(len(box)<3):
        print('Error split')
    if(ori_user == box[1]):
       totalsaynum = 2
       totalsay = ''
       while(totalsaynum<(len(box)-1)):
           totalsay = totalsay + box[totalsaynum] + ' '
           totalsaynum +=1
       print(box[len(box)-1] + ' say : ' + totalsay)

def fun_broadcast(str):
    box = str.split()
    if(len(box)<2):
        print('Error 1')
    totalsaynum = 1
    totalsay = ''
    while(totalsaynum<(len(box)-1)):
        totalsay = totalsay + box[totalsaynum] + ' '
        totalsaynum +=1
    print('(broadcast) ' + box[len(box)-1] + ' say : ' +totalsay)

def fun_get_passpw():
    os.system("stty -echo")
    hiddenpass = input('passwd:')
    os.system("stty echo")
    return hiddenpass

def fun_main_client():
    user = input('user:')
    pwd = fun_get_passpw()
    initlog = 0
    host = '140.123.102.181'
    port = 2050
    istalk = 0
    talkfromwho = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
     
    print('Connected to remote host.')

    while True:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(1024)
                if not data :
                    print('\nDisconnected from server')
                    sys.exit()
                else:
                    
                    strd = data.decode("utf-8")
                    if(strd[0:5]=='sendt'):
                        istalk = 1
                        boxq = strd.split()
                        whona = boxq[len(boxq)-1]
                        talkfromwho = whona
                        if(len(boxq)<3):
                            print('Error split')
                        if(user == boxq[1]):
                            totalsaynum = 2
                            totalsay = ''
                            while(totalsaynum<(len(boxq)-1)):
                               totalsay = totalsay + boxq[totalsaynum] + ' '
                               totalsaynum +=1
                            print(' ' + totalsay + '\n')
                            if(totalsay == 'exit talk'):
                                istalk = 0
                    else:
                        get_cmd(user,data.decode("utf-8"))
            
            else :
                if(initlog == 0):
                    userpwd = user + '@@@' + pwd
                    s.send(str.encode(userpwd))
                    initlog+=1
                else:
                    if(istalk == 1):
                       talktxt = input(' ')
                       if(talktxt == 'exit talk'):
                           istalk = 0
                           print('you exit the talk with ' + talkfromwho)
                           sss22 = 'send ' + talkfromwho + 'exit talk' + user
                       else:
                           sss22 = 'sendt ' + talkfromwho + ' ' + talktxt + ' ' + user
                           s.send(str.encode(sss22))
                    else:
                        msg = input(' ')
                        boxa = msg.split()   
                        if(msg == 'cls'):
                           for i in range(50):
                              print(' ')
                           msg = ''
                           msg = input('')
                        elif(msg[0:4] == 'talk'):
                           istalk = 1
                           talktxt = input('talk ' + boxa[1] + ' now : ')
                           sss22 = 'sendt ' +boxa[1] + ' ' + talktxt + ' ' + user
                           s.send(str.encode(sss22))
                        elif(msg == 'logout'):
                           logoutcheck = input('Are you sure? (yes or no) : ')
                           if(logoutcheck == 'y' or logoutcheck == 'yes'):
                              print('[System Say] bye!')
                          #try catch to do
                              try: 
                                 s.send(str.encode('logout*****' + user))
                                 sys.exit()
                              except:
                                 sys.exit()
                        elif(msg == 'listuser'):
                           s.send(str.encode('listuser '+user))
                        else:    
                           s.send(str.encode(msg + ' ' + user))


if __name__ == "__main__":

    __author__ = 'RangeWang'
    sys.exit(fun_main_client())

