# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from apiv1 import helpers
from apiv1 import formprocessors

@csrf_exempt
@api_view(['POST'])
def login(request):
	try:
		returnData = None
		aryFormKeys = ["fusername","fpassword"]
		formValues = formprocessors.getFormValues(request,"POST",aryFormKeys)
		fusername, fpassword = [formValues.get(k) for k in aryFormKeys]

		if fusername is not None and fpassword is not None:
			import pymongo
			from pymongo import MongoClient

			client = MongoClient('mongodb://apin11:5gh4SAkj316T@ds055772.mlab.com:55772/sipariso')
			db = client.sipariso
			users = db.users
			userResult = users.find_one({"username":fusername,"password":fpassword})
			if userResult is not None:
				if "apikey" in userResult:
					apikey = userResult["apikey"]
					secretkey = userResult["secretkey"]

					returnData = {"apikey":apikey,"secretkey":secretkey,"success":1,"message":""}
				else:
					# mongo dan donen data beklenen sekilde degil
					returnData = {"apikey":"","secretkey":"","success":0,"message":"API Error [err0x12901]"}
			else:
				returnData = {"apikey":"","secretkey":"","success":0,"message":"Hatali kullanici adi,parola bilgisi [inf0x12902]"}
		else:
			returnData = {"apikey":"","secretkey":"","success":0,"message":"API parametrelerini kontrol ediniz [inf0x12903]"}
	except Exception, Argument:
		errorText = ""
		if Argument is None:
			# Try/Catch den donen arguman degeri null.
			errorText = "Hata aciklamasi elde edilemedi [err0x12904]"
		else:
			errorText = str(Argument) + "[err0x12905]"

	   	returnData = {"apikey":"","secretkey":"","success":0,"message":errorText}
	finally:
		return helpers.JSONResponse(returnData)
