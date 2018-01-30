import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='RangeDB.db'):
    new = not os.path.exists(path)
    db = sqlite3.connect(path)
    if new:
        c = db.cursor()
        c.execute('CREATE TABLE userbox (id INTEGER PRIMARY KEY,'
                  ' cla TEXT, stuid TEXT, name TEXT, phone TEXT)')
        add_user(db, '1A', '603410024', 'RangeWang', '0919000000')
        add_user(db, '1A', '603410002', 'AliceChen', '0919111111')
        add_user(db, '1A', '603410003', 'BessHuang', '0919222222')
        add_user(db, '1A', '603410004', 'FukwueLuo', '0919333333')
        add_user(db, '1A', '603410005', 'DebbeyXie', '0919444444')
        add_user(db, '1B', '603410006', 'DeneaHong', '0919555555')
        add_user(db, '1B', '603410007', 'ErineeLin', '0919666666')
        add_user(db, '1B', '603410008', 'JanefuYeh', '0919777777')
        add_user(db, '1B', '603410009', 'Leesssang', '0919888888')
        add_user(db, '1B', '603410010', 'MaybeWang', '0919999999')
        add_user(db, '1B', '603410011', 'NanaHuang', '0919101010')
        db.commit()
    return db

def add_user(db, cla, stuid, name, phone):
    db.cursor().execute('INSERT INTO userbox (cla, stuid, name, phone)'
                        ' VALUES (?, ?, ?, ?)', (cla, stuid, name, phone))
def get_cla(db,stuid):
    c = db.cursor()
    sqlcmd = 'SELECT * FROM userbox'
    c.execute(sqlcmd)
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    box =  [Row(*row) for row in c.fetchall()]
    num = len(box)
    i=0
    clas = ''
    while(i<num):
        if str(box[i][2]) == stuid:
            clas = box[i][1]
        i+=1
    return clas

def get_name(db,stuid):
    c = db.cursor()
    sqlcmd = 'SELECT * FROM userbox'
    c.execute(sqlcmd)
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    box =  [Row(*row) for row in c.fetchall()]
    num = len(box)
    i=0
    name = ''
    while(i<num):
        if str(box[i][2]) == stuid:
            name = box[i][3]
        i+=1
    return name

def get_list(db, cla):
    c = db.cursor()
    sqlcmd = 'SELECT * FROM userbox WHERE cla = "'+cla +'"'
    c.execute(sqlcmd)
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]

def update_info(db, phone, stuid):
    sqlcmd = 'UPDATE userbox SET phone = "'+phone+'" WHERE stuid = "'+stuid+'"'
    db.cursor().execute(sqlcmd)

def showlist(db,cla):
    box = get_list(db,cla)
    num = len(box)
    i=0
    prt_str = ''
    ulist = []
    while(i<num):
        j=1
        while(j<5):
            prt_str = prt_str + str(box[i][j]) + '  '
            j+=1
        #prt_str = prt_str + '&lt;br&gt;'
        ulist.append(prt_str)
        prt_str = ''
        i+=1
    #prt_str = '<p>'+prt_str+'</p>'
    #return ulist
    #return prt_str   
    return box 

if __name__ == '__main__':
    db = open_database()
    
