#coding=utf-8
from flask import Flask,render_template
from flask import request,redirect,abort
from flask import request,redirect,abort,session,redirect,url_for
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message

basedir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)

app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True



mail=Mail(app)
db=SQLAlchemy(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))

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

def send_email(to,subject,template,**kwargs):
	msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
	msg.body=render_template(template+'.txt',**kwargs)
	msg.html=render_template(template+'.html',**kwargs)
	mail.send(msg)

@app.route('/',methods=['GET','POST'])
def index():
	form=NameForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.name.data).first()
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			session['known']=False
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user')
		else:
			session['known']=True
		session['name']=form.name.data
		form.name.data=''
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))



if __name__=='__main__':
	manager.run()