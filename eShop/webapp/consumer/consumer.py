from django.template.loader import get_template
from django.template.context import Context
from django.http import HttpResponse
from eShop.webapp.models import Consumer, Market, Email_Verification, UserType,\
    MapUserTypeWithUser, CustomerStore
import datetime
from django.contrib.auth.models import User
import string
from random import choice
import threading
import time
from django.conf import settings
from eShop.settings import EMAIL_HOST_USER
from django.core.mail.message import EmailMultiAlternatives
import sys
from django.shortcuts import redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, InvalidPage



def ConsumerEditProfile(request):
    if 'usertype' in request.session and 'userid' in request.session: 
        if request.session['usertype'] == "CONSUMER" and request.session['userid'] != "":
            consumerinfo = Consumer.objects.get(UserId__id=int(request.session['userid']))
            t = get_template('consumer_page.html')
            c = Context({'editprofile':'editprofile', 'consumerinfo':consumerinfo})
            return HttpResponse(t.render(c))
        else:
            return redirect("/consumerhome/") 
    else:
        return redirect("/consumerhome/") 


def ConsumerUpdateProfile(request):
    if 'usertype' in request.session and 'userid' in request.session: 
        if request.session['usertype'] == "CONSUMER" and request.session['userid'] != "":
            consumerinfo = Consumer.objects.get(UserId__id=int(request.session['userid']))
            consumerinfo.Name=request.POST['fullname']
            consumerinfo.MobileNumber = request.POST['phonenumber']
            consumerinfo.StreetAddress = request.POST['streetaddress']
            consumerinfo.City = request.POST['city']
            consumerinfo.State = request.POST['state']
            consumerinfo.Country = request.POST['country']
            if request.POST['postalcode'] == "":
                consumerinfo.PostalCode = None
            else:
                consumerinfo.PostalCode = request.POST['postalcode']
            consumerinfo.save()
            return render_to_response('consumer_page.html',{'editprofile':'editprofile', 'message':'Updated Successfully', 'consumerinfo':consumerinfo})
        else:
            return redirect('/consumerhome/')
    else:
        return redirect('/consumerhome/')
   



def ConsumerHome(request):
    if 'usertype' in request.session and 'userid' in request.session: 
        if request.session['usertype'] == "CONSUMER":
            t = get_template('consumer_index.html')
            storeref=CustomerStore.objects.all().order_by('-StoreId')
            marketsref=Market.objects.all().order_by('-MarketId')[:20]
            consumerinfo = Consumer.objects.get(UserId=int(request.session['userid']))
            paginator = Paginator(storeref, 9)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                storeref = paginator.page(page)
            except (EmptyPage, InvalidPage):
                storeref = paginator.page(paginator.num_pages)
            c=Context({'stores':storeref,'markets':marketsref,'consumer':consumerinfo})
            return HttpResponse(t.render(c))


def ConsumerPage(request):
    t = get_template('consumer_page.html')
    #consumerinfo = Consumer.objects.get(UserId__id=int(request.session['userid']))
    c = Context({})
    return HttpResponse(t.render(c))



def ConsumerRegisterationForm(request):
    t=get_template('consumer_registration.html')
    c=Context({'regform':'regform'})
    return HttpResponse(t.render(c))


def ConsumerRegisteration(request):
    t=get_template('index.html')
    marketsref=Market.objects.all().order_by('-MarketId')[:20]
    
    valuecheck=User.objects.filter(username=request.POST['emailid']).exists()
    if valuecheck==False:
        try:
            user=User.objects.create_user(username=request.POST['emailid'].strip(), email=request.POST['emailid'].strip(), password=request.POST['cpwd'])
            consumerref=Consumer(EmailAddress=request.POST['emailid'].strip(),Name=request.POST['fullname'].strip(),MobileNumber=request.POST['mobilenumber'].strip(),StreetAddress=request.POST['streetaddr'],City=request.POST['city'],PostalCode=int(request.POST['postalcode'].strip()),State=request.POST['state'],Country=request.POST['country'],CreatedTime=datetime.datetime.now(),UserId=user)
            consumerref.save()
            usertype=UserType.objects.get(UserTypeName="CONSUMER")
            mapins=MapUserTypeWithUser()
            mapins.UserTypeId=usertype
            mapins.UserId=user
            mapins.save()
            link=CharGenerator()
            emailto=sendMail(consumerref.EmailAddress,link,user.id)
            emailto.start()
            Email_Verification(Verification_Link=link,Auth_Id=user.id,Created_On=datetime.datetime.now()).save()
            c=Context({'message':'Registration completed. Please check your mail box for verification link.','market':marketsref})
            return HttpResponse(t.render(c))
        except:
            print sys.exc_info()
            c=Context({'message':'Registration failed. Please try after some time','market':marketsref})
            return HttpResponse(t.render(c))
    else:
        c=Context({'message':'Email Id already in use.','market':marketsref})
        return HttpResponse(t.render(c))
    

    
def CharGenerator():
    chars = string.letters + string.digits
    charseq=''
    for i in range(40):
        charseq = charseq + choice(chars)
    return charseq



class sendMail(threading.Thread):
    def __init__(self, emailid,link,authid):
        threading.Thread.__init__(self)
        self.emailid=emailid
        self.link=link
        self.authid=authid
        
    def run(self):
        try:
            t1=time.time()
            t = get_template('verificationtemplate.html')
            html = t.render(Context({'link':self.link,'emailid':self.emailid,'authid':self.authid,'SERVER':settings.SERVER_NAME}))    
            msg = EmailMultiAlternatives("eShop: Verification Link for your account","", EMAIL_HOST_USER,[self.emailid])
            msg.attach_alternative(html, "text/html")
            msg.send()
            print "email send to:"+str(self.emailid)+" Time taken:"+str(time.time()-t1)
        except:
            print "Error in sending mail. Email to: "+str(self.emailid)+" "+str(sys.exc_info())
            pass
        
        
        
def Verification(request,authid,verificationlink):
    t=get_template('index.html')
    emref=Email_Verification.objects.filter(Auth_Id=authid).exists()
    if emref==True:
        message=''
        emailverifyref=Email_Verification.objects.get(Auth_Id=authid)
        print emailverifyref.Verification_Link.strip()
        if emailverifyref.Verification_Link.strip()==verificationlink.strip():
            Email_Verification.objects.filter(Auth_Id=authid).update(Verification_Link=CharGenerator(),Verified_On=datetime.datetime.now())
            message='Verification completed.'
        else:
            message='Verification link expired.'
    else:
        message="You are not a registered customer. Please register."
        
    marketsref=Market.objects.all().order_by('-MarketId')[:20]
    c=Context({'message':message,'market':marketsref})
    return HttpResponse(t.render(c)) 