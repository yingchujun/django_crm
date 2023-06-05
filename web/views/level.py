from django.shortcuts import render,redirect
from web import models
from django import forms
from django.urls import reverse

class LevelModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)  # 初始化父类方法
		for field in self.fields.values():
			field.widget.attrs = {'class': 'form-control'}
	class Meta:
		model = models.Level
		fields = ['title', 'percent']

def level_list(request):
	query = models.Level.objects.filter(active='1')
	return render(request, 'level_list.html', {'query': query})


def level_add(request):

	if request.method == "GET":
		form = LevelModelForm()
		return render(request, 'form.html', {'form': form})
	form = LevelModelForm(data=request.POST)
	if not form.is_valid():
		return render(request, 'form.html', {'form': form})

	form.save()

	return redirect(reverse('level_list'))

def level_edit(request, pk):
	level_obj = models.Level.objects.filter(id=pk, active=1).first()

	if request.method == 'GET':
		form = LevelModelForm(instance=level_obj)
		return render(request, 'form.html', {'form': form})

	#   获取数据 校验 更新
	form = LevelModelForm(data=request.POST, instance=level_obj)
	if not form.is_valid():
		 return render(request, 'form.html', {'form': form})

	form.save()
	return redirect(reverse('level_list'))

def level_delete(request, pk):
	# models.Level.objects.filter(id=pk).update(active=0)
	# 方法一：判断是否还有客户有与该级别关联 有不删 没有就直接删除
	exists = models.Customer.objects.filter(level_id=pk).exists()
	if not exists:
		models.Level.objects.filter(id=pk).update(active=0)

	# 方法二： 将相关连的客户等级设置为null
	# models.Customer.objects.filter(level_id=px).update(level=None)

	return redirect(reverse('level_list'))