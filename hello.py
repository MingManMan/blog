#coding=utf-8
from flask import Flask,render_template
from flask import request,redirect,abort,session,redirect,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name=StringField("What is your name?",validators=[Required()])
	submit=SubmitField(u'提交')

app=Flask(__name__)
bootstrap=Bootstrap(app)
moment=Moment(app)
manager=Manager(app)
app.config.from_object('config')
@app.route('/',methods=['GET','POST'])
def index():
	name=None
	form=NameForm()
	if form.validate_on_submit():
		old_name=session.get('name')
		if old_name is not None and old_name!=form.name.data:
			flash('Look like you have changed your name!')
		session['name']=form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'))


if __name__=='__main__':
	manager.run()