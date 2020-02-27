from django.conf.urls.defaults import patterns, url
from eShop.webservices.customer.login.handlers import CustomerLogInWebService
from eShop.webservices.customer.logout.handlers import CustomerLogOutWebService
from eShop.piston.resource import Resource
from eShop.webservices.customer.registration.handlers import CustomerRegistrationHandler
from eShop.webservices.customer.marketarea.handlers import MarketAreaHandler
from eShop.webservices.customer.products.handlers import ProductsList
from eShop.webservices.customer.servicepacks.handlers import ServicePackHandler
from eShop.webservices.customer.categories.handlers import CategoriesHandler
from eShop.webservices.customer.productupload.handlers import ProductUploadHandler
from eShop.webservices.customer.profile.handlers import CustomerProfileHandler
from eShop.webservices.customer.deliveryoptions.handlers import DeliveryOptionsHandler

class CsrfExemptResource(Resource):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

customerlogin= CsrfExemptResource(CustomerLogInWebService)
customerlogout= CsrfExemptResource(CustomerLogOutWebService)
customerregister= CsrfExemptResource(CustomerRegistrationHandler)
marketnames=CsrfExemptResource(MarketAreaHandler)
productslist=CsrfExemptResource(ProductsList)
servicepacks=CsrfExemptResource(ServicePackHandler)
categories=CsrfExemptResource(CategoriesHandler)
productupload=CsrfExemptResource(ProductUploadHandler)
customerprofile=CsrfExemptResource(CustomerProfileHandler)
deliveryoptions=CsrfExemptResource(DeliveryOptionsHandler)

urlpatterns = patterns('',
    url(r'^customerlogin/json',customerlogin,{'emitter_format':'json'} ),
    url(r'^customerlogout/json',customerlogout,{'emitter_format':'json'} ),
    url(r'^customerregister/json',customerregister,{'emitter_format':'json'} ),
    url(r'^marketnames/json',marketnames,{'emitter_format':'json'} ),
    url(r'^productlist/json',productslist,{'emitter_format':'json'} ),
    url(r'^servicepacks/json',servicepacks,{'emitter_format':'json'} ),
    url(r'^categories/json',categories,{'emitter_format':'json'} ),
    url(r'^uploadproduct/json',productupload,{'emitter_format':'json'} ),
    url(r'^customerprofile/json',customerprofile,{'emitter_format':'json'} ),
    url(r'^deliveryoptions/json',deliveryoptions,{'emitter_format':'json'} ),
)
