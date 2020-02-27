
from eShop.piston.handler import BaseHandler
from django.http import HttpResponse
from eShop.webapp.models import Token
import json
import sys




class CustomerLogOutWebService(BaseHandler):
    def create(self, request):
        try:
            attrs = self.flatten_dict(request.POST)
            if 'token' in attrs:
                token=attrs['token']
                is_token_exists=Token.objects.filter(usertoken=token).exists()
                if is_token_exists==True:
                    Token.objects.filter(usertoken=token).update(usertoken="")
                    resp = {'status': 'OK','message': 'logged out'}
                    return HttpResponse(json.dumps(resp))
                else:
                    resp = {'status': 'OK','message': 'Token already deleted' }
                    return HttpResponse(json.dumps(resp))
            else:
                resp = {'status': 'NOT OK','message': 'token field empty'}
                return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK','message': 'error'}
            return HttpResponse(json.dumps(resp))