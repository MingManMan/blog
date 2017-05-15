#coding=utf-8
from flask import Flask
from flask import request,redirect,abort
app=Flask(__name__)
@app.route('/')
def index():
	user_agent=request.headers.get('User-Agent')
	return "<p>Your browser is %s"%user_agent
@app.route("/user/<name>")
def user(name):
	return "<h1>Hello,%s!"%name
@app.route("/400/")
def my400():
	return '<h1>Bad Request</h1>',400
@app.route("/redir/<url>")
def redir(url):
	return redirect("http://"+url)

@app.route("/get_user/<id>")
def get_user(id):
	abort(404)
if __name__=='__main__':
	app.run(debug=True)