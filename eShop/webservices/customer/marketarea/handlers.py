from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
from eShop.webapp.models import Market
import sys



class MarketAreaHandler(BaseHandler):
    def read(self, request):
        try:
            marketnames=[]
            marketref=Market.objects.all()[:5]
            for market in marketref:
                marketnames.append(market.MarketName) 
            resp = {'marketnames': marketnames}
            return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK','message': 'error',}
            return HttpResponse(json.dumps(resp))