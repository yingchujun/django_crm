from django.shortcuts import render, HttpResponse,redirect,reverse
from web import models
from django import forms
from django.core.exceptions import ValidationError
from utils.encrypt import md5
from django.utils.safestring import mark_safe

def customer_list(request):

	# 级别被删除了下属客户怎么办
	# 方法一：判断是否还有客户有与该级别关联 有不删 没有就直接删除
	# 方法二： 将相关连的客户等级设置为null

	# 方法三： 不做处理 查询时跨表查询
	# queryset = models.Customer.objects.filter(active=1, level__active=1)

	# 主动跨表连表查询
	queryset = models.Customer.objects.filter(active=1).select_related('level', 'creator')
	current_page = 0
	if request.GET.get('page'):
		current_page = int(request.GET.get('page'))

	page_list = []
	count_page = len(queryset)
	if current_page % 10 != 0:
		count_page = count_page//10 +1
	else:
		count_page = count_page//10
	print(count_page)
	for i in range(1, count_page):
		page_list.append(mark_safe(f'<li><a href="?page={i}">{i}</a></li>'))

	context = {
		'queryset' : queryset[current_page*10:current_page*10+10],
		'page_list' : page_list
	}



	return render(request, 'customer_list.html', context)


class CustomerModelForm(forms.ModelForm):
	confirm_password = forms.CharField(
		label='重复密码',
		widget=forms.PasswordInput
	)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)  # 初始化父类方法
		self.fields['level'].queryset = models.Level.objects.filter(active=1)

		for field in self.fields.values():
			field.widget.attrs = {'class': 'form-control'}

	class Meta:
		model = models.Customer
		fields = ['username', 'password', 'confirm_password', 'mobile', 'level']
		# widgets = {
		# 	'level': forms.RadioSelect
		# }

	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = md5(self.cleaned_data.get('confirm_password'))

		if password != confirm_password:
			raise ValidationError('密码不一致')
		return confirm_password

	def clean_password(self):
		password = self.cleaned_data['password']

		return md5(password)


def customer_add(request):
	if request.method == 'GET':
		form = CustomerModelForm()
		return render(request, 'form.html', {'form': form})

	if request.method == 'POST':
		form = CustomerModelForm(data=request.POST)
		if not form.is_valid():
			return render(request, 'form.html', {'form': form})
		form.instance.creator_id = request.nb_user.id
		form.save()
		return redirect('/customer/list')



class CustomerEditModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)  # 初始化父类方法
		self.fields['level'].queryset = models.Level.objects.filter(active=1)

		for field in self.fields.values():
			field.widget.attrs = {'class': 'form-control'}

	class Meta:
		model = models.Customer
		fields = ['username', 'mobile', 'level']

	def clean_password(self):
		password = self.cleaned_data['password']
		return md5(password)



def customer_edit(request, pk):

	instance = models.Customer.objects.filter(id=pk,active=1).first()

	if request.method == 'GET':
		form = CustomerEditModelForm(instance=instance)
		return render(request, 'form.html', {'form': form})

	form = CustomerEditModelForm(instance=instance, data=request.POST)
	if not form.is_valid():
		return render(request, 'form.html', {'form': form})
	form.save()
	return redirect('/customer/list')

def customer_delete(request, pk):

	models.Customer.objects.filter(id=pk).update(active=0)

	return redirect(reverse('customer_list'))