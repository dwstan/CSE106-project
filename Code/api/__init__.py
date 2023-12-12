from flask_restful import Api

from api.Resources.Signup import Signup
from api.Resources.Login import Login
from api.Resources.UserDetail import UserDetail
from api.Resources.User import User
from api.Resources.CreatePost import CreatePost
from api.Resources.ProfileDetail import ProfileDetail
from api.Resources.Follow import Follow
from api.Resources.Following import Following
from api.Resources.ProfilePosts import ProfilePosts
from api.Resources.Timeline import Timeline
from api.Resources.Like import Like
from api.Resources.Comment import Comment
from api.Resources.CommentPost import CommentPost
from api.Resources.Explore import Explore
from api.Resources.PostDetail import PostDetail
from api.Resources.EditProfile import EditProfile
from api.Resources.Search import Search



def create_api(app):
    api = Api(app)

    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(UserDetail, '/api/user/<int:user_id>')
    api.add_resource(User, '/api/user')
    api.add_resource(CreatePost, '/api/createpost')
    api.add_resource(ProfileDetail, '/api/profile/<string:user_name>')
    api.add_resource(Follow, '/api/follow')
    api.add_resource(Following, '/api/following/<int:user_id>/<int:profile_id>')
    api.add_resource(ProfilePosts, '/api/profileposts/<int:profile_id>')
    api.add_resource(Timeline, '/api/timeline/<int:user_id>')
    api.add_resource(Explore, '/api/explore/<int:user_id>')
    api.add_resource(Like, '/api/like', endpoint='like')
    api.add_resource(Like, '/post/api/like', endpoint='like_post')  # Add the new URL here
    
    api.add_resource(Comment, '/api/comment')
    api.add_resource(CommentPost, '/api/comment/post/<int:post_id>')
    api.add_resource(PostDetail, '/api/post/<int:post_id>/<int:user_id>')
    api.add_resource(EditProfile, '/api/editprofile')
    api.add_resource(Search, '/api/search/<int:current_user_id>', '/api/search/<int:current_user_id>/<string:keyword>')


    return api