
from django.db import models
import datetime
from django.contrib.auth.models import User

''' used to maintain unique key for maintaining session of mobile users'''
class Token(models.Model):
    TokenId=models.AutoField(primary_key=True)
    usertoken=models.CharField(max_length=20)
    UserId=models.ForeignKey(User)
    ModifiedTime=models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        db_table="token"
    

''' Table to maintain user types'''     
class UserType(models.Model):
    UserTypeId=models.AutoField(primary_key=True)
    UserTypeName=models.CharField(max_length=250)        
    class Meta:
        db_table="usertype"
   
   
class MapUserTypeWithUser(models.Model):
    MapUserTypeId=models.AutoField(primary_key=True)
    UserId=models.ForeignKey(User)
    UserTypeId=models.ForeignKey(UserType)
    class Meta:
        db_table="mapusertypewithuser"
      
      
      
''' Buyer in the market''' 
class Consumer(models.Model):
    ConsumerId=models.AutoField(primary_key=True)
    EmailAddress=models.CharField(max_length=100)
    Name=models.CharField(max_length=64)
    MobileNumber=models.CharField(max_length=500)
    StreetAddress=models.CharField(max_length=500)
    City=models.CharField(max_length=250)
    State=models.CharField(max_length=250)
    PostalCode=models.IntegerField(max_length=6)
    Country=models.CharField(max_length=250)
    UserId=models.ForeignKey(User)
    CreatedTime=models.DateTimeField()
    class Meta:
        db_table="consumer"
          
 
 
          
class ServiceType(models.Model):
    ServiceTypeId=models.AutoField(primary_key=True)
    ServiceTypeName=models.CharField(max_length=250)
    class Meta:
        db_table="servicetype"
  
  
  
''' Services which will be offered to customer by super admin.'''   
class Service(models.Model):
    ServiceId=models.AutoField(primary_key=True)
    ServiceName=models.CharField(max_length=250) 
    Description=models.CharField(max_length=500)
    StartDate=models.DateTimeField(max_length=250)
    EndDate=models.DateTimeField(max_length=250)
    Rate=models.DecimalField(max_digits=10, decimal_places=2)
    Discount=models.CharField(max_length=250)
    IsDeleted=models.BooleanField()
    CreatedTime=models.DateTimeField()
    ServiceTypeId=models.ForeignKey(ServiceType)
    ModifiedTime=models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        db_table="service"
    

'''ServicePacks for Market.it will contain one or more services
    and thus has Many to Many relation'''
class ServicePack(models.Model):
    ServicePackId=models.AutoField(primary_key=True) 
    ServicePackName=models.CharField(max_length=250)
    Price=models.DecimalField(max_digits=10, decimal_places=2)
    ServicePackDescription=models.CharField(max_length=250)
    Discount=models.CharField(max_length=250)
    ExpiryDate=models.DateField(max_length=250)
    CreatedTime=models.DateTimeField()
    ModifiedTime=models.DateTimeField(default=datetime.datetime.now())
    IsDeleted=models.BooleanField()
    has_services=models.ManyToManyField(Service)
      
    class Meta:
        db_table="servicepack"



''' A Representative to register customers.
    will be used on customers registration'''
class SalesReference(models.Model):
    SalesRepresentativeId=models.CharField(max_length=100,primary_key=True) 
    SalesRepresentativeName=models.CharField(max_length=250)
    CreatedTime=models.DateTimeField()
    class Meta:
        db_table="salesrepresentative"
     
  
''' Maintains category of Stores'''
class StoreCategory(models.Model):
    StoreCategoryId=models.AutoField(primary_key=True) 
    StoreCategoryName=models.CharField(max_length=250)
    class Meta:
        db_table="storecategory"        



class SubCategory(models.Model):
    SubcategoryId=models.AutoField(primary_key=True) 
    SubCategoryName=models.CharField(max_length=250)
    StoreCategoryType=models.ForeignKey(StoreCategory)
    class Meta:
        db_table="subcategory"



class DeliveryOptions(models.Model):
    DeliveryId=models.AutoField(primary_key=True)
    DeliveryTypeName=models.CharField(max_length=100)
    class Meta:
        db_table="deliveryoptions" 
        

        
# class ProductCategory(models.Model):
#     ProductCatId=models.AutoField(primary_key=True) 
#     ProductCatName=models.CharField(max_length=250)
#     class Meta:
#         db_table="ProductCategory" 
#     
    
                    
''' Maintains records of products that has been uploaded by customer'''         
class Product(models.Model):
    ProductId=models.AutoField(primary_key=True) 
    #ProductTitle=models.CharField(max_length=250)
    ProductDescription=models.CharField(max_length=500)
    ProductPrice=models.DecimalField(max_digits=10, decimal_places=2)
    Quantity=models.IntegerField(max_length=50,default=0)
    ProductImage=models.CharField(max_length=250)
    CreatedTime=models.DateTimeField()
    ProductType=models.CharField(max_length=250)
    ModifiedTime=models.DateTimeField(default=datetime.datetime.now())
    has_deliveryoptions=models.ManyToManyField(DeliveryOptions)
    class Meta:
        db_table="products"
    

''' Store Belongs to Customer which has one to one mapping.
    so, a foreign key relaion between User and store states
    the one to one mapping'''
class CustomerStore(models.Model):
    StoreId=models.AutoField(primary_key=True)
    StoreName=models.CharField(max_length=250)
    StreetAddress=models.CharField(max_length=500)
    City=models.CharField(max_length=250)
    PostalCode=models.IntegerField(max_length=10)
    State=models.CharField(max_length=250)
    Country=models.CharField(max_length=250)
    MainPhoneNumber=models.CharField(max_length=50)
    ContactPerson=models.CharField(max_length=250)
    EmailAddress=models.EmailField(max_length=250)
    Website=models.CharField(max_length=250)
    BannerImages=models.CharField(max_length=250)
    StoreLogo=models.CharField(max_length=250)
    HoursOfOperation=models.CharField(max_length=250)
    ProductsUploaded=models.IntegerField(max_length=10,default=0)
    Is_Activated=models.BooleanField()
    Is_Blocked=models.BooleanField()
    CreatedTime=models.DateTimeField()
    ModifiedTime=models.DateTimeField(default=datetime.datetime.now())
    CustomerUserId=models.ForeignKey(User)
    SalesRepId=models.CharField(max_length=50)
    ServicePack=models.ForeignKey(ServicePack)
    has_products=models.ManyToManyField(Product)
    has_subcategories=models.ManyToManyField(SubCategory)
    
    class Meta:
        db_table="customerstore"
        
            

''' Market for an area. Markets will be allocated by service packs from super admin'''    
class Market(models.Model):
    MarketId=models.AutoField(primary_key=True)
    MarketName=models.CharField(max_length=250)
    MarketAddress=models.CharField(max_length=500)
    MarketDescription=models.CharField(max_length=500)
    ContactPerson=models.CharField(max_length=250)
    ContactPhoneNumber=models.CharField(max_length=250)
    ContactEmailAddress=models.EmailField(max_length=250)
    MarketLogo=models.CharField(max_length=250)
    MarketImage=models.CharField(max_length=250)
    MarketWebsite=models.CharField(max_length=250)
    CreatedTime=models.DateTimeField()
    ModifiedTime=models.DateTimeField(default=datetime.datetime.now())
    UserId=models.ForeignKey(User)
    has_servicepacks=models.ManyToManyField(ServicePack)
    has_stores=models.ManyToManyField(CustomerStore)
    has_products=models.ManyToManyField(Product)
    class Meta:
        db_table="market"
     

    

class Email(models.Model):
    EmailId=models.AutoField(primary_key=True) 
    NumberOfEmails=models.CharField(max_length=100,blank=True)
    ServiceId=models.ForeignKey(Service)
     
    class Meta:
        db_table="email"
          
     
class SMS(models.Model):
    SMSId=models.AutoField(primary_key=True) 
    NumberOfSMS=models.CharField(max_length=100,blank=True)
    ServiceId=models.ForeignKey(Service)
     
    class Meta:
        db_table="sms"
     
     
     
class ProductShowCase(models.Model):
    ProductShowcaseId=models.AutoField(primary_key=True) 
    NumberOfProductsAllowedToUpload=models.CharField(max_length=100,blank=True)
    ServiceId=models.ForeignKey(Service)
     
    class Meta:
        db_table="productshowCase"
     
     
     
class Advertising(models.Model):
    Advertiseid=models.AutoField(primary_key=True) 
    NumberOfAdvetisement=models.CharField(max_length=100,blank=True)
    ServiceId=models.ForeignKey(Service)
     
    class Meta:
        db_table="advertising"
        
        
class Email_Verification(models.Model):
    Verificationid=models.AutoField(primary_key=True)
    Verification_Link=models.CharField(max_length=100)
    Created_On=models.DateTimeField()
    Verified_On=models.DateTimeField(null=True, blank=True)
    Auth_Id=models.IntegerField()
     
    class Meta:
        db_table="email_verification"
