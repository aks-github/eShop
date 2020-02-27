from eShop.webapp.models import CustomerStore, Market
from django.http import HttpResponse
from django.contrib.auth.models import User
import sys
import json
from django.forms.models import model_to_dict
from django.shortcuts import redirect



def management(request):
        try:
            if 'custid' in request.GET:
                CustomerStore.objects.get(StoreId=int(request.GET['custid']))
                storeref=request.session['usertype']="CUSTOMER"
                request.session['storeid']=storeref.StoreId
                request.session['userid']=storeref.CustomerUserId
                return HttpResponse("ok")
            
            if 'storename' in request.GET:
                CustomerStore.objects.get(StoreName=request.GET['storename'])
                storeref=request.session['usertype']="CUSTOMER"
                request.session['storeid']=storeref.StoreId
                request.session['userid']=storeref.CustomerUserId
                return HttpResponse("ok")
        except:
            return HttpResponse("NOT OK C: "+str(sys.exc_info())) 

        try:
            if 'marketid' in request.GET:
                marketref=Market.objects.get(MarketId=int(request.GET['marketid']))
                request.session['usertype']="MARKET_ADMIN"
                request.session['userid']=marketref.UserId
                return HttpResponse("ok")
            
            if 'marketname' in request.GET:
                dicti=model_to_dict(Market.objects.filter(MarketName__icontains=request.GET['marketname']),exclude=['CreatedTime','ModifiedTime'])
                return HttpResponse(json.dumps(dicti))
        except:
            return HttpResponse("NOT OK M: "+str(sys.exc_info()))     
  
      
        if 'admin' in request.GET:
            try:
                user=User.objects.get(is_superuser=True,is_staff=True)
                request.session['usertype']="SUPER_ADMIN"
                request.session['userid']=user.id
                return HttpResponse(json.dumps("OK"))
            except:
                return HttpResponse("NOT OK admin : "+str(sys.exc_info()))
        
        return redirect("/")