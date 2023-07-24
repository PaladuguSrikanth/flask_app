from flask import Flask, render_template, request, redirect, session,flash
import sqlite3

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

aa =  ""

# List of users should have access to the signup 
signupOwnerList = ["srikanthpaladugu3@gmail.com", "bala@gmail.com"]

# List of users should have access to Read the all the users and can delete 
DBOwnerList = ["srikanthpaladugu3@gmail.com"]


# SQLite database initialization
def create_table():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, phone TEXT, country TEXT, password TEXT)")
    conn.commit()
    conn.close()

def insert_user(name, email, phone, country, password):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, phone, country, password) VALUES (?, ?, ?, ?, ?)", (name, email, phone, country, password))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT name, email, phone, country FROM users")
    data = c.fetchall()
    conn.close()
    return data





#Home route to index.html page
@app.route('/')
def home():
    global aa
    aa = ""
    return render_template('index.html')


#route to signup.html page only after completing verification route otherwie home route will redirect.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global aa
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        country = request.form['country']
        password = request.form['password']
        insert_user(name, email, phone, country, password)
        
        return redirect('/signin')
    
    if aa == "youCanViewSignup":
        aa = ""
        return render_template('signup.html')
    
    return redirect('/')

'''
route to signin.html page and after completion of validation and based on user 
it will go to the corresponding route(i.e portfolio and DataBase).

owners can view the database and rest of those can view portfolio

'''
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global aa
    aa = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("SELECT email, password, name FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        if user and user[1] == password:
            session['email'] = email
            session['name'] = user[2]
            if session['email'] in DBOwnerList:
                aa = ""
                return redirect('/sample')
            
            return redirect('/profile')
        else:
            aa = ""
            return render_template('signin.html', error='Invalid credentials')
    aa = ""
    return render_template('signin.html')




'''
route to verification.html page and after completion of validation and based on user 
it will go to the corresponding route(Signup).

owners only can signup to the application.

'''
@app.route('/verification', methods=['GET', 'POST'])
def verification():
    global aa
    aa = ""
    if request.method == 'POST':
        email = request.form['email']
        
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("SELECT email, password, name FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        if user and user[0] in signupOwnerList:
            aa = "youCanViewSignup"
            
            return redirect('/signup')
        else:
            
            return render_template('verification.html', error='You dont have access to signup')
    
    return render_template('verification.html')

# SQLite database initialization
def create_table1():
    conn = sqlite3.connect('mydatabase1.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, message TEXT)")
    conn.commit()
    conn.close()

def insert_user1(name, email, message):
    conn = sqlite3.connect('mydatabase1.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()

def get_users1():
    conn = sqlite3.connect('mydatabase1.db')
    c = conn.cursor()
    c.execute("SELECT name, email, message FROM users")
    data = c.fetchall()
    conn.close()
    return data

@app.route('/contactme', methods=['GET', 'POST'])
def contactme():
    global aa
    if request.method == 'POST':
        name = request.form['nameCD']
        email = request.form['emailCD']
        message = request.form['messageCD']
        
        insert_user1(name, email, message)
        flash('Sent successfully!', 'success')
        return redirect('/profile')
    

    
    
    
'''
route to signout - it will work by removing looged in user's email from the session

'''
@app.route('/signout')
def signout():
    session.pop('email', None)
    return redirect('/')

'''
route to sample.html - user should login to view the sample.html(i.e database) and getting all users details 
from the data base by calling get_users() method and passing users parameter to the sample.html

'''
@app.route('/sample')
def sample():
    global aa
    
    if 'email' in session:
        users = get_users()
        contactMeDetails = get_users1()
        aa = ""
        return render_template('sample.html', users=users, contactMeDetails = contactMeDetails)
    aa = ""
    return redirect('/signin')


'''
route to profile.html - user should login to view the profile.html(i.e portfolio).

'''
@app.route('/profile')
def profile():
    global aa
    
    if 'email' in session:
        
        aa = ""
        return render_template('profile.html')
    
    
    aa = ""
    return redirect('/signin')

'''
route to delete - it will work by removing looged in user's email from the session

'''

@app.route('/delete', methods=['POST'])
def delete():
    
    if request.method == 'POST':
        email = request.json['email']
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE email=?", (email,))
        conn.commit()
        conn.close()
        return 'Deleted'



#running application 

if __name__ == '__main__':
    create_table()
    create_table1()
    app.run(debug=True)
