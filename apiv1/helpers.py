
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import logging
logger = logging.getLogger(__name__)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

####HELPER
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

def hlogger(resultMessage,request):
    if resultMessage is not None:
        logger.error(resultMessage, exc_info=True, extra={'request': request})
        logger.debug(resultMessage, exc_info=True, extra={'request': request})
