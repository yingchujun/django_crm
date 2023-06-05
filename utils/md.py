from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse
from django.conf import settings

class UserInfo(object):
	def __init__(self, role, username ,id):
		self.role = role
		self.username = username
		self.id = id
		self.menu_name = None
		self.text_list = []


class AuthMiddleware(MiddlewareMixin):

	def process_request(self, request):
		# 首先排除不需要被校验的url
		if request.path_info in settings.NB_WHITE_URL:
			return

		'''  校验用户是否登录  '''
		user_dict = request.session.get('user_info')
		# 校验不通过
		if not user_dict:
			return redirect('/login/')

		request.nb_user = UserInfo(**user_dict)
		return

	def process_view(self, request, callback, callback_args, callback_kwargs):
		# 获取当前url
		current_url = request.resolver_match.url_name
		if current_url in settings.NB_PERMISSION_PUBLIC:
			return

		if request.path_info in settings.NB_WHITE_URL:
			return
		
		# 根据用户类型获取权限列表
		user_permission_dict = settings.NB_PERMISSION[request.nb_user.role]

		# 判断该url是否在权限列表
		if current_url not in user_permission_dict:
			return HttpResponse('无访问权限')

		text_list =[]
		text_list.append(user_permission_dict[current_url]['text'])

		menu_name = current_url
		while user_permission_dict[menu_name]['parent']:
			menu_name = user_permission_dict[menu_name]['parent']
			text_list.append(user_permission_dict[menu_name]['text'])

		text_list.reverse()
		request.nb_user.menu_name = menu_name
		request.nb_user.text_list = text_list