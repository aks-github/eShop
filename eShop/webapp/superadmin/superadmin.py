from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from eShop.webapp.models import Service, ServicePack,Market,\
    SalesReference, ServiceType, UserType, MapUserTypeWithUser,SMS, Email, ProductShowCase, Advertising
import sys
from django.template.loader import get_template
from django.template.context import Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage,InvalidPage
import datetime
from django.conf import settings
from eShop.webapp.customer.customer import handle_uploaded_file


def CheckMarket(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        market=request.GET['marketname']
        market=Market.objects.filter(MarketName__exact=market).exists()
        if market==False:
            return HttpResponse('ok')
        else:
            return HttpResponse('not ok')
    else:
        return redirect("/")
      
      
        
        
def CheckUserName(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            user=User.objects.filter(username=request.GET['username']).exists()
            print user
            if user==False:
                return HttpResponse('ok')
            else:
                return HttpResponse('not ok')
        except :
            print sys.exc_info()
            return HttpResponse('')
    else:
        return redirect("/")   





def Markets(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        markets_list = Market.objects.select_related().all()
        paginator = Paginator(markets_list, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            markets = paginator.page(page)
        except (EmptyPage, InvalidPage):
            markets = paginator.page(paginator.num_pages)
        return render_to_response('superadmin_market.html', {"showmarket": markets})
    else:
        return redirect("/")



def MarketRegistrationForm(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_market.html')
        c=Context({'stepone':'stepone'})
        return HttpResponse(t.render(c))
    else:
        return redirect("/")


@csrf_exempt
def MarketAdminRegistrationForm(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_market.html')
        
        request.session['MarketName']=request.POST.get('mname')
        request.session['MarketAddress']=request.POST.get('maddr')
        request.session['MarketDescription']=request.POST.get('mdesc')
        request.session['ContactPerson']=request.POST.get('contactname')
        request.session['ContactPhoneNumber']=request.POST.get('contactno')
        request.session['ContactEmailAddress']=request.POST.get('contactemail')
        request.session['MarketWebsite']=request.POST.get('mwebsite')
        
        c=Context({'steptwo':'steptwo'})
        return HttpResponse(t.render(c))
    else:
        return redirect("/")




@csrf_exempt
def MarketAdminCredentials(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            market=Market.objects.filter(MarketName= request.session['MarketName']).exists()
            if market==True:
                return render_to_response('superadmin_market.html',{'message':'Market did not specified or do exist'})
            else:
                mapref=MapUserTypeWithUser()
                usertyperef=UserType.objects.get(UserTypeName="MARKET_ADMIN")
                marketref=Market(MarketName=request.session['MarketName'],MarketAddress=request.session['MarketAddress'],MarketDescription=request.session['MarketDescription'],ContactPerson=request.session['ContactPerson'],ContactPhoneNumber=request.session['ContactPhoneNumber'],ContactEmailAddress=request.session['ContactEmailAddress'],MarketWebsite=request.session['MarketWebsite'],CreatedTime=datetime.datetime.now())
                u=User.objects.create_user(username=request.POST['uname'],email=request.session['ContactEmailAddress'],password=request.POST['pwd'])
                mapref.UserTypeId=usertyperef
                mapref.UserId=u
                marketref.UserId=u
                
                try:
                    if request.FILES['marketimage']!=None:   
                        ref=request.FILES['marketimage'].name
                        ref=ref.replace(" ","")    
                        path=settings.MEDIA_ROOT                     
                        image_name=request.session['MarketName']+ '_' +ref
                        repath=path+'/'+image_name
                        if handle_uploaded_file(request.FILES['marketimage'],repath):
                            marketref.MarketImage=image_name        
                            
                    if request.FILES['marketlogo']!=None:
                        ref=request.FILES['marketlogo'].name
                        ref=ref.replace(" ","")  
                        path=settings.MEDIA_ROOT                     
                        image_name=request.session['MarketName']+ '_'+ref
                        repath=path+'/'+image_name
                        if handle_uploaded_file(request.FILES['marketlogo'],repath):
                            marketref.MarketLogo=image_name   
                except:
                    print sys.exc_info()
                    
                marketref.save()
                mapref.save()       
            return render_to_response('superadmin_market.html',{'message':request.session['MarketName']+' Market created'})
        except:
            print sys.exc_info()
            return render_to_response('superadmin_market.html',{'message':'Error'})
    else:
        return redirect("/")



def EditMarket(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'marketid' in request.GET:
            try:
                marketinfo=Market.objects.get(MarketId=int(request.GET['marketid']))
                return render_to_response('superadmin_market.html',{'marketinfo':marketinfo,'editmarketprofile':'editmarketprofile'})
            except:
                print sys.exc_info()
                return render_to_response('superadmin_market.html',{'message':'Error Occured'})
        else:
            return render_to_response('superadmin_market.html',{'message':'Method not allowed'})
    else:
        return redirect("/")  
      
      
    
def  UpdateMarket(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            marketinfo=Market.objects.get(MarketId=int(request.POST['marketid']))
            marketinfo.MarketName=request.POST['mname']
            marketinfo.MarketAddress=request.POST['maddr']
            marketinfo.MarketDescription=request.POST['mdesc']
            marketinfo.ContactPerson=request.POST['contactname']
            marketinfo.ContactPhoneNumber=request.POST['contactno']
            marketinfo.ContactEmailAddress=request.POST['contactemail']
            marketinfo.MarketWebsite=request.POST['mwebsite']
            marketinfo.save()
            User.objects.filter(id=marketinfo.UserId.id).update(email=request.POST['contactemail'])
            return render_to_response('superadmin_market.html',{'message':'market Updated successfully'})
        except:
            print sys.exc_info()
    else:
        return redirect("/")  
        


 

def ShowSalesRef(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        salesref_list = SalesReference.objects.select_related().all()
        paginator = Paginator(salesref_list, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            salesref = paginator.page(page)
        except (EmptyPage, InvalidPage):
            salesref = paginator.page(paginator.num_pages)
        return render_to_response('superadmin_sales.html', {"showsalesref": salesref})
    return redirect("/")



def CheckSalesRef(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            salesrefid=SalesReference.objects.filter(SalesRepresentativeId=request.GET['salesrepid']).exists()
            if salesrefid==False:
                return HttpResponse('ok')
            else:
                return HttpResponse('not ok')
        except :
            print sys.exc_info()
            return HttpResponse('not ok')
    else:
        return redirect("/")
    
       

def SalesRefRegistrationForm(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_sales.html')
        c=Context({'salesrefreg':'salesrefreg'})
        return HttpResponse(t.render(c))     
    return redirect("/")
 
 
 
def SalesRefRegistration(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            SalesReference.objects.get(SalesRepresentativeId=request.POST['salesrepid'])
            return HttpResponse("Sales Representative with given name already present.")
        except:
            print sys.exc_info()
            SalesReference(SalesRepresentativeId=request.POST['salesrepid'],SalesRepresentativeName=request.POST['salesrepname'],CreatedTime=datetime.datetime.now()).save()
            return HttpResponse("Sales Representative Information saved.")
    return redirect("/")


def EditSalesRepId(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'salesrepid' in request.GET:
            try:
                print request.GET['salesrepid']
                salesrepidinfo=SalesReference.objects.get(SalesRepresentativeId=request.GET['salesrepid'])
                print salesrepidinfo.SalesRepresentativeName
                return render_to_response('superadmin_sales.html',{'salesrepidinfo':salesrepidinfo,'editsalesrepid':'editsalesrepid'})
            except:
                print sys.exc_info()
                return render_to_response('superadmin_sales.html',{'message':'Error Occured'})
        else:
            return render_to_response('superadmin_sales.html',{'message':'Method not allowed'})
    else:
        return redirect("/")  
      
    
    
def  UpdateSalesRepId(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        salesrepidinfo=SalesReference.objects.get(SalesRepresentativeId=request.POST['salesrepid'])
        #salesrepidinfo.SalesRepresentativeId=request.POST['salesrepid']
        salesrepidinfo.SalesRepresentativeName=request.POST['salesrepname']
        salesrepidinfo.save()
        return render_to_response('superadmin_sales.html',{'message':'Sales Representative information  Updated successfully'})
    else:
        return redirect("/")




def DeleteSalesrepid(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'salesrepid' in request.GET:
            try:
                print request.GET['salesrepid']
                SalesReference.objects.filter(SalesRepresentativeId=request.GET['salesrepid']).delete()
                return HttpResponse("ok")
            except:
                
                return HttpResponse("Error in salesrepid deletion")
        else:
            return HttpResponse("Method Not allowed")
    else:
        return redirect("/")



#######################################################################


def ShowServices(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_service.html')
        services=Service.objects.filter(IsDeleted=False)
        
        paginator = Paginator(services, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            services = paginator.page(page)
        except (EmptyPage, InvalidPage):
            services = paginator.page(paginator.num_pages)
        
        c=Context({'services':services})
        return HttpResponse(t.render(c))
    else:
        return redirect("/")





def AddServiceForm(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        servicetypes=ServiceType.objects.all()
        return render_to_response('superadmin_service.html',{'addservice':'addservice','servicetypes':servicetypes})
    else:
        return redirect("/")




@csrf_exempt
def CreateService(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if request.method=='POST' and 'servicetypename' in request.POST:
            try:
                service=Service.objects.filter(ServiceName=request.POST['servicename']).exists()
                if service==False:
                    service=Service(ServiceName=request.POST['servicename'],Description=request.POST['servicedescription'],StartDate=request.POST['startdate'],EndDate=request.POST['enddate'],Rate=request.POST['rate'],Discount=request.POST['discount'],CreatedTime=datetime.datetime.now(),IsDeleted=False)
                    servicetype=ServiceType.objects.get(ServiceTypeName=request.POST['servicetypename'])
                    service.ServiceTypeId=servicetype
                    service.save()
                    
                    if 'servicetypename' in request.POST and request.POST['servicetypename']!="":    
                        if request.POST['servicetypename']=='SMS':
                            sms=SMS(NumberOfSMS=request.POST['servicenumbers'])
                            sms.ServiceId=service
                            sms.save()
                    
                        if request.POST['servicetypename']=='EMAIL':
                            email=Email(NumberOfEmails=request.POST['servicenumbers'])
                            email.ServiceId=service
                            email.save()
                    
                        if request.POST['servicetypename']=='PRODUCTSHOWCASE':
                            productshowcase=ProductShowCase(NumberOfProductsAllowedToUpload=request.POST['servicenumbers'])
                            productshowcase.ServiceId=service
                            productshowcase.save()
                    
                        if request.POST['servicetypename']=='ADVERTISE':
                            advertising=Advertising(NumberOfAdvetisement=request.POST['servicenumbers'])
                            advertising.ServiceId=service
                            advertising.save()
                    return HttpResponse("Service Added")
                else:
                    return HttpResponse("Service Name Already exist")
                
            except:
                print sys.exc_info()
                return HttpResponse("Service Not Added")
        else:
            return HttpResponse("Method not supported")
    else:
        return redirect("/")
    
    



def CheckService(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            s=Service.objects.filter(ServiceName=request.GET['servicename']).exists()
            if s==False:
                return HttpResponse('ok')
            else:
                return HttpResponse('not ok')
        except :
            print sys.exc_info()
            return HttpResponse('ok')
    else:
        return redirect("/")
    
       
        
def UpdateService(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'serviceid' in request.POST:
            serviceinfo=Service.objects.get(ServiceId=int(request.POST['serviceid']))
            serviceinfo.ServiceName=request.POST['servicename']
            serviceinfo.Description=request.POST['servicedesc']
            serviceinfo.EndDate=request.POST['enddate']
            serviceinfo.Rate=request.POST['rate']
            serviceinfo.Discount=request.POST['discount']
            serviceinfo.save()
            return render_to_response('superadmin_service.html',{'message':'Service Updated successfully'})
        else:
            return render_to_response('superadmin_service.html',{'message':'Method not allowed'})
    else:
        return redirect("/")


    
def EditService(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'serviceid' in request.GET:
            try:
                print request.GET['serviceid']
                serviceinfo=Service.objects.get(ServiceId=int(request.GET['serviceid']))
                print serviceinfo.ServiceName
                return render_to_response('superadmin_service.html',{'serviceinfo':serviceinfo,'editservice':'editservice'})
            except:
                print sys.exc_info()
                return render_to_response('superadmin_service.html',{'message':'Error Occured'})
        else:
            return render_to_response('superadmin_service.html',{'message':'Method not allowed'})
    else:
        return redirect("/")  
      
    
def DeleteService(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'serviceid' in request.GET:
            try:
                print request.GET['serviceid']
                Service.objects.filter(ServiceId=int(request.GET['serviceid'])).update(IsDeleted=True)
                return HttpResponse("ok")
            except:
                return HttpResponse("Error in service deletion")
        else:
            return HttpResponse("Method Not allowed")
    else:
        return redirect("/")



############################################################################################


def ShowServicePacks(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_servicepack.html')
        servicepacks=ServicePack.objects.filter(IsDeleted=False)
        
        paginator = Paginator(servicepacks, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            servicepacks = paginator.page(page)
        except (EmptyPage, InvalidPage):
            servicepacks = paginator.page(paginator.num_pages)
        
        c=Context({'servicepacks':servicepacks})
        return HttpResponse(t.render(c))
    else:
        return redirect("/")


def AddServicePackForm(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        services=Service.objects.filter(IsDeleted=False)
        return render_to_response('superadmin_servicepack.html',{'addservicepack':'addservicepack','services':services})
    else:
        return redirect("/")


def CreateServicePack(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            service=Service.objects.filter(IsDeleted=False)
            servicepack=ServicePack(ServicePackName=request.POST['servicepackname'],ServicePackDescription=request.POST['servicepackdescription'],ExpiryDate=request.POST['expirydate'],Price=request.POST['price'],Discount=request.POST['discount'],CreatedTime=datetime.datetime.now(),IsDeleted=False)
            servicepack.save()
            for i in service:
                if i.ServiceName in request.POST:
                    print i.ServiceName
                    servicename=Service.objects.get(ServiceName=i.ServiceName)
                    servicepack.has_services.add(servicename)
                    servicepack.save()
            return HttpResponse("Service pack created successfully")
        except:
            print sys.exc_info()
            return HttpResponse("Service pack Creation failed")
    else:
        return redirect("/")
    
    
        

def CheckServicePack(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            s=ServicePack.objects.filter(ServicePackName=request.GET['servicepackname']).exists()
            if s==False:
                return HttpResponse('ok')
            else:
                return HttpResponse('not ok')
        except :
            print sys.exc_info()
            return HttpResponse('ok')
    else:
        return redirect("/")



def EditServicePack(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'servicepackid' in request.GET:
            try:
                #print request.GET['servicepackid']
                servicepackinfo=ServicePack.objects.get(ServicePackId=int(request.GET['servicepackid']))
                currentservicesinpack=servicepackinfo.has_services.all()
                allservices=Service.objects.all()
                newservices=[]       
                for service in allservices:
                    if service in currentservicesinpack:
                        continue
                    newservices.append(service)
                return render_to_response('superadmin_servicepack.html',{'servicepackinfo':servicepackinfo,'services':currentservicesinpack,'additionalservices':newservices,'editservicepack':'editservicepack'})
            except:
                print sys.exc_info()
                return render_to_response('superadmin_servicepack.html',{'message':'Error Occured'})
        else:
            return render_to_response('superadmin_servicepack.html',{'message':'Method not allowed'})
    else:
        return redirect("/")  
      
      
      
    
def UpdateServicePack(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            servicepackid=request.POST['servicepackid']
            ajaxcheckbox=request.POST['checkobj'].split(",")
            servicepackinfo=ServicePack.objects.get(ServicePackId=servicepackid)
            
            services=servicepackinfo.has_services.all()
            
            servicepackinfo.ServicePackName=request.POST['servicepackname']  
            servicepackinfo.ServicePackDescription=request.POST['servicepackdescription']
            servicepackinfo.ExpiryDate=request.POST['expirydate']
            servicepackinfo.Rate=request.POST['price']
            servicepackinfo.Discount=request.POST['discount']     
            servicepackinfo.save() 
            
            
            
            for i in services:
                service=Service.objects.get(ServiceName=i.ServiceName)
                print service.ServiceName
                servicepackinfo.has_services.remove(service)
            
            for i in ajaxcheckbox:
                service=Service.objects.get(ServiceName=i)
                print service
                servicepackinfo.has_services.add(service)
            return render_to_response('superadmin_servicepack.html',{'message':'ServicePack Updated successfully'})
        except:
            print sys.exc_info()
    else:
        return redirect("/") 



def DeleteServicePack(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        if 'servicepackid' in request.GET:
            try:
                print request.GET['servicepackid']
                ServicePack.objects.filter(ServicePackId=int(request.GET['servicepackid'])).update(IsDeleted=True)
                return HttpResponse("ok")
            except:
                return HttpResponse("Error in service pack deletion")
        else:
            return HttpResponse("Method Not allowed")
    else:
        return redirect("/")



###################################################################


def ServicePackAllotedToMarkets(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_packallotment.html')
        try:
            marketobj=[]
            markets=Market.objects.select_related().all()
            
            for market in markets:
                beanobj=MarketWithServicePacks()
                beanobj.MarketName=market.MarketName
                beanobj.MarketAddress=market.MarketAddress
                beanobj.ContactPerson=market.ContactPerson
                
                tempser=market.has_servicepacks.all()
                
                ser=[]
                for servicepack in tempser:
                    serbean=ServicePackBean()
                    serbean.ServicePackName=servicepack.ServicePackName
                    ser.append(serbean)
                
                beanobj.ServicePacks=ser
                    
                marketobj.append(beanobj)
            c=Context({'marketobj':marketobj})
            return HttpResponse(t.render(c))
        except:
            print sys.exc_info()
            c=Context({'':''})
            return HttpResponse(t.render(c))
    else:
        return redirect("/")



def ServicePackAllotmentForm(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        markets=Market.objects.all()
        t=get_template('superadmin_packallotment.html')
        c=Context({'marketname':'marketname','markets':markets})
        return HttpResponse(t.render(c))
    else:
        return redirect("/")
    
    
def listdetails(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        t=get_template('superadmin_packallotment.html')
        #print request.POST['searchbymarket']
        try:
            newpacks=[]
            market=Market.objects.select_related().get(MarketName=request.POST['marketlist'])
            currentpacksinmarket=market.has_servicepacks.all()
            servicepacks=ServicePack.objects.filter(IsDeleted=False)
                        
            for pack in servicepacks:
                if pack in currentpacksinmarket:
                    continue
                newpacks.append(pack)
               
            c=Context({'marketdetails':market,'marketservicepacks':currentpacksinmarket,'additionalpacks':newpacks})
            return HttpResponse(t.render(c))
        except:
            print sys.exc_info
            c=Context({'marketname':'marketname'})
            return HttpResponse(t.render(c))
    else:
        return redirect("/")
    
    

def ServicePackAllotmentToMarket(request):
    if 'usertype' in request.session and request.session['usertype']=="SUPER_ADMIN":
        try:
            print request.POST
            marketid=request.POST['marketid']
            ajaxcheckbox=request.POST['checkobj'].split(",")
            marketref=Market.objects.get(MarketId=marketid)
            
            print ajaxcheckbox
            
            m=marketref.has_servicepacks.all()
            
            for i in m:
                #sp=ServicePack.objects.get(ServicePackName=i.ServicePackName)
                marketref.has_servicepacks.remove(i)
            
            for i in ajaxcheckbox:
                sp=ServicePack.objects.get(ServicePackId=int(i))
                marketref.has_servicepacks.add(sp)
            
            return HttpResponse('Done')
        except:
            print sys.exc_info()
            return HttpResponse('Failed to Allot service packs to Market')
    else:
        return redirect("/")   



    
def ShowChangePassword(request):
    if 'usertype' in request.session and 'userid' in request.session:
        t=get_template('changepassword.html')
        c=Context({'changepassword':'changepassword'})
        return HttpResponse(t.render(c))
    return redirect('/listmarket')



class ServicePackBean:
    _ServicePackName= None
    @property
    def ServicePackName(self):
        return self._ServicePackName
    @ServicePackName.setter
    def ServicePackName(self, ServicePackName):
        self._ServicePackName=ServicePackName
        
    

class MarketWithServicePacks:
    _MarketName,_MarketAddress,_ContactPerson,_ServicePacks=None,None,None,None
    @property 
    def MarketName(self):
        return self._MarketName
    @MarketName.setter
    def MarketName(self, MarketName):
        self._MarketName = MarketName
    
    @property
    def MarketAddress(self):
        return self._MarketAddress
    @MarketAddress.setter
    def MarketAddress(self, MarketAddress):
        self._MarketAddress = MarketAddress

    @property
    def ContactPerson(self):
        return self._ContactPerson
    @ContactPerson.setter
    def ContactPerson(self, ContactPerson):
        self._ContactPerson = ContactPerson
        
    @property
    def ServicePacks(self):
        return self._ServicePacks
    @ServicePacks.setter
    def ServicePacks(self, ServicePack):
        self._ServicePacks=ServicePack
        
##############################################

class MarketDetails:
    _MarketName, _MarketAddress, _MarketDescription, _ContactPerson, _ContactPhoneNumber, _ContactEmailAddress ,_MarketWebsite,_MarketArea= None, None,None, None, None,None,None,None
    @property
    def MarketName(self):
        return self._MarketName
    @MarketName.setter
    def MarketName(self, MarketName):
        self._MarketName = MarketName
    
    @property
    def MarketAddress(self):
        return self._MarketAddress
    @MarketAddress.setter
    def MarketAddress(self, MarketAddress):
        self._MarketAddress = MarketAddress
        
    @property
    def MarketDescription(self):
        return self._MarketDescription
    @MarketDescription.setter
    def MarketDescription(self, MarketDescription):
        self._MarketDescription =MarketDescription
    
    @property
    def ContactPerson(self):
        return self._ContactPerson
    @ContactPerson.setter
    def ContactPerson(self, ContactPerson):
        self._ContactPerson = ContactPerson
        
    @property
    def ContactPhoneNumber(self):
        return self._ContactPhoneNumber
    @ContactPhoneNumber.setter
    def ContactPhoneNumber(self, ContactPhoneNumber):
        self._ContactPhoneNumber = ContactPhoneNumber
    
    @property
    def ContactEmailAddress(self):
        return self._ContactEmailAddress
    @ContactEmailAddress.setter
    def ContactEmailAddress(self, ContactEmailAddress):
        self._ContactEmailAddress = ContactEmailAddress
        
    @property
    def MarketWebsite(self):
        return self._MarketWebsite
    @MarketWebsite.setter
    def MarketWebsite(self, MarketWebsite):
        self._MarketWebsite = MarketWebsite
        
    @property
    def MarketArea(self):
        return self._MarketArea
    @MarketArea.setter
    def MarketArea(self, MarketArea):
        self._MarketArea = MarketArea