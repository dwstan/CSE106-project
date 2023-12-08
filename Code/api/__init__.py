from flask_restful import Api

from api.Resources.Signup import Signup
from api.Resources.Login import Login



def create_api(app):
    api = Api(app)

    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')








    return api