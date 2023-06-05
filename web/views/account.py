from django.shortcuts import render, redirect
from web import models
from utils.encrypt import md5
from django import forms
from django.core.exceptions import ValidationError
from deal_crm.settings import LOGIN_HOME

class LoginForm(forms.Form):
	role = forms.ChoiceField(
		label='角色',choices=(('1', '管理员'), ('2', '用户')), required=True, widget=forms.Select(attrs={'class':"form-control"})
	)
	username = forms.CharField(
		 label='用户名',required=True, widget=forms.TextInput(attrs={'class':"form-control" ,'placeholder':"用户名"})
	)
	password = forms.CharField(
		 label='密码',required=True, widget=forms.PasswordInput(attrs={'class':"form-control" ,'placeholder':"密码"}, render_value=True)
	)

	def clean_username(self):
		username = self.cleaned_data['username']
		if len(username) < 3 :
			raise ValidationError('用户名错误')
		return username

def login(request):

	if request.method == 'GET':
		form = LoginForm()
		return render(request, 'login_list.html', {'form': form})

	if request.method == 'POST':
		# 1. 获取校验数据
		form = LoginForm(data=request.POST)
		if not form.is_valid():
			return render(request, 'login_list.html', {'form': form})
		print(form.cleaned_data)
		role = form.cleaned_data.get('role')
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		password = md5(password)

		# 2. 去数据库校验数据  role ==1 管理员  ==2 用户
		mapping = {
			'1' : 'ADMIN',
			'2' : 'CUSTOMER'
		}
		if role == '1':
			user_object = models.Administrator.objects.filter(username=username, password=password, active=1).first()
		else:
			user_object = models.Customer.objects.filter(username=username, password=password, active=1).first()

		# 2.1 校验失败
		if not user_object:
			return render(request, 'login_list.html', {'error': '账号或密码错误', 'form': form})

		# 2.2 校验成功 用户信息写入session并进入后台
		print(user_object.username)
		request.session['user_info'] = {'role': mapping[role], 'username': user_object.username, 'id': user_object.id}
		return redirect(LOGIN_HOME)

def sms_login(request):

	return render(request, 'sms_login.html')

def logout(request):
	request.session.clear()
	return render(request, LOGIN_HOME)

def home(request):
	return render(request, 'home.html')