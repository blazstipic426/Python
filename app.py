from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = "many random bytes"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)

# Check MySQL connection status
@app.route('/')
def home():
    if 'username' in session:
       
        cue=mysql.connection.cursor()
        cue.execute("SELECT Name,Date_create, Description FROM data_post")
        dataa=cue.fetchall()
        cue.close()
        

        return render_template('home.html',username=session['username'],data=dataa)
    else:
        
        return redirect(url_for('login'))
    



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        pwd =request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and pwd ==user[1]:
            session['username'] = user[0]
            
            return redirect(url_for('home'))
        else:
            return render_template('login.html',error='Invalid username or password')
    
    return render_template('login.html')




@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username =request.form['username']
        email=request.form['email']
        pwd =request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(f"Insert into tbl_users (username,email,password) values('{username}','{email}','{pwd}')")
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('login.html')



@app.route('/add_post')
def add_post():
    return render_template('add.html')






@app.route('/Posts/<string:name>', methods=['GET', 'POST'])
def posts_add(name):

    if request.method =='POST':
        updated_name=request.form['Name']
        
        updated_description=request.form['Description']
        updated_date=datetime.now()

        cur = mysql.connection.cursor()
        cur.execute("UPDATE data_post SET Name = %s, Date_create =%s, Description = %s WHERE Name = %s",(updated_name, updated_date,updated_description, name))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))




    else:
        cur=mysql.connection.cursor()
        cur.execute("SELECT Name, Date_create,Description FROM data_post WHERE Name=%s",(name,))
        row = cur.fetchone()
        cur.close()
            
            
        return render_template('Posts.html', roww=row)





if __name__ == '__main__':
    app.run(debug=True)
