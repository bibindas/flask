import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session,jsonify
from werkzeug import secure_filename
app = Flask(__name__, static_folder='/home/mrrobot/bibin/flask_app', static_url_path='/mystatic')
app.config['UPLOAD_FOLDER'] = '/home/mrrobot/bibin/flask_app/upload'
import sqlite3
con=sqlite3.connect('imager.db')
con.execute( '''CREATE TABLE IF NOT EXISTS admin
       ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
       USERNAME           TEXT    NOT NULL,
       PASSWORD           TEXT NOT NULL);''')
con.execute( '''CREATE TABLE IF NOT EXISTS file
       ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
       USERID         INTEGER ,
       FILENAME           TEXT    );''')

con.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/home')
def home():
    if 'username' in session:
        con=sqlite3.connect('imager.db')
        sql="SELECT * from file "
        fi=con.execute(sql)
        file=list(fi)
        files=[]
        for i in file:
            a=i[2]
            files.append(a)
        print file
        user=session['username']
        return render_template('homepage.html',files=files,user=user.upper())
    else:
        con=sqlite3.connect('imager.db')
        sql="SELECT * from file "
        fi=con.execute(sql)
        file=list(fi)
        files=[]
        for i in file:
            a=i[2]
            files.append(a)
        print file   
        return render_template('adminpage.html',files=files)


@app.route('/login')
def login():
        return render_template('loginpage.html')

@app.route('/loginn/',methods=['POST'])
def login_contact():        
        username=request.form["username"]
        password=request.form["password"]
        con=sqlite3.connect('imager.db')
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

@app.route('/signup')
def signup():
  if request.method=='GET':
     return render_template('signupage.html')

@app.route('/signupp/',methods=['POST']) 
def sign_up():
    username=request.form["username"]
    paswrd=request.form["password"]
    cnfpaswrd=request.form["confirmpassword"]
    if len(username)==0:
        details="Username null"
        return jsonify({'details':details})   

    else:
        if paswrd!=cnfpaswrd:
            details="Password incorrect"
            return jsonify({'details':details})
        else:
            con=sqlite3.connect('imager.db')
            usql="SELECT * from admin WHERE USERNAME='%s'" %(username)
            usr=con.execute(usql)
            usrlis=list(usr)
            if len(usrlis)==0:
                sql="INSERT INTO admin (USERNAME,PASSWORD) VALUES ('%s','%s')" %(username,cnfpaswrd)
                con.execute(sql)
                con.commit()
                con.close()
                session['username']=username
                details="success"
                return jsonify({'details':details})
            else:
                details="User already exist"
                return jsonify({'details':details})   

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/home')


@app.route('/home')
def index():
    return render_template('homepage.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method=='GET':
        return render_template('index.html')
    else:    
        up_file = request.files["file"]
        print up_file.filename
        up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], up_file.filename))
        con=con=sqlite3.connect('imager.db')
        user=session['username']
        adm="SELECT * from admin WHERE USERNAME='%s'"%(user)
        u=con.execute(adm)
        usr=list(u)
        usrid=usr[0][0]
        sq="SELECT * from file WHERE FILENAME='%s'" %(up_file.filename)
        fi=con.execute(sq)
        file=list(fi)
        if len(file)==0:
            sql="INSERT INTO file (USERID,FILENAME) VALUES ('%s','%s')" %(usrid,up_file.filename)
            con.execute(sql)
            con.commit()
            con.close()
            return render_template('upload.html',filename=up_file.filename)

@app.route('/gallery')
def imager_gallery():
    con=sqlite3.connect('imager.db')
    user=session['username']
    adm="SELECT * from admin WHERE USERNAME='%s'"%(user)
    u=con.execute(adm)
    usr=list(u)
    usrid=usr[0][0]
    sql="SELECT * from file WHERE USERID='%s'" %(usrid)
    fi=con.execute(sql)
    file=list(fi)
    files=[]
    for i in file:
        a=i[2]
        files.append(a)    
    return render_template('gallery.html',files=files ,user=user.upper())

@app.route('/delete')
def delete_image():
    return render_template('deletepage.html')

@app.route('/deletee',methods=['POST'])
def deletee():
    dfile=request.form['name']
    con=sqlite3.connect('imager.db')
    user=session['username']
    adm="SELECT * from admin WHERE USERNAME='%s'"%(user)
    u=con.execute(adm)
    usr=list(u)
    usrid=usr[0][0]
    isql="SELECT * from file WHERE FILENAME like '%s' AND USERID='%s' " %('%'+dfile+'%',usrid)
    fi=con.execute(isql)
    file=list(fi)
    if len(file)==0:
        details="Error"
        return jsonify({'details':details})
    file_name=file[0][2]
    sql="DELETE from file WHERE FILENAME='%s'" %(file_name)
    con.execute(sql)
    con.commit()
    con.close()
    details="success"
    return jsonify({'details':details})    

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.run(host="0.0.0.0",port=8000,debug=True)
