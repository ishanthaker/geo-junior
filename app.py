from flask import Flask, render_template, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geo_junior.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Functions for database interactions
@app.before_request
def before_request():
    g.db = db.session

@app.teardown_request
def teardown_request(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.remove()

# Route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_username = request.form.get('username')
        password = request.form.get('password')
        print(entered_username, password)

        # query = text("SELECT * FROM users WHERE username = :username")
        user = User.query.filter_by(username=entered_username, password=password)
        print(user)

        if user:
            # Successful login, redirect to the home page
            global session_username
            session_username = entered_username
            return redirect(url_for('home'))
        else:
            # Incorrect credentials, redirect back to the login page with a message
            return render_template('login.html', message='Incorrect username or password')

    # For GET requests, just render the login page
    return render_template('login.html')

# Route for the home page
@app.route('/home')
def home():
    return render_template('home.html', username=session_username)

# Route for the Quizzes page
@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')

@app.route('/quizGeo')
def quizGeo():
    return render_template('quizGeo.html')

@app.route('/quizLand')
def quizLand():
    return render_template('quizLand.html')

@app.route('/quizCap')
def quizCap():
    return render_template('quizCap.html')

# Route for the Study page
@app.route('/study')
def study():
    return render_template('study.html')

@app.route('/studyGeo')
def studyGeo():
    return render_template('studyGeo.html')

@app.route('/studyLand')
def studyLand():
    return render_template('studyLand.html')

@app.route('/studyCap')
def studyCap():
    return render_template('studyCap.html')

# Route for the Profile page
@app.route('/profile')
def profile():

    return render_template('profile.html', username=session_username)

if __name__ == '__main__':
    app.run(debug=True)
