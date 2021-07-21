from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from server import db, bcrypt
from server.models import User, Post
from server.users.forms import RegistrationFrom, Login, UpdateAccountForm, RequestResetForm, ResetPasswordFrom
from server.users.utils import save_picture, send_reset_email

#its like creating a instance of the app in the __init__.py file
users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():

	#this means if the user is already logged in but clicks in register link in the page than redirect to the homepage. current_user means the current user that is logged in and is_authenticated checks whether the current_user is authenticated or not. if yes returns True if not returns false. current_user is imported from flask which takes logged in user.
	
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	#creating instance of RegistrationForm from forms.py 
	form = RegistrationFrom()

	#if everything that a user inputs in registsration from is as per our validation than this executes
	if form.validate_on_submit():

		#it will save our hash password rather than normal string
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		#it gets all of the data form the username, email field and password form hashed_password
		user = User(username = form.username.data, email=form.email.data, password=hashed_password)

		#it adds user in the session and ready to add them in the database
		db.session.add(user)

		#this now adds all the session users into the database.
		db.session.commit()

		#now this will flash the below message and redirect us to login page to login with the made account
		flash(f'Your Account Has been Created Login In With Your Account Please', 'success')
		return redirect(url_for('users.login'))

	#if data entered by the user aren't as per the validation than again the register.html open
	return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET','POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	#here we created a instance for Login that is in forms.py file
	form=Login()

	#if all the validators meets its requirements in forms.py Login class Then the below statement executes
	if form.validate_on_submit():

		#This this will filter the db with email that we entered in email field of login page and get the first email if there is any otherwise it returns none
		user = User.query.filter_by(email=form.email.data).first()

		#if there is email that we used for login than user saves the first of them and it also checks whether the hashed password of the password entered by the users in the password field of login page matches the password of that email address if email is there and if password matches than the below statement executes.
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			#login_user is imported form flask_login and it will login the user means the email and takes another parameter that is remember which will be the data that we gave to form.remember_me in login page. and redirects us to the home page.
			login_user(user, remember=form.remember_me.data)

			#it stores the next url to be logged after the login is done
			next_page=request.args.get('next')

			#this returns the next_page if next_page doesn't return none. Means if the user tries to access the account page without login than it redirects us to the login page with the next page being account.html which is saved in next_page variable and if the user logs in without being redirected from account than the above variable returns None and below's function will redirect us directly to the home.html page.
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login Unsuccessful', 'danger')

	return render_template('login.html', title='Login', form=form)

#this is a imported function as like login from flask_login its pre built function used for users to help in logging out of their account. using logout_user() logs us out from the current_user
@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


#this route is imported from login_manager in __init__.py. It displays a messege of login required to access the account page and redirects us to the login page.
@users.route('/account', methods=["GET", 'POST'])
@login_required
def account():
	form = UpdateAccountForm()

	#when the user submits the form and its validated than run the following statemets where username changes toe the username that users posted in the form and same for email and its gonna flash us a message and redirect us to account page.
	if form.validate_on_submit():

		#if user has inserted something in the uploading profile picture section in the form than the following code will be executed.
		if form.picture.data:

			#this will get the file name of the picture that we selected from the above save_picture function
			picture_file = save_picture(form.picture.data)

			#now this will change the current image that we have into the picture that we had selected
			current_user.image_file  = picture_file

		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your Account Has Been Updated', 'success')
		return redirect(url_for('users.account'))

	#This will take care of getting our username and email already in the form fill section to change
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	#it takes the image inside of static folder with the name of profile_pics and concatinate it with the curretn users's image file that we stored previously as default.jpg in model.py's image file
	image_file=url_for('static', filename='profile_pic/'+ current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


#this route will be executed to show all the post of particular username that we clicked on like if we click puspa_25p username than we can see all the post posted by puspa_25p. for this the route will be user/username, username being the name of the user that we clicked on. (/user/puspa_25p)
@users.route('/user/<string:username>')
def user_posts(username):
	page =  request.args.get('page', 1, type=int)

	# this will filter the user by the username we clicked on for now let it be puspa_25p. this will search for this username in the database and get the first user if it exists but if it doesn't than it will display 404 error.
	user = User.query.filter_by(username=username). first_or_404()

	#Now we will search the all the posts who have the author of the user retrived by above user variable and sort it by recent date's post first and than goes on and paginate by per_page of 5 posts
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

	#now this will take us to the user_posts.html template with the posts of posts retrived from the database of the user we clicked to see and pass the user being the user we searched for above in the same function
	return render_template('user_posts.html', posts=posts, user=user)


#this route will just get the email for resetting the password and authenticate the user if the email exists in the datebase or not if yes than we can continue with reset password and if not than we will display a flashed message
#simply here they will request to reset their password
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():

	#this means if the user is already logged in and wants to reset the password than we won't allow them to do so means the user must be logged out of the page to get their password reset.
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

		#creating instance of RequestResetForm that we have in forms.py
	form = RequestResetForm()

	#this here will 1st run the validation process for the field in reset_request and if its validated than it will filter the database on the basis of email passed in reset_request.html and pass the user and data its data to variable user.
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()

		#this here is calling the above send_reset_email function
		send_reset_email(user)
		flash('Check Your Email','info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form = form)

#here they will enter the token that they received through email and verify that and if it is verified than they can enter a new password if not than not.
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	#here we pass what ever is return by the verify_reset_token in models.py User class and pass token as a parameter to verify.
	user = User.verify_reset_token(token)

	# if above user variable gets None form the Instance that we created than the token that user passed might be either invalid or might have been experied. so we flashed a message with bootstrap category of warning being that flash message in a yellow box.
	if user is None:
		flash('That is an invalid or it might have been experied', 'warning')
		return redirect(url_for('users.reset_request'))

	form = ResetPasswordFrom()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been changed successfully', 'success')
		return redirect(url_for('users.login'))

	return render_template('reset_token.html', title='Reset Password', form=form)
