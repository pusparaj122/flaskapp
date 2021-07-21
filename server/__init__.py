from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# this helps us to send mail through our flask server
from flask_mail import Mail
from server.config import Config



# we dont move these extension to create_app because we want these outside of the function but we still want to initialize these extension inside of the function.
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'



#app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True

#this means we have kept our username i.e email address in the DB_USER name in enviroment variable of the computer
#path for enviroment variable(controlpanel-->system-->Advance System Setting-->Enviroment Variable-->New-->(variable name is what will be the name of the element you want to store in my case in DB_USER variable name I stored my email address and in DB_PASS I saved password of the email address))
#app.config['MAIL_USERNAME'] = os.environ.get('DB_USER')
#app.config['MAIL_PASSWORD'] = os.environ.get('DB_PASS')

#now we will initialize the mail

mail=Mail()


"""
app.config.update(
MAIL_SERVER='smtp.gmail.com',
MAIL_PORT='587',
MAIL_USE_TLS=True,
MAIL_USERNAME=os.environ.get('EMAIL_USER'),
MAIL_PASSWORD=os.environ.get('EMAIL_PASS')
)

"""
# here we are creating a function to move the creation of our app in this function so that we can create an instance of our app with different configuration.
# this takes an argument for what   configuration object we want to give to our app. so we set it to config class that we created recently in config.py
def create_app(config_class = Config):
	# now we need everthing that creates app except extentions
	app=Flask(__name__)
	# this means value here are instance of Config class in config.py
	app.config.from_object(Config)	

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	#here this import users which is a variable and a instance of blueprint class in users-->routes file.(users=Blueprint('users', __name__)) and same for all of the other imports.
	from server.users.routes import users
	from server.posts.routes import posts
	from server.main.routes import main
	from server.errors.handlers import errors

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app