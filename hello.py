#coding=utf-8
from flask import Flask
from flask import request
app=Flask(__name__)
@app.route('/')
def index():
	user_agent=request.headers.get('User-Agent')
	return "<p>Your browser is %s"%user_agent
@app.route("/user/<name>")
def user(name):
	return "<h1>Hello,%s!"%name
if __name__=='__main__':
	app.run(debug=True)
