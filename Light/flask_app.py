from flask import Flask, render_template,redirect,url_for
import sqlite3 as sql

app = Flask (__name__)

global flag
flag = ""

@app.route('/')
def index():
	global flag
	con = sql.connect("/home/anantkaushik/mysite/task.db")
	cur = con.cursor()
	var = cur.execute("select * from status")
	var = str(cur.fetchone())[2:-3]
	flag = var
	if flag == 'ON':
		rflag = "OFF"
	else:
		rflag = "ON"
	cur.close()
	con.close()
	print(flag)
	return render_template("index.html",flag1=var,flag2=rflag)

@app.route('/setflag')
def setflag():
	global flag
	if flag == "ON":
		flag = "OFF"
		con = sql.connect("/home/anantkaushik/mysite/task.db")
		cur = con.cursor()
		var = cur.execute("update status set status = 'OFF'")
		con.commit()
		cur.close()
		con.close()
		print(flag)
	else:
		flag = "ON"
		con = sql.connect("/home/anantkaushik/mysite/task.db")
		cur = con.cursor()
		var = cur.execute("update status set status = 'ON'")
		con.commit()
		cur.close()
		con.close()
		print(flag)
	return redirect(url_for("index"))
if __name__ == '__main__':
   app.run(host='127.0.0.2',port=5000,debug=True)