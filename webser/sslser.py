
import bank, uuid, datetime, threading, os, time
from time import gmtime, strftime
from OpenSSL import SSL
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'
errortime =[]

def checkdigit(p):
    lenstr = len(p)
    re = False
    for inn in p:
        if (inn.isdigit() or inn=='(' or inn ==')' or inn =='-'):
            re = True
        else:
            return False
    return re


def checkip(iplist, ip):
    for pp in iplist:
       if pp == ip:
          return True
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    visit_ip = request.remote_addr
    session['vip'] = visit_ip
    f = open('block-ip.txt','r')
    getip = f.read()
    bye_ip_list = getip.split()
    f.close()
    if checkip(bye_ip_list, visit_ip):
        abort(403)
    stuid = request.form.get('stuid', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (stuid, password) in [('603410024', 'range'), ('603410011', 'nana')]:
            session['stuid'] = stuid
            session['csrf_token'] = uuid.uuid4().hex
            logfile = open('logfile.txt','a')
            get_current_time = datetime.datetime.now()
            logfile.write(str(get_current_time) +' - '+ stuid + ' login successfully\n')
            logfile.close()
            return redirect(url_for('index'))
        else:
            logfile = open('logfile.txt','a')
            get_current_time = datetime.datetime.now()
            logfile.write(str(get_current_time) +' - '+ stuid + ' try to login but failure\n')
            logfile.close()
            #wip = visit_ip + '@@' 
    return render_template('login.html', stuid=stuid)

@app.route('/logout')
def logout():
    stuid = session.get('stuid')
    session.pop('stuid', None)
    logfile = open('logfile.txt','a')
    get_current_time = datetime.datetime.now()
    logfile.write(str(get_current_time) +' - '+ stuid + ' logout\n')
    logfile.close()
    return redirect(url_for('login'))

@app.route('/')
def index():
    stuid = session.get('stuid')
    if not stuid:
        return redirect(url_for('login'))
    
    visit_ip = session.get('vip')
    f = open('block-ip.txt','r')
    getip = f.read()
    bye_ip_list = getip.split()
    f.close()
    if checkip(bye_ip_list, visit_ip):
        abort(403)

    db = bank.open_database()
    cla = bank.get_cla(db, stuid)
    username = bank.get_name(db, stuid)
    userlist = bank.showlist(db, cla)
    return render_template('index.html',username=username, cla=cla, userlist=userlist)
  
@app.route('/update', methods=['GET', 'POST'])
def update():
    stuid = session.get('stuid')
    if not stuid:
        return redirect(url_for('login'))
    newphone = request.form.get('newphone', '').strip()
    complaint = None
    
    visit_ip = session.get('vip')
    f = open('block-ip.txt','r')
    getip = f.read()
    bye_ip_list = getip.split()
    f.close()
    if checkip(bye_ip_list, visit_ip):
        abort(403)

    if request.method == 'POST':
        if newphone:
            db = bank.open_database()
            msg = ''
            if checkdigit(newphone):
                 bank.update_info(db, newphone, stuid) 
                 db.commit()
                 msg = 'Update successful'
                 logfile = open('logfile.txt','a')
                 get_current_time = datetime.datetime.now()
                 logfile.write(str(get_current_time) +' - '+ stuid + ' update phone info with '+ newphone+'\n')
                 logfile.close()
            else:
                 msg = 'Update failure, please check your phone format'
                 logfile = open('logfile.txt','a')
                 get_current_time = datetime.datetime.now()
                 logfile.write(str(get_current_time) +' - '+ stuid + ' update failure with wrong format '+ newphone+'\n')
                 logfile.close()
            #==============================
            stuid = session.get('stuid')
            if not stuid:
                return redirect(url_for('login'))
            db = bank.open_database()
            cla = bank.get_cla(db, stuid)
            username = bank.get_name(db, stuid)
            userlist = bank.showlist(db, cla)
            #==============================
            return render_template('index.html',username=username, cla=cla, userlist=userlist, sqlmsg=msg)
    return render_template('update.html')

def backupthread():
    while True:
        #t = strftime("%M:%S", gmtime())
        #if(t=='59:59'):
        t = strftime("%S", gmtime())
        if(t=='59'):
            oscmd = 'tar cf ./backup/'+  strftime("%Y.%m.%d-%H.%M.%S", gmtime()) +'-backup.tar logfile.txt RangeDB.db block-ip.txt'
            os.system(oscmd)
            print('auto-backup at '+ strftime("%Y.%m.%d %H:%M:%S", gmtime()))
        time.sleep(1)

if __name__ == '__main__':
    app.debug = True
    t = threading.Thread(target=backupthread)
    t.start()
    app.run(host='0.0.0.0',port=5200,ssl_context='adhoc')
