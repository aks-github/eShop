from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
import sys
from eShop.webapp.models import CustomerStore, Product,Token,\
    DeliveryOptions
from django.conf import settings
from eShop.webservices.customer.registration.handlers import CharGenerator
import datetime
import string
from random import choice



class ProductUploadHandler(BaseHandler):
    def create(self, request):
        try:
            attrs = self.flatten_dict(request.POST)
            valref=validateFields(attrs)
            if valref=="":
                token=attrs['token']
                is_token_exists=Token.objects.filter(usertoken=token).exists()
                print is_token_exists
                if is_token_exists!=None:
                    if 'productimage' in request.FILES:
                        deliverytype=attrs['deliveryoption'].replace("%2C",",")
                        print deliverytype
                        deliverytype=deliverytype.split(',')
                        print deliverytype
                        ref=request.FILES['productimage'].name.replace(" ","")
                        image_name=CharGenerator()+ref.replace(' ','')
                        repath=settings.MEDIA_ROOT+'/'+image_name        
                        token=Token.objects.get(usertoken=token)
                        userid=token.UserId
                                
                        productref=Product(ProductDescription=attrs['description'].replace("+"," "),ProductPrice=attrs['price'],Quantity=int(attrs['quantity']),ProductType=attrs['productcategory'],CreatedTime=datetime.datetime.now())
                                
                        if handle_uploaded_file(request.FILES['productimage'],repath):
                            productref.ProductImage=image_name
                            productref.save()
                            
                            for i in deliverytype:
                                deliveryoption=DeliveryOptions.objects.get(DeliveryId=int(i))
                                productref.has_deliveryoptions.add(deliveryoption)
                            
                            customerref=CustomerStore.objects.get(CustomerUserId=userid)
                            customerref.has_products.add(productref)
                            customerref.save()
                            market=customerref.market_set.get()
                            #marketref=Market.objects.get(MarketId=market.MarketId)
                            market.has_products.add(productref) 
                            market.save()
                               
                            resp = {'status': 'OK'}
                            return HttpResponse(json.dumps(resp))
                        else:
                            resp = {'status': 'NOT OK','message': 'Product not uploaded'}
                            return HttpResponse(json.dumps(resp))
                        #else:
                            #resp = {'status': 'NOT OK','message': 'Only jpeg formats are allowed'}
                            #return HttpResponse(json.dumps(resp))
                    else:
                        resp = {'status': 'NOT OK','message': 'Product image is mandatory'}
                        return HttpResponse(json.dumps(resp))
                else:
                    resp = {'status': 'NOT OK','message':'Please Login again'}
                    return HttpResponse(json.dumps(resp))
            else:
                resp = {'status': 'NOT OK','message':valref+" fields are missing"}
                return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK','message':'error'}
            return HttpResponse(json.dumps(resp))
        
        
        
        
        
def handle_uploaded_file(upfile,path):
    try:
        dest = open(path, 'wb+')
        dest.write(upfile.read())
        dest.close()
        return True
    except:
        return False          
    
    
    
def validateFields(attrs):
    error=""
    try:
        if attrs['token']=="":
            error=error+"token,"
                
        if attrs['deliveryoption']=="":
            error=error+"deliveryoption,"
                
        if attrs['productcategory']=="":
            error=error+"productcategory,"
            
        if attrs['quantity']=="":
            error=error+"quantity,"
                     
        if attrs['description']=="":
            error=error+"description,"
            
        if attrs['price']=="":
            error=error+"price,"        
    except:
        print sys.exc_info()  
        error="fields are missing"
        
    return error


def CharGenerator():
    newstring=""
    chars = string.letters + string.digits
    for i in range(4):
        newstring = newstring + choice(chars)
    return newstring