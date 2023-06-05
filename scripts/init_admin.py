# 启动django
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deal_crm.settings')
django.setup()



from web import models
from utils.encrypt import md5
#
# models.Administrator.objects.create(username='admin', password=md5('admin'), mobile='15857815615')
#
# level_object = models.Level.objects.create(title='VIP', percent=90)
#
#
for i in range(9, 100):
    models.Customer.objects.create(
        username='李-{}'.format(i),
        password=md5("123456"),
        mobile=f'199999999{i}',
        level_id=1,
        creator_id=1
    )