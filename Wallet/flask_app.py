from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3 as sql,random,os,base64,string

app = Flask(__name__,static_url_path='')
app.secret_key = os.urandom(24)

@app.route('/')
def index():
     return render_template("index.html")


@app.route('/logout')
def logout():
     session.pop('user', None)
     return redirect(url_for('invoindex'))
    
@app.route('/invosearch', methods = ['POST'])
def invosearch():
     if request.method == 'POST':
          con = sql.connect("invo.db")
          cur = con.cursor()
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

if __name__ == '__main__':
   app.run(host='127.0.0.2',port=5000,debug=True)
