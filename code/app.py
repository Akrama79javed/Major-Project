from flask import Flask, render_template,redirect,request, flash, session
from database import User, add_to_db, open_db, File, open_db, Job
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'thisissupersecretkeyfornoone'

app.config['UPLOAD_PATH'] = 'static/uploads'

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
        if email and password:
            db = open_db()
            user = db.query(User).filter(email=email)
            if user is not None and user.password == password:
                session['isauth'] = True
                session['id'] = user.id
                session['email'] = user.email
                session['username'] = user.username
                flash('You are logged In', 'success')
                
                return redirect('/')
            else:
                flash('credentials do not match', 'danger')
        else:
            flash('email and password cant be empty','danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('isauth'):   
        session.clear()
    return redirect('/login')

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
        filetype = request.form.get('formtype')
        if filetype == 'pdf':
            pdffile = request.form.get('pdffile')
            filename = secure_filename(pdffile.filename)
            if filename != '':
                if os.path.exists(app.config('UPLOAD_PATH')):
                    os.makedirs(app.config['UPLOAD_PATH'])
                path = os.path.join(app.config['UPLOAD_PATH'],filename)     # make os compatible path string
                try:
                    pdffile.save(path)
                    add_to_db(File(path=path, user_id=session.get('id', 1)))
                    return redirect('/resume/add')
                except Exception as e:
                    print(e)
                    return redirect('/resume/add')
        elif filetype == 'doc':
            wordfile = request.form.get('docfile')
            print("word file =>", wordfile)
        # logic
    return render_template('addresume.html')

@app.route('/job/add', methods=['GET', 'POST'])
def jobadd():
    if request.method == 'POST':
        jobTitle = request.form.get('jobTitle')
        jobDescription= request.form.get('jobDescription')
        jobLocation = request.form.get('jobLocation')
        jobType = request.form.get('jobType')
        print("jobTitle =>", jobTitle)
        print("jobDescription =>", jobDescription)
        print("jobLocation  =>", jobLocation )
        print("jobType =>", jobType)
        # logic
        if len(jobTitle) == 0 or len(jobDescription) == 0 or len(jobLocation) == 0 or len(jobType) == 0:
            flash("All fields are required", 'danger')
            return redirect('/register') # reload the page
        job = Job(job_title=jobTitle, job_description=jobDescription, job_location=jobLocation, job_type=jobType)
        add_to_db(job)
        flash('job aded', 'success')
        return redirect('/job/list')
    return render_template('addjob.html')

@app.route('/job/list')
def job_list():
    db = open_db()
    jobs = db.query(Job).all()
    return render_template('joblist.html', jobs=jobs)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 

 