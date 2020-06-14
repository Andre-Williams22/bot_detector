from flask import Flask,render_template,redirect, url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import stripe 
from dotenv import load_dotenv
load_dotenv()
from twilio.rest import Client
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.urls import url_encode
from urllib.parse import urlencode
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
from werkzeug.security import generate_password_hash, check_password_hash # web security that hashes database for login credentials 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'THISISASECRET'
# connect database to project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/andre22/Documents/Dev/SPD-1.2/bot-detector/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app) # connects database to app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# creates a class that represents a table in the database for the user table
class User(UserMixin,db.Model): #name of table in SQL database is "User"
# Do First: go to terminal and create SQLite db called "database.db". type: sqlite3 database.db
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
# 1. type in terminal: python 
# 2. type: from app import db
# 3. type: db.create_all()
# 4. type: exit()
# 5. type: sqlite3 database.db
# 6. type: .tables (to see what you've created in database)

# SQL Database Commands :
# select * from user;
# .tables
# delete from user; (deletes data in table)
# .exit

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Login Form for login page
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')
# Signup Form for signup page
class SignupForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=5, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


stripe_keys = {
  'secret_key': 'sk_test_8xdHGXFzRls1cnqCAGAKU7qR004iPCi3qd',
  'publishable_key': 'pk_test_FBfglBDbfjv103hobURAe1ji00L58GEGQE'
}


stripe.api_key = stripe_keys['secret_key']


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

# User Authentication Information
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm() #instantiates LoginForm class 

    if form.validate_on_submit(): # checks to see if form has been submitted 
        user = User.query.filter_by(username=form.username.data).first()# query database for user to see if passwords match
        if user:
            if check_password_hash(user.password, form.password.data): # check if passwords match in database and form
                login_user(user, remember=form.remember.data) # logs user in before taking them to dashboard
                return redirect(url_for('dashboard')) # takes to dashboard & allows them to see account info and use service
       
        return '<h1>Invalid Username or Password. Please Try Again</h1>' # passwords do not match, so raise error

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>' #grabs data from input username and password
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256') #this generates a hash 80 chars long
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password) #instantiates a new user from database
        db.session.add(new_user)
        db.session.commit()
        return '<h1> New user has been created! </h1>'
       # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user() # logs user out 
    return redirect(url_for('index'))


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256') #this generates a hash 80 chars long
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password) #instantiates a new user from database
        db.session.add(new_user)
        db.session.commit()
        
    return render_template('payment.html', form=form, key=stripe_keys['publishable_key'])

@app.route('/about')
def about():
    return render_template('about.html')

# Machine learning model
@app.route('/predict',methods=['POST'])
@login_required
def predict():
	df= pd.read_csv("bot.csv", encoding="latin-1")
	df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
	# Features and Labels
	df['label'] = df['class'].map({'ham': 0, 'spam': 1})
	X = df['message']
	y = df['label']
	
	# Extract Feature With CountVectorizer
	cv = CountVectorizer() # Count Vectorizer is used to count each word used in an email
	X = cv.fit_transform(X) # Fit the Data
    # training data
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
	#Naive Bayes Classifier
	from sklearn.naive_bayes import MultinomialNB

	classifier = MultinomialNB()
	classifier.fit(X_train,y_train)
	classifier.score(X_test,y_test)


	if request.method == 'POST':
		message = request.form['message']
		data = [message]
		vect = cv.transform(data).toarray()
		my_prediction = classifier.predict(vect)
	return render_template('predict.html', prediction = my_prediction, key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    '''charges the user'''
    # client = Client(account_sid, auth_token)
    # message = client.messages \
    #     .create(
    #         body="Thank you for your purchase. Keep breathing!",
    #         from_='+12162086503',
    #         to='2142846514')
    # print(message.sid)
    # amount in cents
    
    amount = 1000

    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    
    return redirect(url_for('show_message'))


@app.route('/charge/message')
def show_message():
    ''' Shows the charge amount'''
    amounts=1000

    return render_template('charge.html', amounts=amounts, name=current_user.username, key=stripe_keys['publishable_key'])

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
