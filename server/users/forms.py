from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from server.models import User

class RegistrationFrom(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20) ])
	email = StringField('Emali', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	#here equlato is used validate that the password varialble above and confirm_password must have same data.
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	#used to validate wheather the username and email address used for registration is already taken or not. If not it registers your if yes than it will show the error message used from wtfroms

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('Username Already Taken')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Email Already Taken')


class Login(FlaskForm):
	email = StringField('Emali', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20) ])
	email = StringField('Emali', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	#used to validate wheather the username and email address used for registration is already taken or not. If not it registers your if yes than it will show the error message used from wtfroms

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('Username Already Taken')

	#it validate wheather the passed email address is used or not if its used than it will pass error message if not than the email will be updated
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('Email Already Taken')


#now here we will create a form which user will use to reset their password.
class RequestResetForm(FlaskForm):

	#we will ask the user to write the email of their account
	email  = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Get Code')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Sorry, email does not exists in the database')

class ResetPasswordFrom(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset')