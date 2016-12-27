# -*- coding: utf-8 -*-
# encoding=utf8

import sys
import types
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from apiv1 import helpers
