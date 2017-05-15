#coding=utf-8
from flask import Flask,render_template
from flask import request,redirect,abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app=Flask(__name__)
bootstrap=Bootstrap(app)
moment=Moment(app)
manager=Manager(app)

@app.route('/')
def index():
	return render_template('index.html',current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500
	

@app.route('/user/<username>')
def user(username):
	return render_template('user.html',name=username)
if __name__=='__main__':
	manager.run()