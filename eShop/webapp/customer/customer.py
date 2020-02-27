from django.template.loader import get_template
from django.template.context import Context
from django.conf import settings
import sys
from eShop.webapp.models import Product, StoreCategory, MapUserTypeWithUser,ServicePack, Market, CustomerStore, UserType,\
    DeliveryOptions, SubCategory, Token
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,InvalidPage


def ShowLoginPage(request):
    t=get_template('login.html')
    c=Context({})
    return HttpResponse(t.render(c))


'''Customer Registering his store to the market'''

def CustomerStoreRegistrationForm1(request):
    t=get_template('customer_registration.html')
    markets=Market.objects.all()
    
    categories={}
    refstorecat=StoreCategory.objects.all()
    
    for i in refstorecat:
        refsub=SubCategory.objects.filter(StoreCategoryType=i.StoreCategoryId)
        categories[i.StoreCategoryName]=refsub
    c=Context({'customer_regform1':'customer_regform1','markets':markets,'categories':categories})
    return HttpResponse(t.render(c))




@csrf_exempt
def CustomerStoreRegistrationForm2(request):
    t=get_template('customer_registration.html')
    
    for i in request.POST.getlist('storecategories'):
        request.session[i]=i
    
    request.session['salesrepid']=request.POST.get('salesrepid')
    request.session['marketid']=request.POST.get('marketlist')
    request.session['storename']=request.POST.get('storename')
    request.session['streetaddr']=request.POST.get('streetaddr')
    request.session['city']=request.POST.get('city')
    request.session['postalcode']=request.POST.get('postalcode')
    request.session['country']=request.POST.get('country')
    request.session['state']=request.POST.get('state')
    request.session['mainphonenumber']=request.POST.get('mainphonenumber')
    request.session['website']=request.POST.get('website')
    request.session['contactperson']=request.POST.get('contactperson')
    
    marketref=Market.objects.get(MarketId=int(request.session['marketid']))
    marketservicepacks=marketref.has_servicepacks.all()
    c=Context({'customer_regform2':'customer_regform2','marketservicepacks':marketservicepacks})
    return HttpResponse(t.render(c))



def CustomerStoreRegistration(request):
    try:
        is_user_exists=User.objects.filter(username=request.POST.get('username')).exists()
        storecategoryref=None
        servicepackref=None
        print is_user_exists
        if is_user_exists==False:
            try:
                marketref=Market.objects.get(MarketId=int(request.session['marketid']))    
                servicepackref=ServicePack.objects.get(ServicePackId=int(request.POST.get('searchbyservicepack')))
            except:
                print sys.exc_info()
                return render_to_response('customer_registration.html',{'message':'Market or Service pack not provided','title':'Store Registration','heading':'Store Registration'})      
            
            userref=User.objects.create_user(username=request.POST.get('username'),email=request.POST.get('username'),password=request.POST.get('pwd'))    
            usertype=UserType.objects.get(UserTypeName="CUSTOMER")
            mapins=MapUserTypeWithUser()
            mapins.UserTypeId=usertype
            mapins.UserId=userref
            mapins.save()
            store=CustomerStore(StoreName=request.session['storename'],
                                 StreetAddress=request.session['streetaddr'],
                                 City=request.session['city'],
                                 PostalCode=request.session['postalcode'],
                                 Country=request.session['country'],
                                 State=request.session['state'],
                                 MainPhoneNumber=request.session['mainphonenumber'],
                                 ContactPerson=request.session['contactperson'],                          
                                 EmailAddress=request.POST.get('username'), 
                                 Website=request.session['website'],
                                 SalesRepId=request.session['salesrepid'],
                                 HoursOfOperation=request.POST.get('hoursofservice'),CreatedTime=datetime.datetime.now())     
            store.StoreCategory=storecategoryref
            store.ServicePack=servicepackref            
            store.CustomerUserId=userref
            
              
            try:
                ref=request.FILES['bannerimage'].name
                ref=ref.replace(" ","")    
                path=settings.MEDIA_ROOT                     
                image_name=str(userref.pk)+'_'+request.session['storename']+ref
                repath=path+'/'+image_name
                if handle_uploaded_file(request.FILES['bannerimage'],repath):
                    store.BannerImages=image_name  
            except:
                print sys.exc_info()
    
            try:
                ref=request.FILES['storelogo'].name
                ref=ref.replace(" ","")  
                path=settings.MEDIA_ROOT                     
                image_name=str(userref.pk)+'_'+request.session['storename']+ref
                repath=path+'/'+image_name
                if handle_uploaded_file(request.FILES['storelogo'],repath):
                    store.StoreLogo=image_name   
            except:
                print sys.exc_info()
                
            store.save()    
            token=Token(usertoken="")
            token.UserId=userref
            token.save()
            
            subcategories=SubCategory.objects.all()
            for i in subcategories:
                if i.SubCategoryName in request.session:
                    print i.SubCategoryName
                    store.has_subcategories.add(i)
                    store.save()
            marketref.has_stores.add(store)
            marketref.save()
            return render_to_response('customer_registration.html',{'message':request.session['storename']+' store created','title':'Store Registration','heading':'Store Registration'})
        else:
            del request.session
            return render_to_response('customer_registration.html',{'customer_regform2':'customer_regform2','message':'Username already exists'})
    except:
        print sys.exc_info()
        del request.session
        return render_to_response('customer_registration.html',{'message':'Store not created','title':'Store Registration','heading':'Store Registration'})    
    
    
    
    
   
# def MarketSearch(request):
#     try:
#         marketobj=Market.objects.filter(MarketName__istartswith=request.GET['term'])[:10]
#         list1=[]    
#         if marketobj is not None:
#             for market in marketobj:
#                 list1.append(market.MarketName)
#         return HttpResponse(json.dumps(list1))
#     except:
#         print "Exception: MarketSearch. "+sys.exc_info()
#         return HttpResponse()
  
  
    
# def ServicePackSearch(request):
#     try:
#         servicepackobj=ServicePack.objects.filter(ServicePackName__istartswith=request.GET['term'])
#         list1=[]    
#         if servicepackobj is not None:
#             for servicepack in servicepackobj:
#                 list1.append(servicepack.ServicePackName)
#         return HttpResponse(json.dumps(list1))
#     except:
#         print sys.exc_info()
#         return HttpResponse()


    
def CheckEmailAddress(request):
    try:
        if request.GET['username']=="":
            return HttpResponse('not ok')
        else:
            emailaddr=User.objects.filter(username=request.GET['username']).exists()
            if emailaddr==False:
                return HttpResponse('ok')
            else:
                return HttpResponse('not ok')
    except :
        print sys.exc_info()
        return HttpResponse('not ok')
        
    
    
    
def CustomerHome(request):
        if request.session['usertype']=="CUSTOMER":
            try:
                t=get_template('user_index.html')
                cusinfo=CustomerStore.objects.get(CustomerUserId=request.session['userid'])
                products=cusinfo.has_products.all()
                
                paginator = Paginator(products, 10)
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                try:
                    products = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    products = paginator.page(paginator.num_pages)
                
                      
                c=Context({'home':'home','products':products,'bannerpic':cusinfo.BannerImages,'cusinfo':cusinfo})
                return HttpResponse(t.render(c))
            except:
                print sys.exc_info()
        else:
            del request.session
            return redirect("/")    

 
 
 

def EditProfile(request):
    if 'storeid' in request.session and request.session['storeid']!="":
        t=get_template('user_index.html')
        cusinfo=CustomerStore.objects.select_related().get(CustomerUserId__id=int(request.session['userid']))
        c=Context({'editprofile':'editprofile','cusinfo':cusinfo})
        return HttpResponse(t.render(c))
    else:
        return redirect("/") 
   



def UpdateProfile(request):
    if 'usertype' in request.session and 'storeid' in request.session: 
        if request.session['usertype']=="CUSTOMER" and request.session['storeid']!="":
            userref=request.session['storeid']
            cusinfo=CustomerStore.objects.select_related().get(StoreId=int(request.session['storeid']))
            cusinfo.StoreName=request.POST['storename']
            cusinfo.StreetAddress=request.POST['streetaddress']
            cusinfo.City=request.POST['city']
            cusinfo.PostalCode=request.POST['postalcode']
            #cusinfo.Country=request.POST['country']
            #cusinfo.State=request.POST['state']
            cusinfo.MainPhoneNumber=request.POST['phonenumber']
            cusinfo.EmailAddress=request.POST['emailAddress']
            cusinfo.Website=request.POST['website']
            cusinfo.HoursOfOperation=request.POST['hoursofoperation']
            
            try:
                if 'bannerimage' in request.FILES and request.FILES['bannerimage']!=None:  
                    ref=request.FILES['bannerimage'].name
                    ref=ref.replace(" ","")    
                    path=settings.MEDIA_ROOT                     
                    image_name=str(userref.pk)+'_'+request.POST['storename']+ref
                    repath=path+'/'+image_name
                    if handle_uploaded_file(request.FILES['bannerimage'],repath):
                        cusinfo.BannerImages=image_name  
                              
                if 'StoreLogo' in request.FILES and request.FILES['storelogo']!=None:  
                    ref=request.FILES['storelogo'].name
                    ref=ref.replace(" ","")  
                    path=settings.MEDIA_ROOT                     
                    image_name=str(userref.pk)+'_'+request.POST['storename']+ref
                    repath=path+'/'+image_name
                    if handle_uploaded_file(request.FILES['StoreLogo'],repath):
                        cusinfo.StoreLogo=image_name   
            except:
                print sys.exc_info()

            User.objects.filter(id=cusinfo.CustomerUserId.id).update(email=request.POST['emailAddress'])    
            cusinfo.save()
            return render_to_response('user_index.html',{'editprofile':'editprofile','message':'Updated Successfully','cusinfo':cusinfo})
        else:
            return redirect('/')
    else:
        return redirect('/')
    
    
    
   
   
   
def ViewProfile(request):
    if 'usertype' in request.session and 'storeid' in request.session:
        if request.session['usertype']=="CUSTOMER" and request.session['storeid']!="":
            t=get_template('user_index.html')
            cusinfo=CustomerStore.objects.select_related().get(CustomerUserId__id=int(request.session['userid']))
            storecategories=StoreCategory.objects.all()
        
            storesubcategories=cusinfo.has_subcategories.all()
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
    
            servicepack_for_customer=cusinfo.ServicePack
            services_for_customer=cusinfo.ServicePack.has_services.all()
            c=Context({'viewprofile':'viewprofile','cusinfo':cusinfo,'dic':dic,'servicepacks':servicepack_for_customer,'services':services_for_customer})
            return HttpResponse(t.render(c))
        else:
            return redirect('/')
    else:
        redirect('/')
   



   

def AddProduct(request):
    t=get_template('user_index.html')
    #category=ProductCategory.objects.all();
    cusinfo=CustomerStore.objects.select_related().get(CustomerUserId__id=int(request.session['userid']))
    deliveryoptions=DeliveryOptions.objects.all()
    c=Context({'addproduct':'addproduct','deliveryoptions':deliveryoptions,'cusinfo':cusinfo})
    #c=Context({'addproduct':'addproduct','productcategory':category,'deliveryoptions':deliveryoptions})
    return HttpResponse(t.render(c))
    




def UploadProduct(request):
    if 'usertype' in request.session and 'storeid' in request.session:
        if request.session['usertype']=="CUSTOMER" and request.session['storeid']!="":
            t=get_template('user_index.html')
            cusinfo=CustomerStore.objects.select_related().get(CustomerUserId__id=int(request.session['userid']))
            deliveryoptions=DeliveryOptions.objects.all()
            if request.method=='POST':
                if 'productimage' in request.FILES and request.FILES['productimage']:
                    try:
                        productimagename=request.FILES['productimage'].name
                        productimagename=productimagename.replace(" ","")
                        productref=Product(ProductDescription=request.POST['description'],Quantity=int(request.POST['quantity']),ProductPrice=request.POST['amount'],ProductType=request.POST['productcategory'],CreatedTime=datetime.datetime.now())
                        productref.ProductImage=productimagename
                        pathofimage=settings.MEDIA_ROOT+'/'+productimagename
                        
                        if handle_uploaded_file(request.FILES['productimage'],pathofimage):
                            productref.save()
                            
                            deliveryref=DeliveryOptions.objects.all()
                            
                            for deliverytype in deliveryref:
                                if deliverytype.DeliveryTypeName in request.POST:
                                    option=DeliveryOptions.objects.get(DeliveryTypeName=deliverytype.DeliveryTypeName)
                                    productref.has_deliveryoptions.add(option)
                                    
                            customerstoreref=CustomerStore.objects.get(StoreId=request.session['storeid'])
                            customerstoreref.ProductsUploaded+=1
                            
                            market=customerstoreref.market_set.get()
                            market.has_products.add(productref) 
                            
                            customerstoreref.save()
                            customerstoreref.has_products.add(productref)
                            
                            c=Context({'addproduct':'addproduct','message':'Product uploaded','deliveryoptions':deliveryoptions,'cusinfo':cusinfo})
                            return HttpResponse(t.render(c))
                        else:
                            c=Context({'addproduct':'addproduct','message':'Image not uploaded','deliveryoptions':deliveryoptions,'cusinfo':cusinfo})
                            return HttpResponse(t.render(c))
                    except:
                        print sys.exc_info()
                        c=Context({'addproduct':'addproduct','message':'Error!!!','deliveryoptions':deliveryoptions,'cusinfo':cusinfo})
                        return HttpResponse(t.render(c))
                    else:
                        c=Context({'addproduct':'addproduct','message':'Image not uploaded or image type is not jpeg','deliveryoptions':deliveryoptions,'cusinfo':cusinfo})
                        return HttpResponse(t.render(c))
            else:
                c=Context({'addproduct':'addproduct','message':'Method not allowed','deliveryoptions':deliveryoptions,'cusinfo':cusinfo})
                return HttpResponse(t.render(c))
        else:
            return redirect("/")
    else:
        return redirect("/")  







def EditProduct(request):
    if request.session['usertype']=="CUSTOMER" and request.session['storeid']!="":
        t=get_template('user_index.html')
        cusinfo=CustomerStore.objects.select_related().get(CustomerUserId__id=int(request.session['userid']))
        productinfo=Product.objects.get(ProductId=int(request.GET['productid']))
        c=Context({'editproduct':'editproduct','productinfo':productinfo,'cusinfo':cusinfo})
        return HttpResponse(t.render(c))
    else:
        return redirect("/") 



    
def UpdateProduct(request):
    if 'usertype' in request.session and 'storeid' in request.session:
        if request.session['usertype']=="CUSTOMER" and request.session['storeid']!="":
            message=""
            cusinfo=CustomerStore.objects.select_related().get(CustomerUserId__id=int(request.session['userid']))
            productinfo=Product.objects.get(ProductId=int(request.POST['productid']))
            productinfo.ProductDescription=request.POST['productdescription']
            productinfo.ProductPrice=request.POST['amount']
            productinfo.ProductType=request.POST['productcategory'] 
            productinfo.Quantity=request.POST['quantity'] 
            try:
                if request.FILES['productimage']!=None:  
                    ref=request.FILES['productimage'].name
                    ref=ref.replace(" ","")    
                    path=settings.MEDIA_ROOT                     
                    image_name=request.POST['productid']+'_'+ref
                    repath=path+'/'+image_name
                    if handle_uploaded_file(request.FILES['productimage'],repath):
                        productinfo.ProductImage=image_name  
            except:
                print sys.exc_info()
                message="Error in  Product upload"
                 
            productinfo.save()
            message="Product Updated successfully"
            return render_to_response('user_index.html',{'editproduct':'editproduct','productinfo':productinfo,'message':message,'cusinfo':cusinfo})
        else:
            return redirect('/')
    else:
        return redirect('/')
    





def DeleteProduct(request):
    if request.session['usertype']=="CUSTOMER":
        Product.objects.filter(ProductId=int(request.GET['productid'])).delete()
        return HttpResponse("Product Deleted")
    else:
        return redirect("/") 





def handle_uploaded_file(upfile,path):
    try:
        dest = open(path, 'wb+')
        dest.write(upfile.read())
        dest.close()
        return True
    except:
        return False   