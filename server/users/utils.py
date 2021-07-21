import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from server import mail


#used to save the profile image in the db and server.
def save_picture(form_picture):
	#it creates a random 8byte name to use to save our picture in the file because if we use the same name of image file that a user uploaded it might cause error if the name of the file is already in the file.
	random_hex = secrets.token_hex(8)

	#in order to save our image in the file in the same extention of the uploaded image than we can use os moduel and use .splitext that splits file name and file extention of user uploaded file and returns both the name of the file and extention of the file. so file name is saved in _ and extenstion in f_ext

	#and form_picture will be the data that is in the upload profile picture of the form.py and filename means the name of the file that we are about to upload doing form_picture.filename will grab the name of the file with extension of picture that we selected and splits name and extension
	_, f_ext = os.path.splitext(form_picture.filename)

	#now here we will save the image file with the new name but the same extension. name will be of 8bytes that out secrets module generated for us and f_ext will be the extension that os splitted.
	picture_fn = random_hex + f_ext

	#here we entered the full path to save the uploaded image in our profile_pic folder which is inside of static folder. using os.path.join will create the full path with the following file name we entered
	picture_path = os.path.join(current_app.root_path,'static/profile_pic', picture_fn)

	#this will resize the image into 125px so that our webpage runs faster. we set the size of 125px. Than i =Image.open(form_picture) will save the picture in the i variable and in the next line we resized the image in i to the size we set in output
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	#now this will completely save the image in the path we mentioned in picture_path
	i.save(picture_path)


	return picture_fn


def send_reset_email(user):

	#this is gona get the token value from models.py
	token = user.get_reset_token()

	#this here will be the message that will be sent to the user where the subject will be 'Password Reset Request' sender will be me and recepients will be the email of the user who want to reset the password 
	msg  = Message('Password Reset Request', sender='adhikaripuspa374@gmail.com', recipients=[user.email])

	#here we do _external=True to get the absolute url rather than relative url. this will give us the full domain and this will be the email body. this will give the full domain of the reset_token.html page with token
	msg.body = f''' To reset your password, visit the following link:
	{url_for('users.reset_token', token=token, _external = True)}

	No changes will be made untill you go to the given link and reset your password.

									Thank You 

	 '''
	mail.send(msg)