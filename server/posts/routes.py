from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from server import db
from server.models import Post
from server.posts.forms import PostForm

#its like creating a instance of the app in the __init__.py file
posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
#login required is added because user need to be logged in to post so this decorator will check whether the user is logged in or not
@login_required
def new_post():
	#creating instance for PostForm class of form.py page
	form  = PostForm()

	if form.validate_on_submit():
		post=Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')

#this means if the user wants to go to the post 1 it will be post/1 and if they wants to go to the post 2 it will be post/2 and so on....
@posts.route("/post/<int:post_id>")
def post(post_id):
	#if we want to fetch something by the id than we need to do .get(id of that thing). this means if the post of that id exists than get that post otherwise return 404 means it doesn't exists.
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


#this will use the post_id of the post to update and login is required to update the posts.
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):

	post = Post.query.get_or_404(post_id)
	#if the current user who is using the post isn't the author of the post than the server will abort the task with 403 error.
	if post.author != current_user:
		abort(403)

	#this will create the instance of PostForm form form.py because update form and new form will have same elements inside of but exececpt the legend and Post button
	form = PostForm()

	#it will check if the form validates when we submmited and if True than the following code is executed.
	if form.validate_on_submit():
		#the title of the post field will now be the title of the form field
		post.title = form.title.data

		#the updated contenet in post will now be the actual content of the form
		post.content = form.content.data

		#Every time we don't need to add session because here we aren't creating a new post but changining the current post
		db.session.commit()

		flash('Your post has been updated', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		#Below two codes are used so that when we click on update than the title field and content field will have been filled with the post that we clicked on
		#this will take the title of the post that we have clicked on and pass it to the form.title.data (means title of the post will already be on the form title field) variable
		#(Jun title hamiley click gareyko post mah xa ho tye title chai form ko data ko rup mah display hunnxa ra content ko lagi pani tyahi nai ho)
		form.title.data = post.title

		#this will also do as above but here it takes content
		form.content.data = post.content

		#here the legend we use and created {{ legend }} in the create_post will keep the 'Update_Post' in the legend and if this isn't being executed than will keep another legend from some other function.
	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash('Your post has been successfully deleted', 'success')
	return redirect(url_for('main.home'))