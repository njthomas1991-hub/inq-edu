import json
import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models import Avatar