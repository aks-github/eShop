
from eShop.piston.handler import BaseHandler
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import string
from random import choice
import json
from eShop.webapp.models import Token
import sys
from eShop.webservices.customer.registration.handlers import CharGenerator


class CustomerLogInWebService(BaseHandler):
    
    def create(self, request):
        try:
            attrs = self.flatten_dict(request.POST)
            if 'username' in attrs and 'password' in attrs:
                email = attrs['username'].replace('%40','@')
                password = attrs['password']  
                user = authenticate(username=email, password=password)        
                if user is not None:
                    m=User.objects.get(username=email)
                    login(request, user)            
                    t=Token.objects.get(UserId__id=m.id)
                    newtoken=''
                    if t.usertoken=="":
                        newtoken=CharGenerator()
                        t.usertoken=newtoken
                        t.save()
                    else:
                        newtoken=t.usertoken
                    resp = {'token': newtoken}
                    return HttpResponse(json.dumps(resp))
                else:           
                    resp = {'status': 'NOT OK','message':'user does not exist'}
                    return HttpResponse(json.dumps(resp))
            else:
                resp = {'status': 'NOT OK','message': 'username or password field is empty'}
                return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK','message':'error'}
            return HttpResponse(json.dumps(resp))
        
        
        
        
        
def CharGenerator():
    chars = string.letters + string.digits
    newtoken=''            
    for i in range(15):
        newtoken = newtoken + choice(chars)
    return newtoken