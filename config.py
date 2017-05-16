import os
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MAIL_SERVER='smtp.163.com'
MAIL_PORT=25
MAIL_USE_TLS=True
MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')

FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
FLASKY_MAIL_SENDER='Flasky Admin<mark_ming@163.com>'
FLASKY_ADMIN='mark_ming@163.com'