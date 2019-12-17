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

app = Flask(__name__, static_url_path='/static')


account_sid = 'AC1e5cce5f981923f34e5d2309d9a70cbb' #os.environ["account_sid"]
auth_token = '6ff543682f94c8de705d04f5f3c1768e' #os.environ['auth_token']
client = Client(account_sid, auth_token)

stripe_keys = {
  'secret_key': 'sk_test_S1UKtrSKbTVMv7YzQpch6RBc007RPTTUgW',
  'publishable_key': 'pk_test_LqQaKSR0V30253rAvgA8Bcd300FMsyQ5d2'
}


stripe.api_key = stripe_keys['secret_key']


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html', key=stripe_keys['publishable_key'])


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict',methods=['POST'])
def predict():
	df= pd.read_csv("spam.csv", encoding="latin-1")
	df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
	# Features and Labels
	df['label'] = df['class'].map({'ham': 0, 'spam': 1})
	X = df['message']
	y = df['label']
	
	# Extract Feature With CountVectorizer
	cv = CountVectorizer()
	X = cv.fit_transform(X) # Fit the Data
    # training data
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
	#Naive Bayes Classifier
	from sklearn.naive_bayes import MultinomialNB

	clf = MultinomialNB()
	clf.fit(X_train,y_train)
	clf.score(X_test,y_test)


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
	app.run(debug=True)