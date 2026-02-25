#!/usr/bin/env python
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inclusive_quest_education.settings')
django.setup()
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

target = 'admin'
# Read password from environment to avoid storing secrets in code
pw = os.environ.get('ADMIN_PASSWORD')
if not pw:
    print('ERROR: ADMIN_PASSWORD environment variable is not set. Aborting.')
    raise SystemExit(2)

u = User.objects.filter(username=target).first()
if u:
    u.set_password(pw)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('PASSWORD_SET')
else:
    u2 = User.objects.filter(username__iexact=target).first()
    if u2:
        u2.username = target
        u2.is_staff = True
        u2.is_superuser = True
        u2.set_password(pw)
        u2.save()
        print('UPDATED')
    else:
        User.objects.create_superuser(target, '', pw)
        print('CREATED')

# Verify authentication
user = authenticate(username=target, password=pw)
print('AUTH_OK' if user else 'AUTH_FAIL')
