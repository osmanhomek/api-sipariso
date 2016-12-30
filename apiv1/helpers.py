
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import logging
logger = logging.getLogger("apisipariso")

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

####HELPERS
def tokenKeyGenerator(keyname,keyvalue):
    import jwt, os
    return jwt.encode({keyname:keyvalue}, os.getenv("AUTH_TOKEN_KEY"), algorithm='HS256')

def tokenCheck(encoded,customerid):
    import jwt, os
    returnData = {}
    token_check = jwt.decode(encoded, os.getenv("AUTH_TOKEN_KEY"), algorithms=['HS256'])
    if customerid in token_check.keys():
        token_create_time = token_check[customerid]
        simdi_time = simdi()
        zaman_farki = days_between(token_create_time, "%Y%m%d%H%M%S", simdi_time, "%Y%m%d%H%M%S")
        if zaman_farki>int(os.getenv("TOKEN_TIME_SPAN")):
            returnData = {"success":0,"message":"Token degeri pasif durumda. Token degerinin aktif kalma suresi " + str(os.getenv("TOKEN_TIME_SPAN")) + "dk. dir."}
        else:
            returnData = {"success":1,"message":""}
    else:
        returnData = {"success":0,"message":"Token / Customer Id uyusmazligi"}

    return returnData

def generateSecretkey():
    length = 32
    chars = "AaBbCcDdEeFfGgHhJjKkMmNnPpQqRrSsTtUuVvWwXxYyZz23456789@#+"
    from os import urandom
    return "".join(chars[ord(c) % len(chars)] for c in urandom(length))

def getFormValues(request,postType,aryFormKeys):
	returnData = {}
	if postType == "POST":
		for key in aryFormKeys:
			if key in request.POST:
				returnData[key] = request.POST[key]
			else:
				returnData[key] = None
	return returnData

def formKeyValues(arrayKeys,arrayValues):
	returnData = {}
	for key in arrayKeys:
		if key in arrayValues:
			returnData[key] = arrayValues[key]

	return returnData

def mongodb(dbName):
    try:
        db = None
        import pymongo
        from pymongo import MongoClient
        import os
        mongo_url = os.getenv("MONGO_URL")
        if mongo_url is not None:
            client = MongoClient(mongo_url)
            db = client[dbName]
    except Exception, Argument:
        # log a kayit gonderilebilir
        print (str(Argument))
	   	#pass
    finally:
        return db

def suan():
    from time import gmtime, strftime
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def simdi():
    from time import gmtime, strftime
    return strftime("%Y%m%d%H%M%S", gmtime())

def days_between(d1, d1Format, d2, d2Format):
    from datetime import datetime
    d1 = datetime.strptime(d1, d1Format)
    d2 = datetime.strptime(d2, d2Format)
    return abs((d2 - d1).seconds)/60

def hlogger(resultMessage,request):
    if resultMessage is not None:
        #logger.error(str(zaman) + ":error:"+resultMessage)
        #logger.debug(str(zaman) + ":debug:"+resultMessage)
        logger.info(resultMessage, exc_info=True, extra={'request': request})
        #logger.warning(str(zaman) + ":warning:"+resultMessage)
        #logger.critical(str(zaman) + ":critical:"+resultMessage)
