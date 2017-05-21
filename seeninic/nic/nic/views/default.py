from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..models import login
from ..models import newsfeed
from sqlalchemy import desc
import datetime
import time
import hashlib
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )
user = ''
@view_config(route_name='home', renderer='../templates/p/home.pt')
def home(request):
    return{}
@view_config(route_name='signup', renderer='../templates/p/signup.pt')
def signup(request):
	return{}
@view_config(route_name='signup1')
def signup1(request):
	global user
	user=request.params['username']
	pwd=request.params['password']
	hash_obj = hashlib.md5(pwd.encode())	
	m=hash_obj.hexdigest()
	obj=request.dbsession.query(login).filter(login.username==user).all()
	length=len(obj)
	if length:
		return render_to_response('../templates/p/userocc.pt',{'message':'username is occupied'},request=request)
	else:
		obj=login(username=user,password=m)
		request.dbsession.add(obj)
		return render_to_response('../templates/p/signup1.pt',{'message':'Registered succesfully!!'},request=request)
@view_config(route_name='signupf', renderer='../templates/p/login1.pt')
def signupf(request):
	global user
	return {'name':user, 'message':'logged in'}

@view_config(route_name='login1')
def login1(request):
	global user
	user=request.params['username']
	pwd=request.params['password']
	hash_obj = hashlib.md5(pwd.encode())	
	m=hash_obj.hexdigest()
	obj=request.dbsession.query(login).filter(login.username==user,login.password==m).first()
	if obj is None:
		return render_to_response('../templates/p/den.pt',{'message':'Access denied!!!Incorrect username or password'},request=request)
	else:
		return render_to_response('../templates/p/login1.pt',{'message':'logged in','name':user},request=request)
@view_config(route_name='update', renderer='../templates/p/update.pt')
def update(request):
 	return {'name':user}

@view_config(route_name='update1')
def update1(request):
	#user=request.params['username']
	#print("#@!$@#%$@#"+user)
	ab=request.params['about']
	cont = request.params['content']
	tdy = datetime.date.today()
	localtime = time.asctime(time.localtime(time.time()))
	obj=newsfeed(username=user,about=ab,content=cont,submitted_date=tdy,submitted_time=localtime)
	request.dbsession.add(obj)
	return render_to_response('../templates/p/update.pt',{'message':'updated succesfully!!','name':user},request=request)

@view_config(route_name='tomenu', renderer='../templates/p/login1.pt')
def tomenu(request):
	global user
	return {'name':user, 'message':'logged in'}

@view_config(route_name='news', renderer='../templates/p/news.pt')
def news(request):
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}
