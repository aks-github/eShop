from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
import sys
from eShop.webapp.models import Token, CustomerStore

class CustomerProfileHandler(BaseHandler):
    
    def create(self, request):
        storeHolder=[]
        if 'token' in request.POST:
            attrs = self.flatten_dict(request.POST)
            token=attrs['token']
            is_token_exist=Token.objects.filter(usertoken=token).exists()
            if is_token_exist==True:
                try:
                    token=Token.objects.select_related().get(usertoken=token)
                   
                    storeref=CustomerStore.objects.get(CustomerUserId=token.UserId)
                    
                    store={}
                    store['StoreName']=storeref.StoreName
                    store['StreetAddress']=storeref.StreetAddress
                    store['City']=storeref.City
                    store['PostalCode']=storeref.PostalCode
                    store['State']=storeref.State
                    store['Country']=storeref.Country
                    store['MainPhoneNumber']=storeref.MainPhoneNumber
                    store['ContactPerson']=storeref.ContactPerson
                    store['EmailAddress']=storeref.EmailAddress
                    store['Website']=storeref.Website
                    store['BannerImages']='/media/'+ storeref.BannerImages
                    store['StoreLogo']='/media/'+ storeref.StoreLogo
                    store['HoursOfOperation']=storeref.HoursOfOperation
                    store['NumbersofProductsUploaded']=storeref.ProductsUploaded
                    
                    market=storeref.market_set.get()
                    store['marketname']=market.MarketName
                        
                    storeHolder.append(store)
                    resp = {'myprofile':storeHolder}
                    return HttpResponse(json.dumps(resp))
                except:
                    print sys.exc_info()
                    resp = {'status': 'NOT OK','message': 'error',}
                    return HttpResponse(json.dumps(resp))
            else:
                resp = {'status': 'NOT OK','message': 'Please login again',}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'status': 'NOT OK','message': 'token not found in request',}
            return HttpResponse(json.dumps(resp))
        

'''
product=ProductBean()
                
product.ProductName=i.ProductTitle
product.ProductDescription=i.ProductDescription
product.ProductPrice=i.ProductPrice
product.ProductImage=i.ProductImage
product.ProductTypeId=i.ProductTypeId.StoreCategoryName
product.ProductSubCat=i.ProductSubCat.SubCategoryName
product.ProductDelivery=i.has_deliveryoptions.DeliveryTypeName


class ProductBean:
    _ProductName,_ProductPrice,_ProductDescription,_ProductImage,_ProductTypeId,_ProductSubCat,_ProductDelivery=None,None,None,None,None,None,None
    
    @property
    def ProductName(self):
        return self._ProductName
    @ProductName.setter
    def ProductName(self, ProductName):
        self._ProductName = ProductName
        
    @property
    def ProductPrice(self):
        return self._ProductPrice
    @ProductPrice.setter
    def ProductPrice(self, ProductPrice):
        self._ProductPrice = ProductPrice
        
    
    @property
    def ProductDescription(self):
        return self._ProductDescription
    @ProductDescription.setter
    def ProductDescription(self, ProductDescription):
        self._ProductDescription = ProductDescription    
        
        
    @property
    def ProductImage(self):
        return self._ProductImage
    @ProductImage.setter
    def ProductImage(self, ProductImage):
        self._ProductImage = ProductImage        
        
    
    @property
    def ProductTypeId(self):
        return self._ProductTypeId
    @ProductTypeId.setter
    def ProductTypeId(self, ProductTypeId):
        self._ProductTypeId = ProductTypeId    
   
   
    @property
    def ProductSubCat(self):
        return self._ProductSubCat
    @ProductSubCat.setter
    def ProductSubCat(self, ProductSubCat):
        self._ProductSubCat = ProductSubCat    
        
    @property
    def ProductDelivery(self):
        return self._ProductDelivery
    @ProductDelivery.setter
    def ProductDelivery(self, ProductDelivery):
        self._ProductDelivery = ProductDelivery   
''' 