<h1 align="center">Bot Detector</h1>
<p>
  <a href="https://github.com/Andre-Williams22/bot_detector/blob/master/README.md" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/Andre-Williams22/bot_detector/graphs/traffic" target="_blank">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  </a>
</p>



![Bot Site](static/img/bot-screen.png)

## Authors

* Andre Williams 
* Github: [@Andre-Williams22](https:/Andre-Williams22/)
* LinkedIn: [@andrewilliams22](https://www.linkedin.com/in/andrewilliams22/)

## Purpose

The Bot Detector uses machine learning to identify if a DM or email on a social media platform is from a human or bot scraping the internet. The Bot Detector saves users from interacting with bots rather than humans. Once the user pays for the service they will have unlimited access to the bot detector and can essentially copy and paste the messages they want detected onto the platform.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
If you haven't already installed pip3 for Python3
```
sudo apt install python3-pip
```
Install flask and requests
```
pip3 install flask
pip3 install requests
pip3 install sqlalchemy
pip3 install stripe
pip3 install flask_login
```

### Installing

1. Clone the respository
```
git clone git@github.com:Andre-Williams22/bot_detector.git
```
2. Make sure in the correct directory

3. Enter the development environment
```
export FLASK_ENV=development 
```
4. Open your terminal and run flask
```
flask run
```
You should see something similar to the output below:
```
* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
* Debug mode: off
* Running on (Your Localhost IP) (Press CTRL+C to quit)
```

## Built With

* [Flask](https://palletsprojects.com/p/flask/) - Lightweight web application framework
* [Jinja](https://palletsprojects.com/p/jinja/) - Template engine for python
* [Stripe API](https://tenor.com/gifapi) - API for payments 
* [Bootstrap](https://getbootstrap.com/) - For styling
* [SQLAlchemy](https://docs.sqlalchemy.org/en/13/dialects/sqlite.html) - Database for user registration and message data
* [Flask_Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) - Used for styling on multiple pages

## 📝 License

Copyright © 2020 [Andre Williams](https://github.com/Andre-Williams22).<br />
This project is [MIT](https://github.com/Andre-Williams22/blob/master/LICENSE) licensed.




