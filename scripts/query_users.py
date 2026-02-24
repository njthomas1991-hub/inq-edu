import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inclusive_quest_education.settings')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import django
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
print('Total users:', User.objects.count())
for u in User.objects.order_by('-id')[:10]:
    print(u.id, u.username, repr(u.email), u.has_usable_password())
