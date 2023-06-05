from django.template import Library
from django.conf import settings
register = Library()

@register.inclusion_tag('tag/nb_menu.html')
def nb_menu(request):
	user_menu_list = settings.NB_MENU[request.nb_user.role]

	for menu in user_menu_list:
		for child in menu['children']:
			# if child['url'] == request.path_info:
			if child['name']  == request.nb_user.menu_name:
				child['class'] = 'active'

			else:
				child['class'] = ''
		pass

	return {'menu_list' : user_menu_list}