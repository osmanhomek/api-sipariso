
def getFormValues(request,postType,aryFormKeys):
	returnData = {}
	if postType == "POST":
		for key in aryFormKeys:
			if key in request.POST:
				returnData[key] = request.POST[key]
			else:
				returnData[key] = None
	return returnData


