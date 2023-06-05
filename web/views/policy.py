from django.shortcuts import render, HttpResponse, redirect
from web import models
from django import forms

def policy_list(request):

	queryset = models.PricePolicy.objects.all().order_by('count')

	return render(request, 'policy_list.html' , {'queryset': queryset})

class PolicyModelForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)  # 初始化父类方法

		for field in self.fields.values():
			field.widget.attrs = {'class': 'form-control'}

	class Meta:
		model = models.PricePolicy
		fields = '__all__'


def policy_add(request):
	if request.method == "GET":
		form = PolicyModelForm()
		return render(request, 'form.html', {'form': form})

	form = PolicyModelForm(data=request.POST)
	if not form.is_valid():
		return render(request, 'form.html', {'form': form})

	form.save()
	return redirect('/policy/list/')

def policy_edit(request, pk):
	policy = models.PricePolicy.objects.filter(id=pk).first()
	if request.method == "GET" :
		form = PolicyModelForm(instance=policy)
		return render(request, 'form.html', {'form': form})

	form = PolicyModelForm(instance=policy, data=request.POST)
	if not form.is_valid():
		return render(request, 'form.html', {'form': form})

	form.save()
	return redirect('/policy/list/')



def policy_delete(request, pk):
	models.PricePolicy.objects.filter(id=pk).delete()
	return redirect('/policy/list/')