from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abcd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(255))
    branch = db.Column(db.VARCHAR(255))

class Users(db.Model):
    username = db.Column(db.VARCHAR(255), primary_key=True)
    password = db.Column(db.VARCHAR(255))

@app.route('/')
def home():
    return "Home route"

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login_post', methods=['post'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user_from_db = Users.query.filter_by(username=username).first()
    if user_from_db is not None:
        if check_password_hash(user_from_db.password, password):
            return "User authenticated successfully"
        else:
            return "Invalid credentials"
    else:
        return "User doesnot exist"


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register_post', methods=['post'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)
    user = Users(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return "User registered successfully"



@app.route('/index')
def index():
    name = "Something"
    return render_template('index.html', abcd = name)

@app.route('/form_input', methods=['post'])
def form():
    user_name = request.form.get('name')
    user_branch = request.form.get('branch')
    student = Students(name=user_name, branch=user_branch)
    db.session.add(student)
    db.session.commit()
    return "Data entry done"

if __name__ == '__main__':
    app.run(debug=True)

# result = db.engine.execute("select * from students")
# result.fetchall()

# http://bit.ly/fbdevcinvite_new