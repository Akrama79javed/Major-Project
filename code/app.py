from flask import Flask, render_template,redirect,request, flash, session
from database import User, add_to_db, open_db

app = Flask(__name__)
app.secret_key = 'thisissupersecretkeyfornoone'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Email =>", email)
        print("Password =>", password)
        # logic
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(username, email, password, cpassword)
        # logic
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
            flash("All fields are required", 'danger')
            return redirect('/register') # reload the page
        user = User(username=username, email=email, password=password)
        add_to_db(user)
    return render_template('register.html')

@app.route('/resume/add', methods=['GET', 'POST'])
def resumeadd():
    if request.method == 'POST':
        filetype = request.form.get('filetype')
        if filetype == 'pdf':
            pdffile = request.form.get('pdffile')
            print("pdf file =>", pdffile)
        elif filetype == 'doc':
            wordfile = request.form.get('docfile')
            print("word file =>", wordfile)
        # logic
    return render_template('addresume.html')

@app.route('/job/add', methods=['GET', 'POST'])
def jobadd():
    if request.method == 'POST':
        addjob = request.form.get('add job')
        jobdiscription = request.form.get('job discription')
        print("add job =>", addjob)
        print("job discripttion =>", jobdiscription)
        # logic
    return render_template('addjob.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 

 