from flask import Blueprint
from pip import main

from .extensions import mongo


main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert_one({'name' : 'Anthony'})
    return '<h1>Added a User!</h1>'