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
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'THISISASECRET'
# connect database to project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/andre22/Documents/Dev/SPD-1.2/bot-detector/database.db'
Bootstrap(app)
db = SQLAlchemy(app) # connects database to app

# creates a class that represents a table in the database for the user table
class User(db.Model): #name of table in SQL database is "User"
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
# .exit

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
  'secret_key': 'sk_test_S1UKtrSKbTVMv7YzQpch6RBc007RPTTUgW',
  'publishable_key': 'pk_test_LqQaKSR0V30253rAvgA8Bcd300FMsyQ5d2'
}


stripe.api_key = stripe_keys['secret_key']


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html', key=stripe_keys['publishable_key'])

# User Authentication Information
@app.route('/login', methods=['Get', 'POST'])
def login():

    form = LoginForm() #instantiates LoginForm class 

    if form.validate_on_submit(): # checks to see if form has been submitted 
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>' #grabs data from input username and password


    return render_template('login.html', form=form)

@app.route('/signup')
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)#instantiates a new user from database
        db.session.add(new_user)
        db.session.commit()
        return '<h1> New user has been created! </h1>'
       # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/about')
def about():
    return render_template('about.html')

# Machine learning model
@app.route('/predict',methods=['POST'])
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
		my_prediction = clf.predict(vect)
	return render_template('predict.html', prediction = my_prediction)

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

    return render_template('charge.html', amounts=amounts)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
