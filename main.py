__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError, redirect
import interface
import users
import database
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()

db = database.COMP249Db(True)
db.create_tables()
db.fixed_data()


@application.route('/')
def index():
    info = interface.post_list(db)
    return template('index', data=info)


@application.post('/newpost')
def handler():
    post_content = request.forms.get("post")
    user = request.forms.get("username")
    interface.post_add(db, user, post_content)
    redirect('/')


@application.route('/users/<user>')
def user_page(user):
    tpl = '{{posts}}'

    info = {
        'posts': interface.post_list(db, user)
    }

    return template(tpl, info)


@application.get('/mentions/<user>')
def user_mentions(user):
    tpl = '{{posts}}'

    info = {
        'posts': interface.post_list_mentions(db, user)
    }

    return template(tpl, info)


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    application.run(debug=True, port=8010)