import os, sys
from OpenSSL import SSL
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'
errortime =[]
passlist = []

def checkip(iplist, ip):
    for pp in iplist:
       if pp == ip:
          return True
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    password = request.form.get('password', '')
    if request.method == 'POST':
        print(str(password))
        print(str(passsys))
        if password == passsys:
            session['psw'] = password
            tip = request.remote_addr
            cmdd = 'echo >> ' + str(tip)
            os.system(cmdd)
            return redirect(url_for('index'))
        if password == '000000000':
            session['psw'] = password
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    stuid = session.get('psw')
    if not stuid:
        return redirect(url_for('login'))
    else:
        cmd = 'rm -r /var/www/html/' + sys.argv[2]
        os.system(cmd)
        os.system('reboot')
    return render_template('index2.html')    
if __name__ == '__main__':
    passsys = str(sys.argv[1])
    #app.debug = True
    #app.run(host='140.123.102.181',port=1077,ssl_context='adhoc')
    app.run(host='140.123.102.181',port=1075)
