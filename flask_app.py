from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3 as sql,random,os,base64,string

app = Flask(__name__,static_url_path='')
app.secret_key = os.urandom(24)

def checkbal():
     con = sql.connect("invo.db")
     cur=con.cursor()
     cur.execute("select balance from users where email = ?",(session['user'],))
     qw = cur.fetchone();
     er=str(qw)
     balance=er[2:-3]
     cur.close()
     con.close()
     session['balance']=balance
                 
@app.route('/invochain')
def invoindex():
     return render_template("invologin.html")

@app.route('/invologin')
def invologin():
     if g.user:
          return redirect(url_for('invomaindash'))
     else:
          return render_template("invologin.html")

@app.route('/invomaindash')
def invomaindash():
     if g.user:
          checkbal()
          if session['msg']==0:
               return render_template("invoindex.html",name=session['name'],balance=session['balance'])
          elif session['msg']!=0:
               error=session['msg']
               session['msg']=0
               return render_template("invoindex.html",error=error,name=session['name'],balance=session['balance'])
     else:
          return redirect(url_for('invologin'))
     
@app.before_request
def before_request():
     g.user = None
     if 'user' in session:
          g.user = session['user']

@app.route('/logout')
def logout():
     session.pop('user', None)
     return redirect(url_for('invoindex'))

@app.route('/invoregistration', methods=['GET','POST'])
def invoaddrec():
     if g.user:
          return redirect(url_for('invomaindash'))
     else:
          if request.method == 'POST':
               if request.form['password'] == request.form['repass']:
                    con=sql.connect('BP.db')
                    cur=con.cursor()
                    name = request.form['username']
                    phone = request.form['phone']
                    email = request.form['email']
                    email = email.lower()
                    password = request.form['password']
                    balance = "0.00"
                    cur.execute("INSERT INTO users (name,email,password,phone,balance)VALUES (?,?,?,?,?)",(name,email,password,phone,balance))
                    con.commit()
                    msg = "Congrats! You have successfully registered! Please Login"
                    cur.close()
                    con.close()
                    return render_template("invologin.html",error = msg)
               else:
                    msg = "Password Confirmation Didnt Match the Password"
                    return render_template("invoregister.html",error=msg)
     return render_template("invoregister.html")
    
@app.route('/invosearch', methods = ['POST'])
def invosearch():
     if request.method == 'POST':
          con = sql.connect("invo.db")
          username = request.form['email']
          password= request.form['password']
          cur = con.cursor()
          username = username.lower()
          cur.execute("select password from users where email = ?",(username,))
          a = cur.fetchone();
          ta=str(a)
          output=ta[2:-3]
          cur.execute("select name from users where email = ?",(username,))
          b = cur.fetchone();
          tb=str(b)
          name=tb[2:-3]
          session.pop('user', None)
          if request.form['password'] == output and output != '':
               session['user'] = request.form['email']
               session['name'] = name
               session['msg']=0
               cur.close()
               con.close()
               return redirect(url_for('invomaindash'))
          else:
               error='Invalid Credentials! Please Try Again'
               return render_template('invologin.html',error=error)
     return render_template('invologin.html')


@app.route('/addmoney',methods = ['POST'])
def addmoney():
     if request.method == 'POST':
          balance = float(session['balance'])
          add = request.form['addmoney']
          newbal = float(add)+balance
          con = sql.connect("invo.db")
          cur=con.cursor()
          cur.execute("UPDATE users SET balance = (?) WHERE email = (?);",(str(newbal),session['user'],))
          con.commit()
          cur.close()
          con.close()
          session['msg']="Transaction Successful!"
          return redirect(url_for('invomaindash'))

@app.route('/paymoney',methods = ['POST'])
def paymoney():
     if request.method == 'POST':
          balance = float(session['balance'])
          pay = request.form['paymoney']
          if (balance-float(pay))>=0:
               newbal = balance-float(pay)
               con = sql.connect("invo.db")
               cur=con.cursor()
               cur.execute("UPDATE users SET balance = (?) WHERE email = (?);",(str(newbal),session['user'],))
               con.commit()
               cur.close()
               con.close()
               session['msg']="Transaction Successful!"
               return redirect(url_for('invomaindash'))
          else:
               session['msg']="Transaction Failed! Insufficient Funds"
               return redirect(url_for('invomaindash'))


if __name__ == '__main__':
   app.run(host='127.0.0.2',port=5000,debug=True)
