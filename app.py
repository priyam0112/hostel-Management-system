import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, flash, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
import yaml
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

app.secret_key = '1011'

db = yaml.load(open('hm.yaml'),Loader=yaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['username']
        password = userDetails['password']
        if password == "password08":
            return redirect('/index')

    return render_template('admin.html')

@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('intro.html')

@app.route('/Student Bookings' , methods=['GET', 'POST'])
def studentbook():
    if request.method == 'POST':
        userDetails = request.form
        usn = userDetails['usn']
        fname = userDetails['fname']
        lname = userDetails['lname']
        sem = userDetails['sem']
        phone = userDetails['pno']
        dept = userDetails['Dept']
        year = userDetails['year']
        hostel_name = "NOT DECIDED"
        fee_status = "NOT PAID"
        roomno = "NOT ALLOTTED"
        regex = ("(0|91)?[6-9][0-9]{9}$")
        p = re.compile(regex)
        if re.match(p, phone): #re.match
            cur = mysql.connection.cursor()
            resultVal = cur.execute("SELECT USN FROM STUDENT")
            record = cur.fetchall()
            for row in record:
                if usn == ''.join(row) or usn == '':
                    flash("Usn Can't Be Same")
                    return render_template('studentbook.html')
        
            cur.execute("INSERT INTO STUDENT VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(resultVal+1, usn, fname, lname, sem, phone, dept, year,hostel_name ,fee_status,roomno))
            mysql.connection.commit()
            resultVal = cur.execute("SELECT * FROM STUDENT")
            if resultVal > 0:
                return redirect('/Student Details')
        else:
            flash('Invalid Phone number')
            return render_template('studentbook.html')    
    return render_template('studentbook.html')


@app.route('/Reservation', methods=['GET','POST'])
def reserve():
    if request.method == 'POST':
        f = 0
        userDetails = request.form
        usn = userDetails['usn']
        hostelno = userDetails['hostelno']
        roomno = userDetails['roomno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT USN FROM STUDENT")
        record = cur.fetchall()
        for row in record:
            if usn == ''.join(row) or usn == '':
                f = 1
                print(usn)
                cur.execute("UPDATE STUDENT SET hostel_name=%s,fee_status=%s,roomno=%s WHERE usn=%s",(hostelno,"PAID",roomno,usn))
                mysql.connection.commit()
                return redirect('/Student Details')
            else:
                f = 0
        
        if f==0:
            flash('Usn Not Found')
            return render_template('reserve.html')

    return render_template('reserve.html')

@app.route('/Visitor', methods=['GET','POST'])
def visitor():
    if request.method == 'POST':
        userDetails = request.form
        visname = userDetails['visname']
        intime = userDetails['intime']
        outtime = userDetails['outtime']
        name = userDetails['studentname']
        pno = userDetails['pno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT name FROM HOSTEL")
        record = cur.fetchall()
        regex = ("(0|91)?[6-9][0-9]{9}$")
        p = re.compile(regex)
        if re.match(p, pno):
            for row in record:
                # if name == ''.join(row):
                resultval = cur.execute("SELECT * FROM VISITOR")
                cur.execute("INSERT INTO VISITOR VALUES (%s, %s, %s, %s, %s, %s)", ((resultval+1), visname, intime, outtime,name,pno))
                mysql.connection.commit()
                return redirect('/index')
                # else:
                #     flash("Name Not found")
                #     return render_template('studentbook.html')
        else:
            flash("Invalid Phone Number")
            return render_template('studentbook.html')

    return render_template('reserve.html')
    
@app.route('/Contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/About us')
def aboutus():
    return render_template('aboutus.html')

@app.route('/hostelrooms', methods=['GET','POST'])
def hostelRooms():
    if request.method == 'POST':
        userDetails = request.form
        usn = userDetails['usn']
        hostelno = userDetails['hostelno']
        roomno = userDetails['roomno']
        name = userDetails['name']
        furniture = userDetails['furniture']
        food = userDetails['food']
        cur = mysql.connection.cursor()
        cur.execute("SELECT USN FROM STUDENT")
        record = cur.fetchall()
        for row in record:
            if usn == ''.join(row) or usn == '':
                cur.execute("INSERT INTO HOSTEL VALUES (%s, %s, %s, %s, %s, %s)", (usn,hostelno,roomno,name,furniture,food))
                mysql.connection.commit()
                return redirect('/')
            else:
                flash("USN Not found")
                return render_template('hostelRooms.html')

    return render_template('hostelRooms.html')

@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method == 'POST':
        #Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        message = userDetails['msg']
        cur = mysql.connection.cursor()
        resultval = cur.execute("SELECT * FROM FEEDBACK")
        cur.execute("INSERT INTO FEEDBACK VALUES (%s, %s, %s, %s)", ((resultval+1), name, email, message))
        mysql.connection.commit()
        cur.close()
        return redirect('/')

    return render_template('aboutus.html')



@app.route('/Student Details')
def studentinfo():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM STUDENT')
    data1 = cursor.fetchall()
    return render_template('studentinfo.html', data=data1)




if __name__ == "__main__":
    app.run(debug=True)

