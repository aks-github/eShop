from django.template.loader import get_template
from django.http import HttpResponse
from django.template.context import Context
from eShop.webapp.models import CustomerStore, Market, SubCategory,\
    StoreCategory
import sys
from django.core.paginator import Paginator, EmptyPage,InvalidPage
from django.shortcuts import redirect


def MarketAdmin(request):
    if 'usertype' in request.session and request.session['usertype']=="MARKET_ADMIN":
        try:
            marketref=Market.objects.get(UserId=request.session['userid'])
            stores=marketref.has_stores.all()
            acceptedstores=[]
            for store in stores:
                if store.Is_Activated==True:
                    acceptedstores.append(store)
            paginator = Paginator(acceptedstores, 10)
            try:
                page = int(request.GET.get('pageA', '1'))
            except ValueError:
                page = 1
            try:
                acceptedstores = paginator.page(page)
            except (EmptyPage, InvalidPage):
                acceptedstores = paginator.page(paginator.num_pages)
            
            
            
            requestedstores=[]
            for store in stores:
                if store.Is_Activated==False and store.Is_Blocked==False:
                    requestedstores.append(store)
           
            paginator = Paginator(requestedstores, 10)
            try:
                page = int(request.GET.get('pageB', '1'))
            except ValueError:
                page = 1
            try:
                stores = paginator.page(page)
            except (EmptyPage, InvalidPage):
                stores = paginator.page(paginator.num_pages)
                
        except:
            print sys.exc_info()
            
        t=get_template('marketadmin_index.html')
        c=Context({'stores':stores,'acceptedstores':acceptedstores,'marketadmin':marketref})
        return HttpResponse(t.render(c))
    
    else:
        return redirect("/")






def AcceptStore(request):
    if 'usertype' in request.session and request.session['usertype']=="MARKET_ADMIN":
        if 'storeid' in request.GET:
            try:
                print request.GET['storeid']
                CustomerStore.objects.filter(StoreId=int(request.GET['storeid'])).update(Is_Activated=True)
                return HttpResponse("store accepted")
            except:
                print sys.exc_info()
                return HttpResponse("Error in Store accepting")
        else:
            return HttpResponse("Method Not allowed")
    else:
        return HttpResponse("Session Expired")



def DeclineStore(request):
    if 'usertype' in request.session and request.session['usertype']=="MARKET_ADMIN":
        if 'storeid' in request.GET:
            try:
                print request.GET['storeid']
                CustomerStore.objects.filter(StoreId=int(request.GET['storeid'])).update(Is_Blocked=True)
                marketref=Market.objects.get(UserId=request.session['userid'])
                stores=marketref.has_stores.all()
                for store in stores:
                    if store.Is_Blocked==True:
                        marketref.has_stores.remove(store)
                return HttpResponse("store declined")
            except:
                return HttpResponse("Error in Store declining")
        else:
            return HttpResponse("Method Not allowed")
    else:
        return HttpResponse("Session Expired")




def StoreDetails(request):
    if 'usertype' in request.session and request.session['usertype']=="MARKET_ADMIN":
        t=get_template('viewstoredetails.html')
        try:
            marketref=Market.objects.get(UserId=request.session['userid'])
            storedetails=CustomerStore.objects.get(StoreId=int(request.GET['storeid']))
            storecategories=StoreCategory.objects.all()
            storesubcategories=storedetails.has_subcategories.all()
            dic={}
            selectedsubcategories=[]
            for i in storesubcategories:
                selectedsubcategories.append(i.SubCategoryName)
            
            for storecategory in storecategories:
                subcategory=SubCategory.objects.filter(StoreCategoryType=storecategory.StoreCategoryId)
                
                
                temp=[]
                for i in subcategory:  
                    if i.SubCategoryName in selectedsubcategories:
                        temp.append(i.SubCategoryName)
                        dic[storecategory.StoreCategoryName]=temp

        except:
            print sys.exc_info()
        c=Context({'storedetails':storedetails,'marketref':marketref,'message':'Store'+' '+'"'+storedetails.StoreName+'"'+' '+'Details','dic':dic})
        return HttpResponse(t.render(c))
    else:
        return redirect("/")
