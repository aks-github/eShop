from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
from eShop.webapp.models import Token, CustomerStore, ServicePack, SalesReference, Market
from django.conf import settings
import sys
import datetime
from random import choice
import string


class CustomerRegistrationHandler(BaseHandler):

    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        print attrs
        #storecategoryref=None
        servicepackref=None
        
        validation=ValidateRegFields(attrs)
        
        if validation=="":
            try:
                try:
                    username= attrs['username'].replace('%40','@')
                    User.objects.get(username=username)
                    resp = {'status': 'username aready exist'}
                    return HttpResponse(json.dumps(resp))
                except:
                    password = attrs['password']
                    try:
                        marketref=Market.objects.get(MarketName=attrs['marketname'])
                        #salesrepidref=SalesReference.objects.get(SalesRepresentativeId=attrs['salesrepid']) 
                        #storecategoryref=StoreCategory.objects.get(StoreCategoryName=attrs['storecategory'])
                        servicepackref=ServicePack.objects.get(ServicePackName=attrs['servicepack'])
                        
                        if request.FILES['bannerimage'].content_type=='image/jpeg' and request.FILES['storeimage'].content_type=='image/jpeg' :
                                store=CustomerStore(StoreName=attrs['storename'], StreetAddress=attrs['streetaddr'],City=attrs['city'],PostalCode=attrs['postalcode'],Country=attrs['country'],State=attrs['state'],MainPhoneNumber=attrs['mainphonenumber'],ContactPerson=attrs['contactperson'],EmailAddress=attrs['emailaddress'].replace('%40','@'),Website=attrs['website'],HoursOfOperation=attrs['hoursofservice'],CreatedTime=datetime.datetime.now())
                                
                                User.objects.create_user(username=username,email=username,password=password)
                                
                                userref=User.objects.get(username=username)    
                                token=Token()
                                token.UserId=userref
                                store.SalesRepId=attrs['salesrepid']      
                                #store.StoreCategory=storecategoryref
                                store.ServicePack=servicepackref            
                                store.CustomerUserId=userref 
                                
                                
                                ref=request.FILES['bannerimage'].name                 
                                image_name=CharGenerator()+'_'+str(userref.pk)+'_'+attrs['storename']+ref.replace(' ','')
                                repath=settings.MEDIA_ROOT+'/'+image_name
                                if handle_uploaded_file(request.FILES['bannerimage'],repath):
                                    store.BannerImages=image_name
                                
                                ref=request.FILES['storeimage'].name
                                image_name=CharGenerator()+'_'+str(userref.pk)+'_'+attrs['storename']+ref.replace(' ','')
                                repath=settings.MEDIA_ROOT+'/'+image_name            
                                if handle_uploaded_file(request.FILES['storeimage'],repath):
                                    store.StoreLogo=image_name     
                                
                                store.save()
                                token.save()
                                
                                marketref.has_stores.add(store)
                                marketref.save()
                                resp = {'status': 'OK'}
                                return HttpResponse(json.dumps(resp))  
                        else:
                            resp = {'status': 'NOT OK','message': 'only jpeg images are allowed to upload'}
                            return HttpResponse(json.dumps(resp))
                    except:
                        print sys.exc_info()
                        resp = {'status': 'NOT OK','message': 'Mandatory Fields are missing',}
                        return HttpResponse(json.dumps(resp))
            except:
                print sys.exc_info()
                resp = {'status': 'NOT OK','message': 'error',}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'status': 'NOT OK','message': validation,}
            return HttpResponse(json.dumps(resp))




def ValidateRegFields(attrs):
    error=""
    
    try:
        if attrs['username']=="":
            error=error+"username,"
            
        if attrs['password']=="":
            error=error+"password,"
            
        if attrs['marketname']=="":
            error=error+"marketname,"
        
        if attrs['salesrepid']=="":
            error=error+"salesrepid,"
                 
        if attrs['storecategory']=="":
            error=error+"storecategory,"
        
        if attrs['servicepack']=="":
            error=error+"servicepack,"  
        
        if attrs['storename']=="":
            error=error+"storename," 
            
        if attrs['emailaddress']=="":
            error=error+"emailaddress," 
            
        if attrs['streetaddr']=="":
            error=error+"streetaddr," 
            
        if attrs['city']=="":
            error=error+"city,"  
    
        if attrs['postalcode']=="":
            error=error+"postalcode,"  
        
        if attrs['country']=="":
            error=error+"country,"  
        
        if attrs['state']=="":
            error=error+"state,"  
        
        if attrs['mainphonenumber']=="":
            error=error+"mainphonenumber,"  
            
        if attrs['contactperson']=="":
            error=error+"contactperson,"  
        
        if attrs['website']=="":
            error=error+"website,"  
            
        if attrs['hoursofservice']=="":
            error=error+"hoursofservice,"
    except:  
        error="fields are missing"
    return error




def handle_uploaded_file(upfile,path):
    try:
        dest = open(path, 'wb+')
        dest.write(upfile.read())
        dest.close()
        return True
    except:
        return False          
    
    
    
def CharGenerator():
    newstring=""
    chars = string.letters + string.digits
    for i in range(4):
        newstring = newstring + choice(chars)
    return newstring