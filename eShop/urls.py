from django.conf.urls.defaults import patterns, include,  url
from django.conf import settings
from django.conf.urls.static import static
from eShop.webapp.superadmin.superadmin import    CheckMarket,\
    CheckSalesRef, MarketAdminCredentials, CheckUserName, ShowServices,\
    CreateService, DeleteService, UpdateService,Markets,\
    MarketAdminRegistrationForm, MarketRegistrationForm, ShowSalesRef,\
    SalesRefRegistrationForm, SalesRefRegistration, AddServiceForm, CheckService,\
    ShowServicePacks, AddServicePackForm, CheckServicePack, CreateServicePack,\
    DeleteServicePack, ServicePackAllotedToMarkets, ServicePackAllotmentToMarket,\
    ServicePackAllotmentForm, listdetails, UpdateMarket, EditMarket,\
    DeleteSalesrepid, EditSalesRepId, UpdateSalesRepId, EditService,\
    EditServicePack, UpdateServicePack, ShowChangePassword
from eShop.webapp.customer.customer import UploadProduct,\
    EditProfile, ViewProfile, AddProduct, CustomerHome,\
    DeleteProduct, CustomerStoreRegistrationForm1,\
    CustomerStoreRegistrationForm2, CustomerStoreRegistration, CheckEmailAddress, UpdateProfile, ShowLoginPage, UpdateProduct, EditProduct   #ServicePackSearch,MarketSearch 
from eShop.webservices import urls
from eShop.webapp.views import LogOut, ValidateUser, IndexPage, MarketList,\
    StoreSearch, ProductSearch, IndexPageSearch,StoreSearchOnFourHoursDeliveryPage,\
    ProductSearchOnFourHoursDeliveryPage, StoresSearch, ProductsSearch,\
    RenderToMarket,Categories, Search, ChangePassword, LostPassword,\
    SendPassword, CustomerShowChangePassword, MarketAdminShowChangePassword,\
    ConsumerShowChangePassword, ProductCategoryOnFourHoursDeliveryPage,\
    CategorySearch
from eShop.webapp.marketadmin.marketadmin import MarketAdmin, AcceptStore,\
    DeclineStore, StoreDetails
from eShop.webapp.consumer.consumer import ConsumerRegisterationForm,\
    ConsumerRegisteration, Verification, ConsumerEditProfile,\
    ConsumerUpdateProfile, ConsumerPage, ConsumerHome
from eShop.piston.manaage import management
urlpatterns = patterns('',
                       
    url(r'^$',IndexPage),                   
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^listmarket/$',Markets),
    url(r'^createmarket/$',MarketRegistrationForm),
    url(r'^marketadminreg/$',MarketAdminRegistrationForm),
    url(r'^marketadmincredentials/$',MarketAdminCredentials),
    url(r'^checkmarketname',CheckMarket),
    url(r'^checkusername',CheckUserName),
    url(r'^editmarket$',EditMarket),
    url(r'^updatemarket$',UpdateMarket),
    url(r'^salesref',ShowSalesRef),
    url(r'^registersalesref',SalesRefRegistration),
    url(r'^formsalesref',SalesRefRegistrationForm),
    url(r'^checksalesref',CheckSalesRef),
    url(r'^deletesalesrepid$',DeleteSalesrepid),
    url(r'^editsalesrepid$',EditSalesRepId),
    url(r'^updatesalesrepid$',UpdateSalesRepId),
    url(r'^registercustomer$',CustomerStoreRegistrationForm1),
    url(r'^customercredentials$',CustomerStoreRegistrationForm2),
    url(r'^customerreg$',CustomerStoreRegistration),
    url(r'^checkemailaddress$',CheckEmailAddress),
    url(r'^services$',ShowServices),
    url(r'^checkservice$',CheckService),
    url(r'^addservice/$',AddServiceForm),
    url(r'^createservice$',CreateService),
    url(r'^deleteservice$',DeleteService),
    url(r'^editservice$',EditService),
    url(r'^updateservice$',UpdateService),
    url(r'^servicepacks$',ShowServicePacks),
    url(r'^checkservicepack$',CheckServicePack),
    url(r'^addservicepack$',AddServicePackForm),
    url(r'^createservicepack$',CreateServicePack),
    url(r'^servicepackdelete$',DeleteServicePack),
    url(r'^editservicepack$',EditServicePack),
    url(r'^updateservicepack$',UpdateServicePack),
    url(r'^showallotment$',ServicePackAllotedToMarkets),
    url(r'^allotmentform$',ServicePackAllotmentForm),
    url(r'^listdetails$',listdetails),
    url(r'^updatepacktomarket',ServicePackAllotmentToMarket),
    url(r'^login$',ShowLoginPage),
    url(r'^validateuser$',ValidateUser),
    url(r'^customerhome$',CustomerHome),
    url(r'^uploadproduct$',UploadProduct),
    url(r'^management$',management),
    url(r'^editprofile$',EditProfile),
    url(r'^viewprofile',ViewProfile),
    url(r'^updateprofile',UpdateProfile),
    url(r'^addproduct',AddProduct),
    url(r'^updateproduct',UpdateProduct),
    url(r'^deleteproduct',DeleteProduct),
    url(r'^editproduct',EditProduct),
    url(r'^marketadmin/$',MarketAdmin),
    url(r'^acceptstore$',AcceptStore),
    url(r'^declinestore/$',DeclineStore),
    url(r'^storedetails/$',StoreDetails),
    url(r'^marketlist',MarketList),
    url(r'^storesearch',StoreSearch),
    url(r'^productsearch',ProductSearch),
    url(r'^indexsearch',IndexPageSearch),
    url(r'^store$',StoresSearch),
    url(r'^product$',ProductsSearch),
    url(r'^store/(?P<storeid>\d+)/$',StoreSearchOnFourHoursDeliveryPage),
    url(r'^product/(?P<productid>\d+)/$',ProductSearchOnFourHoursDeliveryPage),
    url(r'^(?P<marketid>\d+)/$',RenderToMarket),
    #url(r'^(?P<marketname>\w+)/(?P<storename>\w+)$',StoreURI),
    url(r'^(?P<marketid>\d+)/categories/(?P<categoryid>\w+)/',Categories),
    url(r'^search$',Search),
    url(r'showchangepassword',ShowChangePassword),
    url(r'changepassword',ChangePassword),
    url(r'lostpassword',LostPassword),
    url(r'sendpassword',SendPassword),
    url(r'^logout',LogOut),
    url(r'passwordchange$',CustomerShowChangePassword),
    url(r'cpwdmarketadmin$',MarketAdminShowChangePassword),
    url(r'^ws/',include(urls)),
    url(r'^consumerreg/',ConsumerRegisterationForm),
    url(r'^consumercredentials',ConsumerRegisteration),
    url(r'^verification/(?P<authid>\d+)/(?P<verificationlink>\w+)',Verification),
    url(r'^consumerviewprofile',ConsumerEditProfile),
    url(r'^consumerupdateprofile',ConsumerUpdateProfile),
    url(r'^consumerpage',ConsumerPage),
    url(r'^consumerhome',ConsumerHome),
    url(r'^cpwdconsumer',ConsumerShowChangePassword),
    #changes made by amit
    url(r'^store/(?P<storeid>\d+)/(?P<category>[\w|\W]+)/$',ProductCategoryOnFourHoursDeliveryPage),
    url(r'^categorysearch',CategorySearch),
    #end
    
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)