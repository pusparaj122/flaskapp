import os

# this will allow us to have configuration in one file.
class Config:
	# those os.environ.get() means value of these are stored in the enviroment variable with the respective names. these are done to hide sensative data form the source code
	SECRET_KEY = os.environ.get('s_key')
	SQLALCHEMY_DATABASE_URI = os.environ.get('uri')

	# these fonfiguration are made to send mail with token for reset password to the user email address
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = '587'
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('DB_USER')
	MAIL_PASSWORD = os.environ.get('DB_PASS')

# app.config.update(
# 		MAIL_SERVER='smtp.gmail.com',
# 		MAIL_PORT='587',
# 		#MAIL_USE_TSL=True,
# 		MAIL_USE_TLS=True,
# 		MAIL_USERNAME=os.environ.get('DB_USER'),
# 		MAIL_PASSWORD=os.environ.get('DB_PASS')
# 	)