from flask import Flask, session, redirect, url_for, escape, request,render_template,jsonify
app = Flask(__name__)
import sqlite3
con=sqlite3.connect('database.db')
con.execute( '''CREATE TABLE IF NOT EXISTS admin
       ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
       USERNAME           TEXT    NOT NULL,
       PASSWORD           TEXT NOT NULL);''')
con.execute( '''CREATE TABLE IF NOT EXISTS contact
       ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
       USERID         INTEGER ,
       NAME           TEXT    ,
       CONTACT           TEXT NOT NULL);''')

con.close()


@app.route('/')
def home():
    if 'username' in session:
        user=escape(session['username'])
        return render_template('home.html',username=user.upper())
    else:    
        return render_template('admin.html')

@app.route('/login')
def login():
        return render_template('logincnt.html')

@app.route('/loginn/',methods=['POST'])
def login_contact():        
        username=request.form["username"]
        password=request.form["password"]
        con=sqlite3.connect('database.db')
        sql="SELECT * from admin WHERE USERNAME='%s' AND PASSWORD='%s'" %(username,password)
        admin=con.execute(sql)
        lisadmin=list(admin)
        lenadmin=len(lisadmin)
        if lenadmin==0:
            details="Invalid user"
            return jsonify({'details':details})
        
        else:
            print username,lisadmin
            session['username']=username
            con.close()
            details="success"
            return jsonify({'details':details}) 
    


@app.route('/signup',methods=['POST','GET'])
def signup():
  if request.method=='GET':
     return render_template('signup.html')
  else: 
    username=request.form["username"]
    paswrd=request.form["password"]
    cnfpaswrd=request.form["confirmpassword"]
    if len(username)==0:
        return render_template('paserr.html')
    else:
        if paswrd!=cnfpaswrd:
            return render_template('cnpas.html')
        else:
            con=sqlite3.connect('database.db')
            usql="SELECT * from admin WHERE USERNAME='%s'" %(username)
            usr=con.execute(usql)
            usrlis=list(usr)
            if len(usrlis)==0:
                sql="INSERT INTO admin (USERNAME,PASSWORD) VALUES ('%s','%s')" %(username,cnfpaswrd)
                con.execute(sql)
                con.commit()
                con.close()
                session['username']=username
                return redirect('/home')
            else:
                return render_template('signuperr.html')    
                

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
            
@app.route('/home')
def homepage():
    user=escape(session['username'])
    return render_template('home.html',username=user.upper())


@app.route('/addcont')
def add_con():
    user=escape(session['username'])
    return render_template('addcon.html',username=user.upper())

@app.route('/add', methods=["POST"])
def add():
    con=sqlite3.connect('database.db')
    user=escape(session['username'])
    usql="SELECT * from admin WHERE USERNAME='%s'" %(user)
    uid=con.execute(usql)
    userid=list(uid)
    usid=userid[0][0]
    nam=request.form['name']
    num= request.form['number']
    sql="SELECT * from contact WHERE NAME='%s'" %(nam)
    n=con.execute(sql)
    namlis=list(n)
    if len(namlis)==0:
        sql="INSERT INTO contact (USERID,NAME,CONTACT) VALUES ('%s','%s','%s')" %(usid,nam,num)
        con.execute(sql)
        con.commit()
        con.close()
        details="Details added successfully"
        return jsonify({'details':details})
    else:
        details="Details already added"
        return jsonify({'details':details})    

@app.route('/allcontact')
def veiw_all():
    con=sqlite3.connect('database.db')
    user=escape(session['username'])
    usql="SELECT * from admin WHERE USERNAME='%s'" %(user)
    userid=con.execute(usql)
    usrid=list(userid)
    uid=usrid[0][0]
    csql="SELECT * from contact WHERE USERID='%s'" %(uid)
    cont=con.execute(csql)
    contact=list(cont)    
    name=[]
    number=[]
    for i in contact:
        us=str(i[2])
        name.append(us)
    for i in contact:
        num=str(i[3])
        number.append(num)    
    lename=range(len(name))
    con.close()
    return render_template('search.html',username=user.upper(),name=name,lename=lename,number=number)


@app.route('/search/')
def contact_search():
    con=sqlite3.connect('database.db')
    user=escape(session['username'])
    usql="SELECT * from admin WHERE USERNAME='%s'" %(user)
    uid=con.execute(usql)
    userid=list(uid)
    usid=userid[0][0]
    us= request.args.get('name')
    sql="SELECT * from contact WHERE NAME like '%s' AND USERID='%s'" %('%'+us+'%',usid)
    srch=con.execute(sql)
    srchlis=list(srch)
    name=[]
    number=[]
    print srchlis
    lename=len(srchlis)
    for i in srchlis:
        us=str(i[2])
        name.append(us)
    for i in srchlis:
        num=str(i[3])
        number.append(num)    
    le=range(len(name))
    con.close()
    return jsonify({'name':name,'number':number,})

@app.route('/edit')
def edit_con():
    user=escape(session['username'])
    return render_template('econ.html',username=user.upper())
 
@app.route('/editnum', methods=["POST"])
def edit_num():
    con=sqlite3.connect('database.db')
    user=escape(session['username'])
    usql="SELECT * from admin WHERE USERNAME='%s'" %(user)
    uid=con.execute(usql)
    userid=list(uid)
    usid=userid[0][0]
    nam=request.form['name']
    num= request.form['number']
    print num 
    sql="SELECT * from contact WHERE NAME='%s' AND USERID='%s'" %(nam,usid)
    n=con.execute(sql)
    na=list(n)
    print na
    if len(na)==0:
        error="Contact details not added"
        return jsonify({'details':error})
    else:    
        name=na[0][2]
        nsql="UPDATE contact set CONTACT='%s' WHERE NAME='%s'" %(num,name)
        con.execute(nsql)
        con.commit()
        con.close()
        details="Details updated"
        return jsonify({'details':details})

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.run(debug=True,host='0.0.0.0',port=2000)