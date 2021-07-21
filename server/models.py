from server import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

#it will find the logged in user by its id and get the information about that user through that id. it is used while doing login. this decorator must be the same way
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#Database things lies here
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
	password = db.Column(db.String(60), nullable = False)

	#this means our post attribute has the relationship with Post class its similare to add another column to Posts model. what backref allows us to do is when we have a post we can simply use author attribute to get the user who created the post and lazy argument just define when the sqlalchemy loads the data from the database so true means the database will load the data in one go as necessary. This relationship is helpful beacuse we can easily get the all of the post of a user by using post attribute.

	posts = db.relationship('Post', backref='author', lazy=True)

	# this is done for users to reset their password. we imported (from itsdangerous import TimedJSONWebSignatureSerializer as Serializer) and this module will help us to generate a token that expries in the time that we set here it is 1800 seconds means 30minutes. this token will be sent through email and if it varifies than the user can reset their password.
	def get_reset_token(self, expries_sec=1800):

		#it creates a token
		s = Serializer(current_app.config['SECRET_KEY'], expries_sec)

		# here it returns the token that we have created by dumps method with payload of user_id and decode it to string with 'utf-8' other wise it returns bytes. self .id will get the id of current user and pass that to user_id in a dictionary.
		return s.dumps({'user_id': self.id}).decode('utf-8')

	# static method is used to tell python that we aren't passing self in the below function. as we are under Userclass we need to pass self as another parameter but we didn't do that 
	@staticmethod
	def verify_reset_token(token):

		s = Serializer(current_app.config['SECRET_KEY'])

		# we used try and except because we could get some exception while running the above code. so when we try the code if it returns something except None than the return User.query.get(user_id) runs. below code tries to get the user_id from the token and if it failes to get that than the code in except is ran. Otherwise it gets the User who have that user id. Now we create a route
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None 
		return User.query.get(user_id)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title=db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)

	#using the above relation it will get the id of the user who author the post
	#here user means we aren't refrencing the class but the table name and the column name so the above user model automatically will the table name set to lowercase user and post model will have automatically set to lowercase post. We can set our own table name but for now we will leave those

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"