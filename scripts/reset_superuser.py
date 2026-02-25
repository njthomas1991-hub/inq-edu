#!/usr/bin/env python3
"""Reset or create a superuser and print credentials.

Usage: python scripts/reset_superuser.py

This script will:
 - find the first superuser (ordered by id) and set a new random password, OR
 - if no superuser exists, create one with username 'admin' and a random password.

It prints the username and the new password. Treat the output as sensitive.
"""
import os
import pathlib
import secrets
import sys

ROOT = str(pathlib.Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inclusive_quest_education.settings')
import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Require explicit confirmation via env var to avoid accidental runs
if os.environ.get('CONFIRM_RESET') != '1':
    print('ABORT: To run this script set CONFIRM_RESET=1 in the environment and re-run.')
    print('Example (PowerShell): $env:CONFIRM_RESET="1"; python scripts/reset_superuser.py')
    raise SystemExit(2)

# Generate a random password but do not print it unless explicitly allowed
pw = secrets.token_urlsafe(12)

su = User.objects.filter(is_superuser=True).order_by('id').first()
if su:
    su.set_password(pw)
    su.save()
    print('RESET')
    print('id:', su.id)
    print('username:', su.username)
    print('email:', su.email)
else:
    username = 'admin'
    # ensure unique username
    base = username
    i = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{i}"
        i += 1
    su = User.objects.create_superuser(username=username, email='admin@example.com', password=pw)
    print('CREATED')
    print('id:', su.id)
    print('username:', su.username)
    print('email:', su.email)

# By default do not print the new password. If you set ALLOW_PRINT_PASSWORD=1 the
# password will be printed to stdout. Alternatively the script will write the
# password to a local file named .saved_superuser (which is git-ignored).
if os.environ.get('ALLOW_PRINT_PASSWORD') == '1':
    print('password:', pw)
else:
    out = Path(ROOT) / '.saved_superuser'
    try:
        out.write_text(f"username={su.username}\npassword={pw}\n")
        print(f'Password written to {out} (git-ignored).')
    except Exception:
        # Fallback to printing a redaction message
        print('Password saved to local file failed — set ALLOW_PRINT_PASSWORD=1 to print to stdout')

print('\nNOTE: This script requires CONFIRM_RESET=1 to run and will not print passwords by default.')
