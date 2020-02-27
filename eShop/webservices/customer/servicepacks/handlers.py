from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
from eShop.webapp.models import Market
import sys

class ServicePackHandler(BaseHandler):
    def create(self, request):
        try:
            attrs = self.flatten_dict(request.POST)
            servicepackslist=[]
            if attrs['marketname']!="":
                is_market_exists=Market.objects.filter(MarketName=attrs['marketname']).exists()
                
                if is_market_exists==True:
                    marketref=Market.objects.get(MarketName=attrs['marketname'])
                    servicepacks=marketref.has_servicepacks.all()
                    for servicepack in servicepacks:
                        servicepackslist.append(servicepack.ServicePackName)     
                    resp = {'servicepacks': servicepackslist}
                    return HttpResponse(json.dumps(resp))
                
                else:
                    resp = {'status': 'NOT OK','message':'Market name does not exist'}
                    return HttpResponse(json.dumps(resp))
            else:
                resp = {'status': 'NOT OK','message':'Market name is mandatory',}
                return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK',}
            return HttpResponse(json.dumps(resp))