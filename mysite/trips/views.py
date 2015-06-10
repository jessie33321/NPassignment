from django.shortcuts import render
from django.core.context_processors import csrf
# Create your views here.
from datetime import datetime
from trips.models import info,account
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import template
from django.contrib import auth

username = ''
	
def login(request):
	c = {}
	c.update(csrf(request))
	global username
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	
	if account.objects.filter(name=username).exists():
		user = account.objects.get(name=username)
		
		if user.password == password:
			if username=='superuser':
				return HttpResponseRedirect('/superuser/')
			else:
				return HttpResponseRedirect('/home/')
		else:
			return render_to_response('login2.html',c)
			
	else:
		username=''
		return render_to_response('login2.html',c)
		
def superuser(request):
	list = info.objects.all()
	if request.POST.get('dname', ''):
		c = {}
		c.update(csrf(request))
		dname = request.POST.get('dname', '')
		user = account.objects.get(name=dname)
		user.delete()
		inf = info.objects.get(name=dname)
		inf.delete()
		return render(request,'superuser.html',{'list': list})
	elif request.POST.get('name', '') and request.POST.get('password', '') and request.POST.get('gender', '') and request.POST.get('height', '') and request.POST.get('weight', ''):
		c = {}
		c.update(csrf(request))
		name = request.POST.get('name', '')
		password = request.POST.get('password', '')
		gender = request.POST.get('gender', '')
		height = request.POST.get('height', '')
		weight = request.POST.get('weight', '')
		acc_obj = account.objects.create(name=name,password=password)
		acc_obj.save()
		info_obj = info.objects.create(name=name,gender=gender,height=height,weight=weight,time=datetime.now())
		info_obj.save()
		return render(request,'superuser.html',{'list': list})		
	else:
		return render(request,'superuser.html',{'list': list})
	
def home(request):
	list  = info.objects.get(name=username)	
	return render(request,'home.html',{'list': list})
	
def modify(request):
	c = {}
	c.update(csrf(request))
	gender = request.POST.get('gender', '')
	height = request.POST.get('height', '')
	weight = request.POST.get('weight', '')
	
	if gender!='':
		info_obj = info.objects.get(name=username)
		info_obj.gender = gender
		info_obj.height = height
		info_obj.weight = weight
		info_obj.time = datetime.now()
		info_obj.save()
		return HttpResponseRedirect('/home/')
	else:
		return render(request,'modify.html')
		
def register(request):
	c = {}
	c.update(csrf(request))
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	gender = request.POST.get('gender', '')
	height = request.POST.get('height', '')
	weight = request.POST.get('weight', '')
	
	if username!='' and password!='' and gender!='' and height!='' and weight!='':
		acc_obj = account.objects.create(name=username,password=password)
		acc_obj.save()
		info_obj = info.objects.create(name=username,gender=gender,height=height,weight=weight,time=datetime.now())
		info_obj.save()
		return HttpResponseRedirect('/login2/')
	else:
		return render(request,'register.html')