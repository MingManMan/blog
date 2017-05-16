#coding=utf-8
from flask import Flask,render_template
from flask import request,redirect,abort
from flask import request,redirect,abort,session,redirect,url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import os
from flask_sqlalchemy import SQLAlchemy

basedir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)

app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)


bootstrap=Bootstrap(app)
moment=Moment(app)
manager=Manager(app)

class Role(db.Model):
	"""docstring for Role"""
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users=db.relationship('User',backref='role',lazy='dynamic')
	def __repr__(self):
		return '<Role %r>'%self.name
class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
	def __repr_(self):
		return "<User %r>"%self.username

class NameForm(Form):
	name=StringField("What is your name?",validators=[Required()])
	submit=SubmitField(u'提交')		


@app.route('/',methods=['GET','POST'])
def index():
	form=NameForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.name.data).first()
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			session['known']=False
		else:
			session['known']=True
		session['name']=form.name.data
		form.name.data=''
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))



if __name__=='__main__':
	manager.run()