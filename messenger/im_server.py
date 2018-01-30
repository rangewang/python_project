import sys,socket,select,os,datetime
RECV_BUFFER = 1024
socket_list = []

def fun_sendall(sc,sock,msg):
    for socket in socket_list:
        if(socket != sc and socket != sock):
           try:
               socket.sendall(msg)
           except:
               socket.close()
               if(socket in socket_list):
                  print('rm user') 
                  socket_list.remove(socket)

def fun_get_online_user():
    userbox = in_readfile()
    usernum = len(userbox)
    totaltex = ''
    i=0
    while(i<usernum):
        userinfo = userbox[i].split('(+)')
        if(userinfo[1] == '1'):
           totaltex = totaltex + userinfo[0] + '. '
        i+=1
    totaltex = 'listO The online users : ' + totaltex
    #print(totaltex)
    return totaltex
    
def init_doc():
    userbox = in_readfile()
    usernum = len(userbox)
    totaltex = ''
    i=0
    while(i<usernum):
        userinfo = userbox[i].split('(+)')
        totaltex = totaltex +userinfo[0]+'(+)0(+)NA(+)un'
        if(i!=(usernum-1)):
            totaltex = totaltex+'%$'
        i+=1
    f = open('list.txt','w')
    f.write(totaltex)
    f.close()

def in_readfile():
    f = open('list.txt','r')
    get_str = f.read()
    userbox = get_str.split('%$')
    f.close()
    return userbox

def write_doc(user,colnum,chw):
    userbox = in_readfile()
    usernum = len(userbox)
    totaltex = ''
    i=0
    while(i<usernum):
        userinfo = userbox[i].split('(+)')
        if(userinfo[0] == user):

            userinfo[colnum] = chw
        totaltex = totaltex + userinfo[0] + '(+)' + userinfo[1] + '(+)' + userinfo[2] + '(+)' + userinfo[3]
        if(i!=(usernum-1)):
            totaltex = totaltex + '%$'
        i+=1
    f = open('list.txt','w')
    f.write(totaltex)
    f.close()

def fun_get_user_status(str):
    userbox = in_readfile()
    usernum = len(userbox)
    i=0
    statusvalue = 9
    while(i<usernum):
        userinfo = userbox[i].split('(+)')
        if((str == 'range') or (str == 'nana') or (str == 'boss')):
            if(str == userinfo[0]):
                statusvalue = userinfo[1]
        i+=1
    return statusvalue

def fun_get_off_msg(str):
    status = fun_get_user_status(str)
    offmsg = ''
    if(status == '2'):
        userbox = in_readfile()
        usernum = len(userbox)
        i=0
        while(i<usernum):
           userinfo = userbox[i].split('(+)')
           if((str == 'range') or (str == 'nana') or (str == 'boss')):
               if(str == userinfo[0]):
                  offmsg = userinfo[2]
           i+=1
    return offmsg

def fun_login(userid,pw):
    if(userid == 'range'):
        if(pw == 'rangepw'):
            print('user: '+userid+' login succeedfully')
            return userid
    elif(userid == 'nana'):
        if(pw == 'nanapw'):
            print('user: '+userid+' login succeedfully')
            return userid
    elif(userid == 'boss'):
        if(pw == 'bosspw'):
            print('user: '+userid+' login succeedfully')
            return userid
    print('user: '+userid+' login blocked')
    return 'block'

def fun_get_login_status(str):
    userbox = in_readfile()
    usernum = len(userbox)
    i=0
    returndata = ''
    while(i<usernum):
        userinfo = userbox[i].split('(+)')
        #print(userinfo[0]+'  '+userinfo[3])
        if(str == userinfo[0]):
            returndata = userinfo[3]
        i+=1
    return returndata
if __name__ == "__main__":

    __author__ = 'RangeWang'
    init_doc()
    print('initialize the user status')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 2050))
    server_socket.listen(10)
    socket_list.append(server_socket)
    logfile = open('logfile-for-server.txt','w')
    print('Server started')
    while True:
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [], 0)
        
        for sock in read_sockets:
            #print(socket_list)
            if(sock == server_socket):
               sc, sockname = server_socket.accept()
               socket_list.append(sc)
            else:
               #print('accept side')
               data = sock.recv(RECV_BUFFER)
               if data:
                  get_current_time = datetime.datetime.now()
                  dedata = data.decode("utf-8")
                  logfile.write(str(get_current_time) +' - '+ dedata + '\n')
                  userpwd = dedata.split('@@@')
                  get_login = fun_get_login_status(userpwd[0])
                  ls_get = dedata.split()
                  status012 = fun_get_user_status(userpwd[0])
                  if(get_login == 'un'):
                     login_result = fun_login(userpwd[0],userpwd[1])
                     if(login_result == 'block'):
                        sock.sendall(str.encode('block'))
                        write_doc(userpwd[0],1,'0')
                        write_doc(userpwd[0],3,'un')
                        socket_list.remove(sock)
                     else:  
                        if(status012 == '0'):
                           write_doc(userpwd[0],1,'1')
                           write_doc(userpwd[0],3,'in')
                           sc.sendall(str.encode('login OK!'))
                        if(status012 == '2'):
                           offmsg = fun_get_off_msg(userpwd[0])               
                           sc.sendall(str.encode('logim OK,('+offmsg+')'))
                           write_doc(userpwd[0],1,'1')
                           write_doc(userpwd[0],2,'NA')
                           write_doc(userpwd[0],3,'in')
                  elif(ls_get[0] == 'listuser'):
                     onlist = fun_get_online_user()
                     debox = dedata.split()
                     fromuser = ls_get[1]
                     fromuser = onlist + ' ' + fromuser
                     #sc.sendall(str.encode(fromuser))
                     fun_sendall(server_socket,server_socket,str.encode(fromuser))
                      
                  elif(dedata == 'logout*****range'):
                     #print('tag . help me' + userpwd[0])
                     write_doc('range',1,'0')
                     write_doc('range',2,'NA')
                     write_doc('range',3,'un')

                  elif(dedata == 'logout*****nana'):
                     print('tag . help me' + userpwd[0])
                     write_doc('nana',1,'0')
                     write_doc('nana',2,'NA')
                     write_doc('nana',3,'un')
                  elif(dedata == 'logout*****boss'):
                     print('tag . help me' + userpwd[0])
                     write_doc('boss',1,'0')
                     write_doc('boss',2,'NA')
                     write_doc('boss',3,'un')

                     socket_list.remove(sock)
   
                  else:
                     fun_sendall(server_socket,sock,data)
                  
                  try:
                     d00 = data.decode("utf-8")
                     d01 = d00.split()
                     offmsg222 = fun_get_user_status(d01[1])
                     if(offmsg222 == '0' and d01[0] == 'send'):
                        write_doc(d01[1],1,'2')
                        totxt = ''
                        tonum = 2
                        while(tonum<(len(d01)-1)):
                           totxt = totxt + d01[tonum] + ' '
                           tonum += 1
                        writeword = d01[len(d01)-1] + ' say : ' + totxt
                        write_doc(d01[1],2, writeword)
                        #print(totxt)
                  except:
                     print(' ')
