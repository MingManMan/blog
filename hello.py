#coding=utf-8
from flask import Flask
from flask import request,redirect,abort
from flask_script import Manager
app=Flask(__name__)
manager=Manager(app)

@app.route('/')
def index():
	user_agent=request.headers.get('User-Agent')
	return "<p>Your browser is %s"%user_agent
if __name__=='__main__':
	manager.run()