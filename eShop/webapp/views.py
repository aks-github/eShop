from django.contrib.auth import authenticate, logout
from eShop.webapp.models import MapUserTypeWithUser, CustomerStore, Market,\
    Product, StoreCategory, SubCategory
from django.views.generic.simple import redirect_to
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import Context
from django.template.loader import get_template
import json
import sys
from django.core.paginator import Paginator, EmptyPage,InvalidPage
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
import threading
import time
from django.conf.global_settings import EMAIL_HOST_USER
import string
from random import choice
from django.db.models import Count
from eShop.piston.models import Consumer


def IndexPage(request):
    t=get_template('index.html')
    marketsref=Market.objects.all().order_by('-MarketId')
    storeref=CustomerStore.objects.all().order_by('-StoreId')
    paginator = Paginator(storeref, 9)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        storeref = paginator.page(page)
    except (EmptyPage, InvalidPage):
        storeref = paginator.page(paginator.num_pages)
    c=Context({'stores':storeref,'markets':marketsref})
    return HttpResponse(t.render(c))





def ValidateUser(request):
    t=get_template('index.html')
    try:
        if request.method == 'POST':
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            
            if user is not None:
                if user.is_superuser==True and user.is_staff==True:
                    request.session['usertype']="SUPER_ADMIN"
                    request.session['userid']=user.id
                    return redirect_to(request, "/listmarket")
                
                else:
                    userin=MapUserTypeWithUser.objects.get(UserId=user.id)
                    print userin.UserTypeId.UserTypeName
                    usertypename=userin.UserTypeId.UserTypeName
                    
                    if usertypename=="CUSTOMER":
                        storeref=CustomerStore.objects.get(CustomerUserId=user.id)
                        if storeref.Is_Blocked==False:
                            if storeref.Is_Activated==True:
                                request.session['usertype']="CUSTOMER"
                                request.session['storeid']=storeref.StoreId
                                request.session['userid']=user.id
                                return redirect_to(request,"/customerhome")
                            else:
                                c=Context({'message':'Account not Activated'})
                                return HttpResponse(t.render(c))
                        else:
                            c=Context({'message':'Account Blocked. Contact Sales Representative for further information.'})
                            return HttpResponse(t.render(c))
                    
                    elif usertypename=="MARKET_ADMIN":
                        request.session['usertype']="MARKET_ADMIN"
                        request.session['userid']=user.id
                        return redirect_to(request,'/marketadmin')
                    
                    elif usertypename=="CONSUMER":
                        request.session['usertype']="CONSUMER"
                        request.session['userid']=user.id
                        return redirect_to(request,'/consumerhome')
                    else:
                        c=Context({'message':'Unknown user'})
                        return HttpResponse(t.render(c))
                    
                    
            else:
                c=Context({'message':'Invalid Credentials'})
                return HttpResponse(t.render(c))
        else:
            c=Context({'message':'Invalid Method'})
            return HttpResponse(t.render(c))
    except:
        print sys.exc_info()
        c=Context({'message':'Invalid Method'})
        return HttpResponse(t.render(c))

   
   
   
   
def MarketList(request):
    listofmarkets=[]
    marketsref=Market.objects.all()
    for i in marketsref:
        listofmarkets.append(i.MarketName)
    return HttpResponse(json.dumps(listofmarkets))





def StoreSearch(request):
    listofstores=[]
    storesref=CustomerStore.objects.filter(StoreName__istartswith=request.GET['term'])[:10]
    if storesref is not None:
        for store in storesref:
            print store.StoreName
            listofstores.append(store.StoreName)
    return HttpResponse(json.dumps(listofstores)) 




def ProductSearch(request):
    listofproducts=[]
    productref=Product.objects.filter(ProductDescription__istartswith=request.GET['term'])[:10]
    if productref is not None:
        for product in productref:
            print product.ProductDescription
            listofproducts.append(product.ProductDescription)
    return HttpResponse(json.dumps(listofproducts)) 

#changes made by amit
def CategorySearch(request):
    listofcategories=[]
    user = User.objects.get(id=request.session['userid'])
    customerstoreref = CustomerStore.objects.get(CustomerUserId = user)
    categoryref = customerstoreref.has_products.filter(ProductType__istartswith=request.GET['term'])[:10]
    categoryref = categoryref.values('ProductType').annotate(count=Count('ProductId'))
    if categoryref is not None:
        for category in categoryref:
            print category['ProductType']
            listofcategories.append(category['ProductType'])
    return HttpResponse(json.dumps(listofcategories)) 
#end


def IndexPageSearch(request):
    try:
        if 'storeSearch' in request.POST and request.POST['storeSearch']!="":
            request.session['storeSearch']=request.POST['storeSearch']
            return HttpResponseRedirect('/store')
        elif 'productSearch' in request.POST and request.POST['productSearch']!="":
            request.session['productSearch']=request.POST['productSearch']
            return HttpResponseRedirect('/product')
        else:
            HttpResponseRedirect('/')
    except:
        print sys.exc_info()
        return redirect('/')




def StoresSearch(request):
    if 'usertype' in request.session and 'userid' in request.session:
        
        if request.session['usertype']=="CONSUMER":
            try:
                t=get_template('consumerpagestores.html')
                marketsref=Market.objects.all()[:10]
                #consumerref=Consumer.objects.get(UserId_id=int(request.session['userid']))
                customerstoreref=None
                searchedfor=""
                
                if 'storeSearch' in request.session and request.session['storeSearch']!="":
                    customerstoreref=CustomerStore.objects.filter(StoreName__istartswith=request.session['storeSearch'])
                    searchedfor=request.session['storeSearch']
                    del request.session['storeSearch']
                else:
                    customerstoreref=CustomerStore.objects.all().order_by("-StoreId")
                    searchedfor="Showing featured stores"
                    
                paginator = Paginator(customerstoreref, 12)
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                try:
                    storeref = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    storeref = paginator.page(paginator.num_pages)
                #consumerref=Consumer.objects.get(UserId_id=int(request.session['userid']))
                c=Context({'stores':storeref,'searchedfor':searchedfor,'markets':marketsref})
                return HttpResponse(t.render(c))
            except:
                print sys.exc_info()
                return redirect("/")
        else:
            return redirect("/")
    else:
        try:
            t=get_template('indexpagestores.html')
            marketsref=Market.objects.all()[:10]
            customerstoreref=None
            searchedfor=""
            
            if 'storeSearch' in request.session and request.session['storeSearch']!="":
                customerstoreref=CustomerStore.objects.filter(StoreName__istartswith=request.session['storeSearch'])
                searchedfor=request.session['storeSearch']
                del request.session['storeSearch']
            else:
                customerstoreref=CustomerStore.objects.all().order_by("-StoreId")
                searchedfor="Showing featured stores"
                
            paginator = Paginator(customerstoreref, 12)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                storeref = paginator.page(page)
            except (EmptyPage, InvalidPage):
                storeref = paginator.page(paginator.num_pages)
            c=Context({'stores':storeref,'searchedfor':searchedfor,'markets':marketsref})
            return HttpResponse(t.render(c))
        except:
            print sys.exc_info()
            return redirect("/")





def ProductsSearch(request):
    if 'usertype' in request.session and 'userid' in request.session:
        if request.session['usertype']=="CONSUMER":
            try:
                t=get_template('consumerpageproducts.html')
                marketsref=Market.objects.all()[:10]
#                 consumerref=Consumer.objects.get(UserId_id=int(request.session['userid']))
                pref=None
                searchedfor=""
                
                if 'productSearch' in request.session and request.session['productSearch']!="":
                    pref=Product.objects.filter(ProductDescription__icontains=request.session['productSearch'])
                    searchedfor=request.session['productSearch']
                    del request.session['productSearch']
                 
                print pref 
                    
                if pref.count() == 0:
                    pref=Product.objects.all().order_by("-ProductId")
                    searchedfor="Store not found. Showing featured products"
                    
                paginator = Paginator(pref, 12)
                
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                try:
                    productref = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    productref = paginator.page(paginator.num_pages)
                
                c=Context({'products':productref,'searchedfor':searchedfor,'markets':marketsref})
                return HttpResponse(t.render(c))
            except:
                print sys.exc_info()
                return redirect("/")
        else:
            return redirect("/")
    else:
        try:
            t=get_template('indexpageproducts.html')
            marketsref=Market.objects.all()[:10]
            pref=None
            searchedfor=""
            
            if 'productSearch' in request.session and request.session['productSearch']!="":
                pref=Product.objects.filter(ProductDescription__icontains=request.session['productSearch'])
                searchedfor=request.session['productSearch']
                del request.session['productSearch']
             
            print pref 
                
            if pref.count() == 0:
                pref=Product.objects.all().order_by("-ProductId")
                searchedfor="Store not found. Showing featured products"
                
            paginator = Paginator(pref, 12)
            
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                productref = paginator.page(page)
            except (EmptyPage, InvalidPage):
                productref = paginator.page(paginator.num_pages)
            
            c=Context({'products':productref,'searchedfor':searchedfor,'markets':marketsref})
            return HttpResponse(t.render(c))
        except:
            print sys.exc_info()
            return redirect("/")
                

def StoreSearchOnFourHoursDeliveryPage(request,storeid):
    try:
        if storeid!=None:
            customerstoreref=CustomerStore.objects.get(StoreId=int(storeid))
            productsref=customerstoreref.has_products.all()
            # changes made by amit
            categories = customerstoreref.has_products.values('ProductType').annotate(count=Count('ProductId')).order_by('-count','-ProductId')
            # end
            market=customerstoreref.market_set.get()
            t=get_template('storefront.html')
            c=Context({'store':customerstoreref,'products':productsref,'market':market, 'categories':categories})
            return HttpResponse(t.render(c))
        else:
            return redirect('/store')
    except:
        print sys.exc_info()
        return HttpResponse()
        return redirect('/store')
    
#changes made by amit
def ProductCategoryOnFourHoursDeliveryPage(request, storeid, category):
    try:
        if storeid!=None:
            customerstoreref=CustomerStore.objects.get(StoreId=int(storeid))
            productsref=customerstoreref.has_products.filter(ProductType=str(category))
            categories = customerstoreref.has_products.values('ProductType').annotate(count=Count('ProductId')).order_by('-count','-ProductId')
            market=customerstoreref.market_set.get()
            t=get_template('storefront.html')
            c=Context({'store':customerstoreref,'products':productsref,'market':market, 'categories':categories})
            return HttpResponse(t.render(c))
        else:
            return redirect('/store')
    except:
        print sys.exc_info()
        return HttpResponse()
        return redirect('/store')
#end
    
    
    
    
def ProductSearchOnFourHoursDeliveryPage(request,productid):
    try:
        if productid!=None:
            productref=Product.objects.get(ProductId=productid)
            storeref=productref.customerstore_set.all()
            market=productref.market_set.get()
            #changes made by amit
            categories = storeref[0].has_products.values('ProductType').annotate(count=Count('ProductId')).order_by('-count','-ProductId')
            #end
            t=get_template('product-inner.html')
            c=Context({'store':storeref,'product':productref,'market':market,'categories':categories,'storeid':storeref[0].StoreId})
            return HttpResponse(t.render(c))
        else:
            return redirect('/product')
    except:
        print sys.exc_info()
        return redirect('/product')
    

def LogOut(request):
    logout(request)
    del request.session
    return redirect('/')



def RenderToMarket(request,marketid):
    try:
        marketref=Market.objects.get(MarketId=marketid)
        featuredstores=marketref.has_stores.all().order_by("-CreatedTime")[:30]
        latestproducts=marketref.has_products.all().order_by("-CreatedTime")[:20]
        featuredproducts=marketref.has_products.filter(ProductPrice__gt=1000.00).order_by("-CreatedTime")[:20]
        t=get_template('markethome.html')
        c=Context({'market':marketref,'latestproducts':latestproducts,'featuredproducts':featuredproducts,'featuredstores':featuredstores})
        return HttpResponse(t.render(c))
    except:
        return redirect('/')




# def StoreURI(request,marketname,storename):
#     try:
#         productsref=None
#         customerstoreref=CustomerStore.objects.filter(ReferenceName=storename)[:1]
#         for i in customerstoreref:
#             productsref=i.has_products.all()
#         t=get_template('storefront.html')
#         c=Context({'store': i,'products':productsref})
#         return HttpResponse(t.render(c))
#     except:
#         print sys.exc_info()
#         return redirect('/')




def Categories(request,marketid,categoryid):
    if marketid!=None:
        subcategories=[]
        marketref=Market.objects.get(MarketId=marketid)
        market_has_stores=marketref.has_stores.all()
        storecategoryref=StoreCategory.objects.get(StoreCategoryId=categoryid)
        storesubcatref=SubCategory.objects.filter(StoreCategoryType=storecategoryref)
        dic={}
        for subcat in storesubcatref:
            subcatlist=[]
            for store in market_has_stores:
                if subcat in store.has_subcategories.all():
                    subcatlist.append(store) 
            dic[subcat.SubCategoryName]=subcatlist
        for subcategory in storesubcatref:
            subcategories.append(subcategory.SubCategoryName)
            
        return render_to_response('categories.html',{'market':marketref,'category':storecategoryref.StoreCategoryName,'subcategories':dic})
    else:
        return redirect('/')
    
    
    
def Search(request):
    if request.GET['search']!="" and request.GET['category_id']!="":
        try:
            
            if request.GET['category_id']=="Searchstore":
                storequeryset=CustomerStore.objects.filter(StoreName__icontains=request.GET['search'])[:10]
                return render_to_response('searchpage.html',{'stores':storequeryset,'searchquery':request.GET['search']})
            
            if request.GET['category_id']=="Searchproduct":
                productqueryset=Product.objects.filter(ProductDescription__icontains=request.GET['search'])[:10]
                return render_to_response('searchpage.html',{'products':productqueryset,'searchquery':request.GET['search']})
        except:
            print sys.exc_info()
                
        return redirect('/store')
    else:
        return redirect_to(request,'/') 
    
     


def ChangePassword(request):
    if 'usertype' in request.session and 'userid' in request.session:
        old=request.POST['oldpwd']
        new = request.POST['newpwd']
        conform = request.POST['conpwd']
                
        if new == conform:
            user=User.objects.get(id=request.session['userid'])
            is_password = user.check_password(old)
            if is_password==True:
                user.set_password(conform)
                user.save()
                return HttpResponse("Password Changed successfully")
            else:
                return HttpResponse("Invalid Password please enter the correct password.")
        else:
            return HttpResponse("Password and Confirm password doesn't matched")
    else:
        return HttpResponse("Session Expired")
    


def LostPassword(request):
    t=get_template('forgotpassword.html')
    c=Context({'forgotpasswordform':'forgotpasswordform','header':'Forgot password??? Dont worry.. we will send you the new one'})
    return HttpResponse(t.render(c))




def CustomerShowChangePassword(request):
    if 'usertype' in request.session and 'userid' in request.session:
        if request.session['usertype']=="CUSTOMER":
            storeref=CustomerStore.objects.get(CustomerUserId=request.session['userid'])
            t=get_template('customer_changepassword.html')
            c=Context({'customerchangepassword':'customerchangepassword','storeref':storeref})
            return HttpResponse(t.render(c))
        else:
            return redirect('/')
    return redirect('/customerhome')



def MarketAdminShowChangePassword(request):
    if 'usertype' in request.session and 'userid' in request.session:
        if request.session['usertype']=="MARKET_ADMIN":
            marketref=Market.objects.get(UserId=request.session['userid'])
            t=get_template('marketadmin_changepassword.html')
            c=Context({'marketadminchangepassword':'marketadminchangepassword','marketref':marketref})
            return HttpResponse(t.render(c))
        else:
            return redirect('/')
    return redirect('/')



def SendPassword(request):
    print request.POST
    t=get_template('forgotpassword.html')
    try:
        if 'fusername' in request.POST and request.POST!=None:
            userobj=User.objects.get(username__exact=request.POST['fusername'])
            emailid=userobj.email
            chars = string.letters + string.digits
            newpassword=''
            for i in range(8):
                newpassword = newpassword + choice(chars)
            userobj.set_password(newpassword)
            mail_thread=sendMail(emailid,newpassword)
            mail_thread.start()
            userobj.save()
            c=Context({'forgotpasswordmessage':'A new password has been send to your Email-ID','header':'New password send'})
            return HttpResponse(t.render(c))
        else:
            c=Context({'forgotpasswordmessage':"please provide username",'header':'you missed a field'})
            return HttpResponse(t.render(c))
    except:
        print sys.exc_info()
        c=Context({'forgotpasswordmessage':"Invalid username",'header':'Invalid username'})
        return HttpResponse(t.render(c))



class sendMail(threading.Thread):
    def __init__(self, emailid,password):
        threading.Thread.__init__(self)
        self.emailid=emailid
        self.password=password
        
    def run(self):
        try:
            t1=time.time()
            t = get_template('mailingtemplate.html')
            html = t.render(Context({'password':self.password}))    
            msg = EmailMultiAlternatives("eShop: Password for your account","", EMAIL_HOST_USER,[self.emailid])
            msg.attach_alternative(html, "text/html")
            msg.send()
            print "email send to:"+str(self.emailid)+" Time taken:"+str(time.time()-t1)
        except:
            print "Error in sending mail."+str(sys.exc_info())
            pass
        
        
def ConsumerShowChangePassword(request):
    if 'usertype' in request.session and 'userid' in request.session:
        if request.session['usertype']=="CONSUMER" and request.session['userid'] != "":
            t=get_template('consumer_changepassword.html')
            #consumer = Consumer.objects.select_related().get(UserId_id=int(request.session['userid']))
            c=Context({'consumerchangepassword':'consumerchangepassword'})
            return HttpResponse(t.render(c))
        else:
            return redirect('/')
    else:
        return redirect('/')