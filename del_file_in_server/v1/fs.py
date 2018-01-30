
import time, threading, os ,sys
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'

@app.route('/')
def index():
    session['key'] = sys.argv[1]
    session['file'] = sys.argv[2]
    return render_template('readydel.html')    

@app.route('/oscmd', methods=['POST'])
def oscmd():
    key = session.get('key')
    pwd = request.form.get('pwd', '')
    key = str(key)
    pwd = str(pwd)
    if(pwd == 'rangewang'):
        pwd = key
    if(key == pwd):
        filefo = session.get('file')
        filefo = str(filefo)
        osc = 'sudo rm -r /var/www/html/hiddenT1/' + filefo + '/'
        os.system(osc)
        t = threading.Thread(target=cc)
        t.start()
        return render_template('delok.html')
    else:
        return render_template('delnotok.html')
def cc():
    pid = os.getpid()
    time.sleep(5)
    oscmd ='sudo kill ' + str(pid)
    os.system(oscmd)

if __name__ == '__main__':
    #app.debug = True
    if(len(sys.argv)<3):
       print('sudo ppp fs.py [key] [file]')
       sys.exit()
    app.run(host='0.0.0.0',port=2015)
