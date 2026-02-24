import inspect
import django
from django.db import models

def main():
    print('Django version:', django.get_version(), django.VERSION)
    print('CheckConstraint repr:', repr(models.CheckConstraint))
    try:
        sig = inspect.signature(models.CheckConstraint)
        print('signature:', sig)
    except Exception as e:
        print('signature error:', e)

if __name__ == '__main__':
    main()
