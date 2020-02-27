from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
from eShop.webapp.models import DeliveryOptions
import sys



class DeliveryOptionsHandler(BaseHandler):
    
    def read(self, request):
        try:
            options=[]
            optionref=DeliveryOptions.objects.all()
            for option in optionref:
                deliveryoption={}
                deliveryoption[option.DeliveryId]=option.DeliveryTypeName
                print option.DeliveryTypeName
                options.append(deliveryoption)
            resp = {'deliveryoptions': options}
            return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK','message': 'error',}
            return HttpResponse(json.dumps(resp))