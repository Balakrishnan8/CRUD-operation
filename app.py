from flask import Flask,request,render_template,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "test"
app.config["MYSQL_DB"] = "Apps"

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def home():
	if request.method == "POST":
		detail = request.form
		name = detail["name"]
		age = detail["age"]
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO datatable(NAME,AGE) VALUES(%s, %s)",(name,age))
		mysql.connection.commit()
		cur.close()
		return redirect("/table")
	return render_template("index.html")

""" @app.route("/search",methods=['POST','GET'])
def se():
	sKey = request.form["sear"]
	cur = mysql.connection.cursor()
	res = cur.execute("SELECT * FROM datatable where NAME LIKE %s",(sKey,))
	tab = cur.fetchall()
	return render_template("table.html", userdetails = tab) """

@app.route("/table")
def fetch():
	cur = mysql.connection.cursor()
	res = cur.execute("SELECT * FROM datatable")
	tab = cur.fetchall()
	return render_template("table.html", userdetails = tab)


@app.route("/update/<name1>", methods=['GET','POST'])
def update(name1):
	if request.method == "POST":
		upval = request.form
		name = upval['name']
		age=upval["age"]
		cur = mysql.connection.cursor()
		cur.execute("UPDATE datatable SET NAME=%s,AGE=%s WHERE NAME=%s",(name,age,name1))
		mysql.connection.commit()
		cur.close()
		return redirect("/table")
	return render_template("update.html",name1=name1)

@app.route("/delete/<string:i>")
def delete(i):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM datatable WHERE NAME=%s",(i,))
	mysql.connection.commit()
	cur.close()
	return redirect("/table")

if __name__ == "__main__":
	app.run(debug=True,host="127.0.0.1",port=5050)
