from flask import Blueprint, render_template
from flask_login import login_required, current_user
import requests
import os



user = Blueprint('user', __name__, template_folder='templates')

@user.route('/')
def index():

    if current_user.is_authenticated:  # Check if the user is logged in
        data = requests.get("http://127.0.0.1:5000/api/user/" + str(current_user.id)).json()
        data2 = requests.get("http://127.0.0.1:5000/api/user").json()
        data3 = requests.get("http://127.0.0.1:5000/api/timeline/" + str(current_user.id)).json()
        return render_template('indexlogged.html', name=current_user.name, id=current_user.id, profilepicture=data['profilepicture'], users=data2, timeline=data3)

    else:
        return render_template('index.html')
    
    
@user.route('/explore')
@login_required
def explore():
    data = requests.get("http://127.0.0.1:5000/api/user/" + str(current_user.id)).json()
    data2 = requests.get("http://127.0.0.1:5000/api/user").json()
    data3 = requests.get("http://127.0.0.1:5000/api/explore/" + str(current_user.id)).json()
    return render_template('explore.html', name=current_user.name, id=current_user.id, profilepicture=data['profilepicture'], users=data2, timeline=data3)




# @user.route('/profile')
# @login_required
# def profile():

#     data = requests.get("http://127.0.0.1:5000/api/profile/" + str(current_user.name)).json()
#     data3 = requests.get("http://127.0.0.1:5000/api/profileposts/" + str(current_user.id)).json()
#     return render_template('profile.html', user_id=current_user.id, profile_data = data, posts = data3)


@user.route('/profile/<string:user_name>')
@login_required
def profile_id(user_name):
    data = requests.get("http://127.0.0.1:5000/api/profile/" + str(user_name)).json()

    data2 = requests.get("http://127.0.0.1:5000/api/following/" + str(current_user.id) + "/" + str(data['user_id'])).json()
    data3 = requests.get("http://127.0.0.1:5000/api/profileposts/" + str(data['user_id'])).json()
    return render_template('profile.html', user_id=current_user.id,profile_data = data, following = data2, posts = data3)




@user.route('/createpost')
@login_required
def createpost():
    data = requests.get("http://127.0.0.1:5000/api/user/" + str(current_user.id)).json()
    return render_template('createpost.html', name=current_user.name, user_id=current_user.id, profilepicture=data['profilepicture'])

@user.route('/editprofile')
@login_required
def editprofile():
    data = requests.get("http://127.0.0.1:5000/api/profile/" + str(current_user.name)).json()
    return render_template('editprofile.html', name=current_user.name, user_id=current_user.id, profile = data)

@user.route('/post/<int:post_id>')
@login_required
def post(post_id):

    

        data = requests.get("http://127.0.0.1:5000/api/user/" + str(current_user.id)).json()
        data2 = requests.get("http://127.0.0.1:5000/api/user").json()
        data3 = requests.get("http://127.0.0.1:5000/api/timeline/" + str(current_user.id)).json()
        data4 = requests.get("http://127.0.0.1:5000/api/post/" + str(post_id) + "/" + str(current_user.id)).json()
        return render_template('post.html', name=current_user.name, id=current_user.id, profilepicture=data['profilepicture'], users=data2, timeline=data4)



@user.route('/search/', defaults={'keyword': None})
@user.route('/search/<string:keyword>')
@login_required
def search(keyword):
    data = requests.get("http://127.0.0.1:5000/api/user/" + str(current_user.id)).json()
    data2 = requests.get("http://127.0.0.1:5000/api/user").json()
    url = "http://127.0.0.1:5000/api/search/" + str(current_user.id)
    if keyword:
        url += "/"
        url += str(keyword)
    data3 = requests.get(url).json()

    return render_template('search.html', name=current_user.name, id=current_user.id, profilepicture=data['profilepicture'], users=data2, query=data3, keyword=keyword)