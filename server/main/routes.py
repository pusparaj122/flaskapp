from flask import render_template, request, Blueprint
from server.models import Post

#its like creating a instance of the app in the __init__.py file
main = Blueprint('main', __name__)


#application things lies here

@main.route("/")
@main.route("/home")
def home():

	#it is used to get the post of page 1 where per_page will be 5. doing pagination we can add limited number of post for users to see in the home page and we can use next and previous buttons to get other post request.args.get('page', 1, type=int) this will get the first page and pass it to page variable. and the next next line in post variable we will pageinate the taken page into only 5 post perpage

	#this .get methods gets the dict of page key word and page of 1
	page = request.args.get('page', 1, type=int)

	# now this below code will search the Posts in the database order in the descending order of posted date and paginate the page by per_page of 5 posts. this is how we do sort in sqlalchemy

	#(muni ko code mah hami database mah post search garera teslai recent data ko post lai maathi rakheyra order garea and teslai per page mah 5 ota post rakheyra paginate garera teslai posts varialble mah pass gareyko xa)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page=5)
	return render_template('home.html', posts=posts, title='home')

@main.route('/about')
def about():
	return render_template('about.html')
