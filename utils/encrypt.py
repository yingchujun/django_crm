import  hashlib
from deal_crm.settings import SECRET_KEY

def md5(data_string):
	obj = hashlib.md5(SECRET_KEY.encode('utf-8'))
	obj.update(data_string.encode('utf-8'))
	return obj.hexdigest()