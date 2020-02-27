from django.http import HttpResponse
import json
from eShop.piston.handler import BaseHandler
from eShop.webapp.models import StoreCategory, SubCategory
import sys




class CategoriesHandler(BaseHandler):
    def read(self, request):
        try:
            categories=[]
            categoriesref=StoreCategory.objects.all()
            for category in categoriesref:
                dictionary={}
                subcategorieslist=[]
                subcategoriesref=SubCategory.objects.filter(StoreCategoryType=category.StoreCategoryId)
                
                for subcat in subcategoriesref:
                    subcategorieslist.append(subcat.SubCategoryName)
                dictionary[category.StoreCategoryName]=subcategorieslist
                categories.append(dictionary)
            resp = {'categories': categories}
            return HttpResponse(json.dumps(resp))
        except:
            print sys.exc_info()
            resp = {'status': 'NOT OK','message': 'error',}
            return HttpResponse(json.dumps(resp))