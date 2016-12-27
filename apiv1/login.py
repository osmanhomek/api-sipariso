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

@csrf_exempt
@api_view(['POST'])
def check(request):
	try:
		formValues = helpers.getFormValues(request,"POST",["fusername","fpassword","fcustomer"])
		fusername, fpassword, fcustomer = [formValues.get(k) for k in ["fusername","fpassword","fcustomer"]]
		ggInfo = n11Info = hbInfo = ""
		resultStatus,resultMessage = 0,None

		if fusername is not None and fpassword is not None and fcustomer is not None:
			ggInfo,n11Info,hbInfo,resultMessage = loginDB("sipariso",fusername,fpassword,fcustomer)
		else:
			resultMessage = "API parametrelerini kontrol ediniz [inf0x12903]"
	except Exception, Argument:
	   	resultMessage = "Hata aciklamasi elde edilemedi. Try/Catch den donen arguman degeri null. [err0x12904]" if Argument is None else str(Argument) + " [err0x12905]"
	finally:
		helpers.hlogger(resultMessage,request)
		returnData = {
			"success": "0" if resultMessage is not None else "1",
			"message": resultMessage,
			"customer": fcustomer,
			"accounts": "" if resultMessage is not None else {"gittigidiyor":ggInfo,"n11":n11Info,"hepsiburada":hbInfo}
		}
		return helpers.JSONResponse(returnData)

def loginDB(dbName,fusername,fpassword,fcustomer):
	n11Info = ggInfo = hbInfo = resultMessage = None
	try:
		db = helpers.mongodb(dbName)
		if db is not None:
			users = db.users
			if users is not None:
				#QUERY
				userResult = users.find_one({"username":fusername,"password":fpassword,"customer":fcustomer})
				if userResult is not None:
					if "n11" in userResult:
						formValues = helpers.formKeyValues(["username","apikey","secretkey"],userResult["n11"])
						username,apikey,secretkey = [formValues.get(k) for k in ["username","apikey","secretkey"]]
						n11Info = {"username":str(username),"apikey":str(apikey),"secretkey":str(secretkey)}
					else:
						resultMessage = "API Error mongo dan donen data beklenen sekilde degil [err0x12911]"
					if "gittigidiyor" in userResult:
						formValues = helpers.formKeyValues(["username","apikey","secretkey","rolename","rolepass"],userResult["gittigidiyor"])
						username,apikey,secretkey,rolename,rolepass = [formValues.get(k) for k in ["username","apikey","secretkey","rolename","rolepass"]]
						ggInfo = {"username":str(username),"apikey":str(apikey),"secretkey":str(secretkey),"rolename":str(rolename),"rolepass":str(rolepass)}
					else:
						resultMessage = "API Error mongo dan donen data beklenen sekilde degil [err0x12912]"
					if "hepsiburada" in userResult:
						formValues = helpers.formKeyValues(["username","apiusername","apipassword","merchantid"],userResult["hepsiburada"])
						username,apiusername,apipassword,merchantid = [formValues.get(k) for k in ["username","apiusername","apipassword","merchantid"]]
						hbInfo = {"username":str(username),"apiusername":str(apiusername),"apipassword":str(apipassword),"merchantid":str(merchantid)}
					else:
						resultMessage = "API Error mongo dan donen data beklenen sekilde degil [err0x12913]"
				else:
					resultMessage = "Hatali kullanici adi,parola bilgisi ["+fcustomer+"] [inf0x12902]"
			else:
				resultMessage = "MongoClient problemi!!"
		else:
			resultMessage = "MongoClient db gelmedi"
	except Exception, Argument:
	   	resultMessage = "Hata aciklamasi elde edilemedi. Try/Catch den donen arguman degeri null. [err0x12904]" if Argument is None else str(Argument) + " [err0x12905]"
	finally:
		helpers.hlogger(resultMessage,None)
		return ggInfo,n11Info,hbInfo,resultMessage
