from __future__ import with_statement
from contextlib import closing
from pprint import pprint
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', 'r') as f:
            db.cursor().executescript(f.read())
            # db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()


# configuration
DATABASE = './katta.db'
DEBUG = True
SECRET_KEY = 'development key'
USERID = ''
USERNAME = ''
NICKNAME = ''
PASSWORD = ''
MAINCOMUID = ''


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# データベースに接続するメソッド
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# データベースの値を判定するメソッド
def NaPlist():
    cur = g.db.execute('select userid, username, nickname, password, maincomuid from users order by userid')
    NaPdict = [dict(userid=row[0], username=row[1], nickname=row[2], password=row[3], maincomuid=row[4]) for row in cur.fetchall()]
    x = [['' for i in range(5)]for j in range(len(NaPdict))]
    for ii in range(len(NaPdict)):
        x[ii][0] = NaPdict[ii]["userid"]
        x[ii][1] = NaPdict[ii]["username"]
        x[ii][2] = NaPdict[ii]["nickname"]
        x[ii][3] = NaPdict[ii]["password"]
        x[ii][4] = NaPdict[ii]["maincomuid"]
        ii += 1
    return x
def myNaP(username):
    x = NaPlist()
    y = []
    for i in range(len(x)):
        y.append(x[i][1])
        i += 1
    if username in y:
        correctpassword = x[y.index(username)][3]
    else:
        correctpassword = "0000"
    return correctpassword
def getID(username):
    x = NaPlist()
    y = []
    for i in range(len(x)):
        y.append(x[i][1])
        i += 1
    if username in y:
        app.config['USERID'] = x[y.index(username)][0]
        app.config['NICKNAME'] = x[y.index(username)][2]
        app.config['PASSWORD'] = x[y.index(username)][3]
        app.config['MAINCOMUID'] = x[y.index(username)][4]
def getName(userid):
    x = NaPlist()
    y = []
    ans = "anknown user"
    for i in range(len(x)):
        if userid == x[i][0]:
            ans = x[i][1]
        i += 1
    return ans
def getNicname(userid):
    x = NaPlist()
    y = []
    ans = "anknown user"
    for i in range(len(x)):
        if userid == x[i][0]:
            ans = x[i][2]
        i += 1
    return ans
def CNaPlist():
    cur = g.db.execute('select * from comunity order by comuid')
    CNaPdict = [dict(comuid=row[0], comuname=row[1], comupass=row[2]) for row in cur.fetchall()]
    cx = [['' for i in range(3)]for j in range(len(CNaPdict))]
    for ii in range(len(CNaPdict)):
        cx[ii][0] = CNaPdict[ii]["comuid"]
        cx[ii][1] = CNaPdict[ii]["comuname"]
        cx[ii][2] = CNaPdict[ii]["comupass"]
        ii += 1
    return cx
def getComuN(comuid):
    cx = CNaPlist()
    cy = []
    for i in range(len(cx)):
        cy.append(cx[i][0])
        i += 1
    if comuid in cy:
        comun = cx[cy.index(comuid)][1]
    else:
        comun = 0
    return comun
def getComuP(comuid):
    cx = CNaPlist()
    cy = []
    for i in range(len(cx)):
        cy.append(cx[i][0])
        i += 1
    if comuid in cy:
        comun = cx[cy.index(comuid)][2]
    else:
        comun = 0
    return comun
def getComuI(comuname):
    cx = CNaPlist()
    cy = []
    for i in range(len(cx)):
        cy.append(cx[i][1])
        i += 1
    if comuname in cy:
        comui = cx[cy.index(comuname)][0]
    else:
        comui = 0
    return comui
def checkmybelongs(userid):
    cur = g.db.execute('select entcomuid from belongs where entuserid = ?', [userid])
    MyBdict = [dict(entcomuid=row[0]) for row in cur.fetchall()]
    mx = ['' for i in range(len(MyBdict))]
    for ii in range(len(MyBdict)):
        mx[ii] = MyBdict[ii]["entcomuid"]
        ii += 1
    return mx
def checkourbelongs(comuid):
    cur = g.db.execute('select entuserid from belongs where entcomuid = ?', [comuid])
    MyBdict = [dict(entuserid=row[0]) for row in cur.fetchall()]
    mx = ['' for i in range(len(MyBdict))]
    for ii in range(len(MyBdict)):
        mx[ii] = MyBdict[ii]["entuserid"]
        ii += 1
    return mx

def checkcomubuys(comuid):
    cur = g.db.execute('select * from comubuys where buycomuid = ?', [comuid])
    MyBdict = [dict(comubuysid=row[0], buycomuid=row[1], buyuserid=row[2], comubuy=row[3], comubuytime=row[4], comuetc=row[5], comubflag=row[6]) for row in cur.fetchall()]
    mx = [['' for i in range(7)] for j in range(len(MyBdict))]
    for i in range(len(MyBdict)):
        mx[i][0] = MyBdict[i]['comubuysid']
        mx[i][1] = MyBdict[i]['buycomuid']
        mx[i][2] = MyBdict[i]['buyuserid']
        mx[i][3] = MyBdict[i]['comubuy']
        mx[i][4] = MyBdict[i]['comubuytime']
        mx[i][5] = MyBdict[i]['comuetc']
        mx[i][6] = MyBdict[i]['comubflag']
        i += 1
    return mx
def checkmybuys(userid):
    cur = g.db.execute('select * from mybuys where buymyid = ?', [userid])
    MyBdict = [dict(mybuysid=row[0], buymyid=row[1], mybuy=row[2], mybuytime=row[3], myetc=row[4], mybflag=row[5]) for row in cur.fetchall()]
    mx = [['' for i in range(6)] for j in range(len(MyBdict))]
    for i in range(len(MyBdict)):
        mx[i][0] = MyBdict[i]['mybuysid']
        mx[i][1] = MyBdict[i]['buymyid']
        mx[i][2] = MyBdict[i]['mybuy']
        mx[i][3] = MyBdict[i]['mybuytime']
        mx[i][4] = MyBdict[i]['myetc']
        mx[i][5] = MyBdict[i]['mybflag']
        i += 1
    return mx
def mkkattes(comuid, fromurl):
    comuname = getComuN(comuid)
    memberids = checkourbelongs(comuid)
    x = NaPlist()
    members = []
    for i in range(len(memberids)):
        for j in range(len(x)):
            if memberids[i] == x[j][0]:
                members.append(x[j][2])
            j += 1
        i += 1
    katteslist = checkcomubuys(comuid)
    kattes = []
    for i in range(len(katteslist)):
        if katteslist[i][6] == 0:
            addeduser = getNicname(katteslist[i][2])
            kattabutton = "http://localhost:8080/kattapushed?comubuysid=" + str(katteslist[i][0]) + "&comefrom=" + fromurl
            kattes.append(dict(comubuysid=katteslist[i][0], buyuserid=addeduser, comubuy=katteslist[i][3], comubuytime=katteslist[i][4], comuetc=katteslist[i][5], comubflag=katteslist[i][6], kattabutton=kattabutton))
        i += 1
    return kattes
def mkkaos(userid, fromurl):
    kaoslist = checkmybuys(userid)
    kaos = []
    for i in range(len(kaoslist)):
        if kaoslist[i][5] == 0:
            mkattabutton = "http://localhost:8080/mkattapushed?mybuysid=" + str(kaoslist[i][0]) + "&comefrom=" + fromurl
            kaos.append(dict(mybuysid=kaoslist[i][0], buymyid=kaoslist[i][1], mybuy=kaoslist[i][2], mybuytime=kaoslist[i][3], myetc=kaoslist[i][4], mybflag=kaoslist[i][5], mkattabutton=mkattabutton))
        i += 1
    return kaos




@app.before_request
def before_request():
    g.db = connect_db()
    if session.get('logged_in'):
        if app.config['USERNAME'] == '':
            logout()
@app.after_request
def after_request(response):
    g.db.close()
    return response
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/kattapushed', methods=['GET'])
def kattapushed():
    comubuysid = request.args.get('comubuysid', type=int)
    comefrom = request.args.get('comefrom', type=str)
    cur = g.db.execute('select * from comubuys where comubuysid = ?', [comubuysid])
    MyBdict = [dict(comubuysid=row[0], buycomuid=row[1], buyuserid=row[2], comubuy=row[3], comubuytime=row[4], comuetc=row[5]) for row in cur.fetchall()]
    g.db.commit()
    comubdict = MyBdict[0]
    g.db.execute('update comubuys set comubflag = 1 where comubuysid = ?',[comubuysid])
    g.db.commit()
    g.db.execute('insert into comubhist (comubuysid, buycomuid, buyuserid, boughtuserid, comubuy, comubuytime, comuetc) values(?,?,?,?,?,?,?)', [comubdict['comubuysid'], comubdict['buycomuid'], comubdict['buyuserid'], app.config['USERID'], comubdict['comubuy'], comubdict['comubuytime'], comubdict['comuetc']])
    g.db.commit()
    return redirect(comefrom)
@app.route('/kattahist', methods=['GET'])
def kattahist():
    comuid = request.args.get('comuid', type=int)
    cur = g.db.execute('select * from comubhist where buycomuid = ? order by comubhsid desc',[comuid])
    CHdict = [dict(comubhsid=row[0], comubuysid=row[1], buycomuid=row[2], buyuserid=row[3], boughtuserid=row[4], comubuy=row[5], comubuytime=row[6], kattatime=row[7], comuetc=row[8]) for row in cur.fetchall()]
    mx = [['' for i in range(9)] for j in range(len(CHdict))]
    for i in range(len(CHdict)):
        mx[i][0] = CHdict[i]['comubhsid']
        mx[i][1] = CHdict[i]['comubuysid']
        mx[i][2] = CHdict[i]['buycomuid']
        mx[i][3] = CHdict[i]['buyuserid']
        mx[i][4] = CHdict[i]['boughtuserid']
        mx[i][5] = CHdict[i]['comubuy']
        mx[i][6] = CHdict[i]['comubuytime']
        mx[i][7] = CHdict[i]['kattatime']
        mx[i][8] = CHdict[i]['comuetc']
        i += 1
    kattahists = []
    comuname = getComuN(comuid)
    for i in range(len(CHdict)):
        buyuser = getNicname(mx[i][3])
        boughtuser = getNicname(mx[i][4])
        kattahists.append(dict(comubhsid=mx[i][0],buyuser=buyuser,boughtuser=boughtuser,comubuy=mx[i][5], comubuytime=mx[i][6],kattatime=mx[i][7],comuetc=mx[i][8]))
        i += 1
    return render_template('kattahist.html', comuname=comuname,kattahists=kattahists)
@app.route('/mkattapushed', methods=['GET'])
def mkattapushed():
    mybuysid = request.args.get('mybuysid', type=int)
    comefrom = request.args.get('comefrom', type=str)
    cur = g.db.execute('select * from mybuys where mybuysid = ?', [mybuysid])
    MyBdict = [dict(mybuysid=row[0], buymyid=row[1], mybuy=row[2], mybuytime=row[3], myetc=row[4]) for row in cur.fetchall()]
    g.db.commit()
    mybdict = MyBdict[0]
    g.db.execute('update mybuys set mybflag = 1 where mybuysid = ?',[mybuysid])
    g.db.commit()
    g.db.execute('insert into mybhist (mybuysid, buymyid, mybuy, mybuytime, myetc) values(?,?,?,?,?)', [mybdict['mybuysid'], mybdict['buymyid'], mybdict['mybuy'], mybdict['mybuytime'], mybdict['myetc']])
    g.db.commit()
    return redirect(comefrom)
@app.route('/mkattahist', methods=['GET'])
def mkattahist():
    cur = g.db.execute('select * from mybhist where buymyid = ? order by mybhsid desc',[app.config['USERID']])
    CHdict = [dict(mybhsid=row[0], mybuysid=row[1], buymyid=row[2], mybuy=row[3], mybuytime=row[4], kattatime=row[5], myetc=row[6]) for row in cur.fetchall()]
    mx = [['' for i in range(7)] for j in range(len(CHdict))]
    for i in range(len(CHdict)):
        mx[i][0] = CHdict[i]['mybhsid']
        mx[i][1] = CHdict[i]['mybuysid']
        mx[i][2] = CHdict[i]['buymyid']
        mx[i][3] = CHdict[i]['mybuy']
        mx[i][4] = CHdict[i]['mybuytime']
        mx[i][5] = CHdict[i]['kattatime']
        mx[i][6] = CHdict[i]['myetc']
        i += 1
    mkattahists = []
    for i in range(len(CHdict)):
        mkattahists.append(dict(mybhsid=mx[i][0],mybuy=mx[i][3], mybuytime=mx[i][4],kattatime=mx[i][5],myetc=mx[i][6]))
        i += 1
    return render_template('mkattahist.html',myname=app.config['NICKNAME'],mkattahists=mkattahists)




@app.route('/')
def tologin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('mypage'))

@app.route('/mypage', methods=['POST','GET'])
def mypage():
    mynickname = app.config['NICKNAME']
    maincmname = getComuN(app.config['MAINCOMUID'])
    fromurl = "http://localhost:8080/mypage"
    kattes = mkkattes(app.config['MAINCOMUID'], fromurl)
    # 以下しばらくKatte追加用
    mycomuids = checkmybelongs(app.config['USERID'])
    if app.config['MAINCOMUID'] in mycomuids:
        mycomuids.remove(app.config['MAINCOMUID'])
    nowmycomuslength = len(mycomuids)
    mycomus = []
    for i in range(nowmycomuslength):
        mycomus.append(getComuN(mycomuids[i]))
        i += 1
    if request.method == 'POST':  #コミュニティ用Katte追加用
        addbuycomuidpre = request.form['mycomus']
        if addbuycomuidpre != "Kao":
            addbuycomuid = getComuI(addbuycomuidpre)
            addcomubuy = request.form['comubuy']
            addcomuetc = request.form['comuetc']
            g.db.execute('insert into comubuys (buycomuid, buyuserid, comubuy, comuetc) values(?, ?, ?, ?)',[addbuycomuid, app.config['USERID'], addcomubuy, addcomuetc])
            g.db.commit()
            flash('Added New Katte')
        else:
            addmybuy = request.form['comubuy']
            addmyetc = request.form['comuetc']
            g.db.execute('insert into mybuys (buymyid, mybuy, myetc) values(?, ?, ?)',[app.config['USERID'], addmybuy, addmyetc])
            g.db.commit()
            flash('Added New Kao')
        return redirect(url_for('mypage'))
    # Kao表示用
    kaos = mkkaos(app.config['USERID'], fromurl)
    kattahisturl = "http://localhost:8080/kattahist?comuid=" + str(app.config['MAINCOMUID'])
    mkattahisturl = "http://localhost:8080/mkattahist"
    return render_template('mypage.html',NICKNAME=mynickname, maincomuid=app.config['MAINCOMUID'], maincomuname=maincmname, kattes=kattes,mycomus=mycomus,nowmycomuslength=nowmycomuslength,kaos=kaos,kattahisturl=kattahisturl,mkattahisturl=mkattahisturl)
@app.route('/mycomutop')
def mycomutop():
    mbids = checkmybelongs(app.config['USERID'])
    mycomunities = []
    for mbid in mbids:
        mbname = getComuN(mbid)
        comuurl = "http://localhost:8080/comutop?comuid=" + str(mbid)
        mycomunities.append(dict(comuid=mbid, comuname=mbname, comuurl=comuurl))
    return render_template('mycomutop.html',mycomunities=mycomunities)
@app.route('/comutop', methods=['GET'])
def comutop():
    comuid = request.args.get('comuid', type=int)
    fromurl = "http://localhost:8080/comutop?comuid=" + str(comuid)
    kattes = mkkattes(comuid, fromurl)
    comuname = getComuN(comuid)
    memberids = checkourbelongs(comuid)
    x = NaPlist()
    members = []
    for i in range(len(memberids)):
        for j in range(len(x)):
            if memberids[i] == x[j][0]:
                members.append(x[j][2])
            j += 1
        i += 1
    kattahisturl = "http://localhost:8080/kattahist?comuid=" + str(comuid)
    return render_template('comutop.html', kattahisturl=kattahisturl, comuname=comuname, comuid=comuid, members=members, kattes=kattes)
@app.route('/allcomukattes')
def allcomukattes():
    mbids = checkmybelongs(app.config['USERID']) #自分の入ってるコミュニティのID
    mycomunities = []
    for mbid in mbids: #コミュニティID１個につきの作業
        fromurl = "http://localhost:8080/allcomukattes"
        kattes = mkkattes(mbid, fromurl)
        mbname = getComuN(mbid)#コミュニティの名前取得
        mycomunities.append(dict(comuname=mbname, kattes=kattes))
    return render_template('allmycomukattes.html', mycomunities=mycomunities)


@app.route('/checkmyprof')
def checkmyprof():
    passasta = ''
    for i in range(len(app.config['PASSWORD'])):
        passasta = passasta + '*'
        i += 1
    maincm = getComuN(app.config['MAINCOMUID'])
    if maincm == 0:
        maincm = "メインコミュニティを設定してください"
    prof = [app.config['USERNAME'], app.config['NICKNAME'], passasta, maincm]
    return render_template('checkmyprof.html', prof=prof)
@app.route('/changemynickname')
def changemynickname():
    getID(app.config['USERNAME'])
    return render_template('changemynickname.html', nownickname=app.config['NICKNAME'])
@app.route('/changemynn', methods=['POST'])
def changemynn():
    g.db.execute('update users set nickname = ? where userid = ?', [request.form['newnickname'], app.config['USERID']])
    g.db.commit()
    app.config['NICKNAME'] = request.form['newnickname']
    flash('New nickname was successfully posted')
    return redirect(url_for('checkmyprof'))
@app.route('/changemypasswd')
def changemypasswd():
    getID(app.config['USERNAME'])
    return render_template('changemypasswd.html', nowpasswd=app.config['PASSWORD'])
@app.route('/changemypw', methods=['POST'])
def changemypw():
    g.db.execute('update users set password = ? where userid = ?', [request.form['newpasswd'], app.config['USERID']])
    g.db.commit()
    app.config['PASSWORD'] = request.form['newpasswd']
    flash('New password was successfully posted')
    return redirect(url_for('checkmyprof'))
@app.route('/changemymaincomu')
def changemymaincomu():
    nowmaincomu = getComuN(app.config['MAINCOMUID'])
    if nowmaincomu == 0:
        nowmaincomu = "メインコミュニティを設定していません"
    nowmycomus = []
    nowmycomuids = checkmybelongs(app.config['USERID'])
    for i in range(len(nowmycomuids)):
        nowmycomus.append(getComuN(nowmycomuids[i]))
        i += 1
    nowmycomuslength = len(nowmycomus)
    return render_template('changemymaincomu.html', nowmaincomu=nowmaincomu, nowmycomuslength=nowmycomuslength, nowmycomus=nowmycomus)
@app.route('/changemymc', methods=['POST'])
def changemymc():
    newmymcname = request.form['newmymaincomu']
    newmymaincomuid = getComuI(newmymcname)
    print(app.config['MAINCOMUID'])
    if newmymaincomuid != 0:
        g.db.execute('update users set maincomuid = ? where userid = ?', [newmymaincomuid, app.config['USERID']])
        g.db.commit()
        app.config['MAINCOMUID'] = newmymaincomuid
        flash('New maincomunity was successfully posted')
    else:
        flash('A trable was happend')
    return redirect(url_for('checkmyprof'))
@app.route('/addmycomu', methods=['GET', 'POST'])
def addmycomu():
    error = None
    if request.method == 'POST':
        amcflag = 0
        addcomuid = int(request.form['comuid'])
        nowmycomus = checkmybelongs(app.config['USERID'])
        for i in range(len(nowmycomus)):
            if nowmycomus[i] == addcomuid:
                amcflag = 1
            i += 1
        if amcflag == 1:
            flash('You have already joined this comunity')
            return redirect(url_for('checkmyprof'))
        else:
            orgcmpass = getComuP(addcomuid)
            if request.form['comupass'] == orgcmpass:
                g.db.execute('insert into belongs values(?,?)', [addcomuid, app.config['USERID']])
                g.db.commit()
                flash('You were joined')
                return redirect(url_for('mypage'))
            elif request.form['comupass'] != orgcmpass:
                error = 'Invalid password'
            elif orgcmpass == 0:
                error = 'There are no id'
            else:
                error = 'There are no id'
    return render_template('addmycomu.html', error=error)
@app.route('/addcomunity', methods=['GET','POST'])
def addcomunity():
    error = ""
    if request.method == 'POST':
        if request.form['comupass'] != 0 and request.form['comupass'] != '0000':
            g.db.execute('insert into comunity (comuname, comupass) values (?, ?)',
                        [request.form['comuname'], request.form['comupass']])
            g.db.commit()
            cid = getComuI(request.form['comuname'])
            g.db.execute('insert into belongs values(?, ?)', [cid, app.config['USERID']])
            g.db.commit()
            flash('New comunity was successfully added')
            return redirect(url_for('mypage'))
        else:
            flash('you can not set this password')
    return render_template('addcomunity.html', error=error)


# ログインとログアウト
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # 改造中
        app.config['USERNAME'] = request.form['username']
        tmpname = app.config['USERNAME']
        orgpass = myNaP(app.config['USERNAME'])
        app.config['PASSWORD'] = orgpass
        if request.form['password'] == app.config['PASSWORD'] and request.form['username'] == app.config['USERNAME']:
            session['logged_in'] = True
            getID(app.config['USERNAME'])
            flash('You were logged in')
            return redirect(url_for('mypage'))
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        elif app.config['PASSWORD'] == "0000":
            error = 'There are no id'
        else:
            error = 'There are no id'
    return render_template('login.html', error=error)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


# ユーザーの追加
@app.route('/adduser', methods=['GET','POST'])
def adduser():
    error = ""
    if request.method == 'POST':
        mkuserflag = myNaP(request.form['username'])
        if mkuserflag != "0000":
            flash('you can not set this username')
        elif request.form['password'] != 0 and request.form['password'] != '0000':
            g.db.execute('insert into users (username, nickname, password) values (?, ?, ?)',
                        [request.form['username'], request.form['nickname'], request.form['password']])
            g.db.commit()
            flash('New user was successfully added')
            return redirect(url_for('login'))
        else:
            flash('you can not set this password')
    return render_template('adduser.html', error=error)
