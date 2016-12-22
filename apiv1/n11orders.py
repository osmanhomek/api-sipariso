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

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
def getOrdersCount(request):
	try:
		aryFormKeys = ["apikey","secretkey","status"]
		formValues = formprocessors.getFormValues(request,"POST",aryFormKeys)
		apikey, secretkey, status = [formValues.get(k) for k in aryFormKeys]

		if apikey is not None and secretkey is not None and status is not None:
			wsdl = 'https://api.n11.com/ws/OrderService.wsdl'
			from suds.client import Client
			client = Client(wsdl)

			auth = {
				'appKey':apikey,
            	'appSecret':secretkey
			}
			searchData = {
	            'productId':None,
	            'status':status,
	            'buyerName':"",
	            'orderNumber':"",
	            'productSellerCode':"",
	            'recipient':"",
	            'sameDayDelivery':None,
	            'period':{
	            	'startDate':"",
	            	'endDate':"",
	            }
			}
			pagingData = {
            	'currentPage':0,
            	'pageSize':1
			}
			recordCount = None
			response = client.service.OrderList(auth=auth, searchData=searchData, pagingData=pagingData)
			if "result" in response:
				if "status" in response.result:
					response_status = response.result.status
					if response_status == "success":

						if "pagingData" in response:
							pagingData = response.pagingData
							currentPage = pagingData.currentPage
     						pageSize = pagingData.pageSize
     						totalCount = pagingData.totalCount
     						pageCount = pagingData.pageCount

     						recordCount = totalCount

				else:
					returnData = {"status":status,"recordcount":"","success":0,"message":"API sonuc bilgisi basarili olarak gelmedi [inf0x12903]"}
			else:
				returnData = {"status":status,"recordcount":"","success":0,"message":"API mekanizmasindan sonuc gelmedi [inf0x12903]"}

			if recordCount is None:
				returnData = {"status":status,"recordcount":"","success":0,"message":"Toplam kayit adedi alinamadi [inf0x12903]"}
			else:
				returnData = {"status":status,"recordcount":recordCount,"success":1,"message":""}
		else:
			returnData = {"status":"","recordcount":"","success":0,"message":"API parametrelerini kontrol ediniz.[inf0x12903]"}
	except Exception, Argument:
		errorText = ""
		if Argument is None:
			# Try/Catch den donen arguman degeri null.
			errorText = "Hata aciklamasi elde edilemedi"
		else:
			errorText = str(Argument)

		returnData = {"status":"","recordcount":"","success":0,"message":errorText}
	finally:
		if returnData["success"] == 0:
			logger.error(returnData["message"], exc_info=True, extra={'request': request})

		return helpers.JSONResponse(returnData)

@csrf_exempt
@api_view(['POST'])
def getOrders(request):
	try:
		aryFormKeys = ["apikey","secretkey","status"]
		formValues = formprocessors.getFormValues(request,"POST",aryFormKeys)
		apikey, secretkey, status = [formValues.get(k) for k in aryFormKeys]

		if apikey is not None and secretkey is not None and status is not None:
			wsdl = 'https://api.n11.com/ws/OrderService.wsdl'

			import scio
			import urllib2
			client = scio.Client(urllib2.urlopen(wsdl))

			fauth = client.type.Authentication()
			fauth.appKey = apikey
			fauth.appSecret = secretkey

			fperiod = client.type.OrderSearchPeriod()
			fperiod.startDate = ""
			fperiod.endDate = ""

			fsearchData = client.type.OrderDataListRequest()
			#fsearchData.productId = ''
			fsearchData.status = status
			fsearchData.buyerName = ""
			fsearchData.orderNumber = ""
			fsearchData.productSellerCode = ""
			fsearchData.recipient = ""
			fsearchData.sameDayDelivery = ""
			fsearchData.period = fperiod

			fpagingData = client.type.PagingData()
			fpagingData.currentPage = 0
			fpagingData.pageSize = 100
			#fpagingData.totalCount = ""
			#fpagingData.pageCount = ""

			rresult = None
			response = client.service.DetailedOrderList(auth=fauth, searchData=fsearchData, pagingData=fpagingData)
			if hasattr(response,"result"):
				rresult = response.result
				if hasattr(rresult,"status"):
					rstatus = str(rresult.status).strip()
					if rstatus == "success":
						if hasattr(response,"pagingData"):
							pagingData = response.pagingData
							if hasattr(pagingData,"totalCount"):
								totalCount = pagingData.totalCount
								if totalCount == 0:
									returnData = {"status":status,"recordcount":totalCount,"success":1,"message":"islem basarili"}
								else:
									if hasattr(response,"orderList"):
										orderList = response.orderList
										if hasattr(orderList,"order"):
											order = orderList.order
											fullOrderData = []
											for orderRec in order:
												responseJson = {}
												#RcreateDate, Rid, RorderNumber, RpaymentType, Rstatus, RtotalAmount = ""
												if hasattr(orderRec,"createDate"): RcreateDate = str(orderRec.createDate)
												if hasattr(orderRec,"id"): Rid = str(orderRec.id)
												if hasattr(orderRec,"orderNumber"): RorderNumber = str(orderRec.orderNumber)
												if hasattr(orderRec,"paymentType"): RpaymentType = str(orderRec.paymentType)
												if hasattr(orderRec,"status"): Rstatus = str(orderRec.status)
												if hasattr(orderRec,"totalAmount"): RtotalAmount = str(orderRec.totalAmount)

												responseJson["createDate"] = RcreateDate
												responseJson["orderid"] = Rid
												responseJson["orderNumber"] = RorderNumber
												responseJson["paymentType"] = RpaymentType
												responseJson["orderstatus"] = Rstatus
												responseJson["totalAmount"] = RtotalAmount

												fullOrderData.append(responseJson)

												returnData = {"status":"","recordcount":totalCount,"success":1,"orders":str(fullOrderData),"message":"islem basarili"}
					else:
						returnData = {"status":"","recordcount":"","orders":"","success":0,"message":"API den cevap success donmedi " + str(rstatus)}
			else:
				returnData = {"status":"","recordcount":"","success":0,"message":"API den cevap donmedi","orders":""}
		else:
			returnData = {"status":"","recordcount":"","success":0,"message":"API parametrelerini kontrol ediniz.[inf0x12903]","orders":""}
	except Exception, Argument:
		errorText = ""
		if Argument is None:
			# Try/Catch den donen arguman degeri null.
			errorText = "Hata aciklamasi elde edilemedi [err0x12904]"
		else:
			errorText = str(Argument) + "[err0x12905]"

	   	returnData = {"status":"","recordcount":"","success":0,"message":errorText,"orders":""}
	finally:
		if returnData["success"] == 0:
			message = ""
			if "message" in returnData:
				message = returnData["message"]
			else:
				message = "returnData bilgisi gelmedi veya icerisinde message key i bulunmuyor"

			logger.error(message, exc_info=True, extra={'request': request})
			logger.debug(message, exc_info=True, extra={'request': request})
			logger.info(message, exc_info=True, extra={'request': request})
			logger.warning(message, exc_info=True, extra={'request': request})
			logger.critical(message, exc_info=True, extra={'request': request})
			logger.exception(message, exc_info=True, extra={'request': request})

		return helpers.JSONResponse(returnData)
