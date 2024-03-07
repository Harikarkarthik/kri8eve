from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from requests.api import options
from tinymce.models import HTMLField


class UserRoleRef(models.Model):
    # user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True)
    user_role_name = models.CharField(max_length=250, blank=True, null=True)
    salary = models.CharField(max_length=250, blank=True, null=True)
    bonus= models.CharField(max_length=250, blank=True, null=True)
    incentives= models.CharField(max_length=250, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class kri8evTeam(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True)
    role=models.ForeignKey(UserRoleRef, on_delete= models.CASCADE ,null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    mobile_number = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    # ref_code = models.CharField(max_length=200, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Team_Code(models.Model):
    team=models.ForeignKey(kri8evTeam, on_delete= models.CASCADE ,null=True)
    ref_code = models.CharField(max_length=200, blank=True, null=True)

class Product_Category(models.Model):
    image=models.FileField(upload_to= 'product_category_image', blank=True, null=True)
    Product_Category_Name= models.CharField(max_length=250, blank=True, null=True)

    Product_Category_Description= models.CharField(max_length=250, blank=True, null=True)
    Create_TimeStamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Product_Sub_Category(models.Model):
    product_category= models.ForeignKey(Product_Category,on_delete=models.CASCADE, blank=True, null=True)
    image=models.FileField(upload_to= 'product_sub_category_image', blank=True, null=True)
    product_sub_category_name= models.CharField(max_length=250, blank=True, null=True)
    product_sub_category_Description= models.CharField(max_length=250, blank=True, null=True)
    Create_TimeStamp= models.CharField(max_length=250, blank=True, null=True)
    Last_Update_TimeStamp= models.CharField(max_length=250, blank=True, null=True)

class Product_Inventory(models.Model):

    Quantity= models.CharField(max_length=250, blank=True, null=True)
    Create_TimeStamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Discount(models.Model):

    Discount_Name= models.CharField(max_length=250, blank=True, null=True)
    Discount_Description= models.CharField(max_length=250, blank=True, null=True)
    Discount_Percentage= models.CharField(max_length=250, blank=True, null=True)
    Status= models.CharField(max_length=250, blank=True, null=True)

    start_date= models.DateField(auto_now_add=False,verbose_name="Start_date",blank=True,null=True)
    end_date=models.DateField(auto_now_add=False,verbose_name="End_date",blank=True,null=True)
    Create_TimeStamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Brand(models.Model):
    brand_name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Master_Attributes(models.Model):
    name =  models.CharField(max_length=250, blank=True, null=True)

class Master_AttributeOptions(models.Model):
    option =  models.CharField(max_length=250, blank=True, null=True)

    attributes = models.ForeignKey(Master_Attributes,on_delete= models.CASCADE,null=True)


class Product(models.Model):
    brand=models.ForeignKey(Brand, on_delete= models.CASCADE ,null=True)

    # post_image = models.FileField(upload_to= 'post_images', blank=True, null=True)
    # post_video = models.FileField(upload_to= 'post_video', blank=True, null=True)

    Product_Name= models.CharField(max_length=250, blank=True, null=True)
    Product_Description= models.TextField(max_length=5000, blank=True, null=True)
    Product_Image= models.FileField(upload_to= 'Product_Image', blank=True, null=True)
    # Product_Video= models.FileField(upload_to= 'Product_Video', blank=True, null=True)
    Product_Video= models.CharField(max_length=1000, blank=True, null=True)
    Product_Selling_Price= models.IntegerField(blank=True, null=True)
    Gst= models.CharField(max_length=250, blank=True, null=True)
    Product_Listed_Price= models.CharField(max_length=250, blank=True, null=True)
    Product_Details= models.TextField(max_length=5000, blank=True, null=True)
    Status= models.CharField(max_length=250, blank=True, null=True)
    Create_TimeStamp= models.CharField(max_length=250, blank=True, null=True)
    Last_Update_TimeStamp= models.CharField(max_length=250, blank=True, null=True)
    HSN_SAC_Code= models.CharField(max_length=250, blank=True, null=True)
    Wash_instructions= models.TextField(max_length=5000, blank=True, null=True)
    Product_Category=models.ForeignKey(Product_Category,on_delete=models.CASCADE, blank=True, null=True)
    product_sub_category=models.ForeignKey(Product_Sub_Category,on_delete=models.CASCADE, blank=True, null=True)

    Discount= models.ForeignKey(Discount,on_delete=models.CASCADE, blank=True, null=True)
    Product_Inventory = models.ForeignKey(Product_Inventory,on_delete=models.CASCADE, blank=True, null=True)
    count_sold                  = models.IntegerField(default=0,blank=True, null=True)

    # attribute = models.ForeignKey(Attributes,on_delete=models.CASCADE, blank=True, null=True)
    # wishlistss = models.BooleanField(default=0, blank=True, null=True)
class Attributes(models.Model):
    Product_ID =  models.ForeignKey(Product,on_delete= models.CASCADE,null=True)
    name =  models.CharField(max_length=250, blank=True, null=True)

class AttributeOptions(models.Model):
    attributes = models.ForeignKey(Attributes,on_delete= models.CASCADE,null=True)
    option =  models.CharField(max_length=250, blank=True, null=True)
    # option_1 =  models.CharField(max_length=250, blank=True, null=True)
    # option_2=  models.CharField(max_length=250, blank=True, null=True)
    # option_3=  models.CharField(max_length=250, blank=True, null=True)
    # option_4 =  models.CharField(max_length=250, blank=True, null=True)




class ProductAttributes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    attributes = models.ForeignKey(Attributes,on_delete= models.CASCADE,null=True)
    Product_ID =  models.ForeignKey(Product,on_delete= models.CASCADE,null=True)
    selectedoptions = models.CharField(max_length=250, blank=True, null=True)


class Custom_user_profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    profile_img_64 = models.TextField(max_length=99999, blank=True, null=True)
    profile_img= models.FileField(upload_to= 'profile_img', blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Custom_User(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(UserRoleRef,on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    Full_Name= models.CharField(max_length=250, blank=True, null=True)
    Date_Of_Birth= models.DateField(max_length=250, blank=True, null=True)
    Mobile_Number= models.CharField(max_length=250, blank=True, null=True)
    Email_ID= models.EmailField(max_length=250, blank=True, null=True)
    Terms= models.CharField(max_length=250, blank=True, null=True)
    referral_code=models.CharField(max_length=250, blank=True, null=True)
    user_to_user_refcode=models.CharField(max_length=250, blank=True, null=True)

    gender= models.CharField(max_length=250, blank=True, null=True)
    location= models.CharField(max_length=250, blank=True, null=True)
    alt_number= models.CharField(max_length=250, blank=True, null=True)

    Create_TimeStamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

# class User_Authentication(models.Model):
#     User_Name= models.CharField(max_length=250, blank=True, null=True)
#     User_Password= models.CharField(max_length=250, blank=True, null=True)
#     Status= models.CharField(max_length=250, blank=True, null=True)
#     Create_TimeStamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class User_Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True,related_name='spotlytCustom_User')
    Address= models.CharField(max_length=250, blank=True, null=True)
    City= models.CharField(max_length=250, blank=True, null=True)
    State= models.CharField(max_length=250, blank=True, null=True)
    Country= models.CharField(max_length=250, blank=True, null=True)
    Pincode= models.CharField(max_length=250, blank=True, null=True)
    street= models.CharField(max_length=250, blank=True, null=True)
    address_type= models.CharField(max_length=250, blank=True, null=True)
    delfault_address = models.BooleanField(default=0, blank=True, null=True)


class User_Payment(models.Model):
    Payment_Name= models.CharField(max_length=250, blank=True, null=True)
    Payment_Type= models.CharField(max_length=250, blank=True, null=True)
    GST= models.CharField(max_length=250, blank=True, null=True)
    Delivery_Charges= models.CharField(max_length=250, blank=True, null=True)
    Amount= models.CharField(max_length=250, blank=True, null=True)
    Create_TimeStamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)


class Reviews(models.Model):
    # course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    Product_ID= models.ForeignKey(Product, on_delete= models.SET_NULL, null=True)
    reviewMessage = models.CharField(max_length=500, blank=True, null=True)
    star_rating = models.CharField(max_length=20, blank=True, null=True)
    review_image= models.FileField(upload_to= 'review_image', blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)



class FAQs(models.Model):
    # course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    # lesson = models.ForeignKey(Lesson, on_delete= models.CASCADE,null=True)
    # user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    faq_name = models.CharField(max_length=250, blank=True, null=True)
    # faq_type = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)



class Testimonials(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    category = models.CharField(max_length=250, blank=True, null=True)
    image = models.FileField(upload_to= 'testimonials_images', blank=True, null=True)
    # video = models.FileField(upload_to= 'testimonials_video', blank=True, null=True)
    video = models.CharField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(max_length=20, blank=True, null=True)

    feedback_small_description = models.TextField(max_length=2000, blank=True, null=True)
    feedback_detailed_description = models.TextField(max_length=5000, blank=True, null=True)

    # create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    # last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class ShippingCharges(models.Model):
    days= models.CharField(max_length=250, blank=True, null=True)
    locationname= models.CharField(max_length=250, blank=True, null=True)
    pincode= models.CharField(max_length=250, blank=True, null=True)
    amount= models.CharField(max_length=250, blank=True, null=True)


class OrderDetails(models.Model):
    delivery_boy=models.ForeignKey(kri8evTeam, on_delete= models.CASCADE,null=True)
    shippingcharges = models.ForeignKey(ShippingCharges, on_delete= models.CASCADE,null=True)
    user   =  models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    total         = models.CharField(max_length=250, blank=True, null=True)
    delivery_status         = models.CharField(max_length=250, blank=True, null=True)

    Address= models.CharField(max_length=250, blank=True, null=True)
    City= models.CharField(max_length=250, blank=True, null=True)
    State= models.CharField(max_length=250, blank=True, null=True)
    Country= models.CharField(max_length=250, blank=True, null=True)
    Pincode= models.CharField(max_length=250, blank=True, null=True)
    street= models.CharField(max_length=250, blank=True, null=True)

    # PaymentDetails = models.ForeignKey(PaymentDetails, on_delete= models.CASCADE,null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class PaymentDetails(models.Model):
    orderdetails =   models.ForeignKey(OrderDetails, on_delete= models.CASCADE,null=True)
    amount        = models.CharField(max_length=250, blank=True, null=True)
    provider = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    payment_id = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp                =   models.DateField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)
    #  Custom_User=models.ForeignKey(Custom_User,on_delete= models.CASCADE,null=True)




# class PaymentDetails(models.Model):
#     # OrderDetails =   models.ForeignKey(OrderDetails, on_delete= models.CASCADE,null=True)
#     amount        = models.CharField(max_length=250, blank=True, null=True)
#     provider = models.CharField(max_length=250, blank=True, null=True)
#     status = models.CharField(max_length=250, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)





class OrderItems(models.Model):
    OrderDetails =   models.ForeignKey(OrderDetails, on_delete= models.CASCADE,null=True)
    Product_ID   = models.ForeignKey(Product, on_delete= models.CASCADE,null=True)
    quantity     = models.CharField(max_length=250, blank=True, null=True)
    size     = models.CharField(max_length=250, blank=True, null=True)

    color     = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class ShoppingSession(models.Model):
    user             =  models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    total                   = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class CartItem(models.Model):
    ShoppingSession   =  models.ForeignKey(ShoppingSession, on_delete= models.CASCADE,null=True)
    Product_ID   = models.ForeignKey(Product, on_delete= models.CASCADE,null=True)
    quantity     = models.CharField(max_length=250, blank=True, null=True)
    selectedoptions = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Buy_NowCartItem(models.Model):
    ShoppingSession   =  models.ForeignKey(ShoppingSession, on_delete= models.CASCADE,null=True)
    Product_ID   = models.ForeignKey(Product, on_delete= models.CASCADE,null=True)
    quantity     = models.CharField(max_length=250, blank=True, null=True)
    selectedoptions = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class LeaderBoardOne(models.Model):
    points          = models.CharField(max_length=250, blank=True, null=True)
    used_code          = models.CharField(max_length=250, blank=True, null=True)
    user             =  models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)




class PromoCode(models.Model):
    # custom_user = models.ForeignKey(Custom_User,on_delete= models.CASCADE,null=True)
    # product = models.ForeignKey(Product,on_delete= models.CASCADE,null=True)
    Code = models.CharField(max_length=250, blank=True, null=True)
    discount = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    marketer_id = models.CharField(max_length=250, blank=True, null=True)
    Expiry_Timestamp=models.DateField(verbose_name="Expiry_Timestamp",blank=True,null=True)
    Create_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete= models.CASCADE,null=True)
    status = models.CharField(max_length=250, blank=True, null=True)

    Create_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    Last_Update_TimeStamp=models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)











class Parent(models.Model):
    user_details = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)



# class UserRoleRef(models.Model):
#     custom_user=models.ForeignKey(Custom_User, on_delete= models.CASCADE ,null=True)
#     user_role_name = models.CharField(max_length=250, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class StateCodeRef(models.Model):
    state_code = models.CharField(max_length=50, blank=True, null=True)
    state_name = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    role = models.ForeignKey(UserRoleRef, on_delete= models.CASCADE,null=True)
    parent = models.ForeignKey(Parent, on_delete= models.CASCADE,null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    fullname = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    terms = models.CharField(max_length=250, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank= True, null= True)
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    my_interest = models.TextField(max_length=500, blank=True, null=True)
    my_hobbies = models.TextField(max_length=500, blank=True, null=True)
    profile_img= models.FileField(upload_to= 'profile_img', blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Course(models.Model):
    course_name = models.CharField(max_length=250, blank=True, null=True)
    course_video = models.CharField(max_length=1050, blank=True, null=True)
    course_description = models.TextField(max_length=5000, blank=True, null=True)
    course_selling_price = models.IntegerField(blank=True, null=True)
    course_discounted_price = models.IntegerField(blank=True, null=True)
    course_final_price = models.IntegerField(blank=True, null=True)
    gst = models.CharField(max_length=50, blank=True, null=True)
    instructor = models.TextField(max_length=5000, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    # what_will_you_get = models.CharField(max_length=500, blank=True, null=True)
    what_will_you_learn = models.CharField(max_length=500, blank=True, null=True)
    enrolled_students_count = models.CharField(max_length=500, blank=True, null=True)
    trailer_link=models.FileField(upload_to= 'trailer_link', blank=True, null=True)

    text = models.CharField(max_length=500, blank=True, null=True)
    course_images=models.FileField(upload_to= 'course_images', blank=True, null=True)
    icon= models.FileField(upload_to= 'course_icon', blank=True, null=True)
    cover_image=models.FileField(upload_to= 'course_cover_images', blank=True, null=True)
    slider_images=models.FileField(upload_to= 'course_slider_images', blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Lesson(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    order_id = models.CharField(max_length=50, blank=True, null=True)
    lesson_name = models.CharField(max_length=250, blank=True, null=True)
    lesson_cover_image = models.FileField(upload_to= 'lesson_cover_image', blank=True, null=True)
    lesson_description = models.TextField(max_length=5000, blank=True, null=True)

    time_duration                =   models.TimeField(auto_now_add=True,verbose_name="Time_Duration",blank=True,null=True)
    lesson_video = models.CharField(max_length=500, blank=True, null=True)
    pre_lesson_id = models.CharField(max_length=200, blank=True, null=True)
    next_lesson_id = models.CharField(max_length=200, blank=True, null=True)
    preview_video = models.CharField(max_length=500, blank=True, null=True)
    # next_lesson_id = models.CharField(max_length=200, blank=True, null=True)
    activity = HTMLField( blank=True, null=True)
    instruction = HTMLField( blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class UserCourse(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    current_lesson_id = models.CharField(max_length=250, blank=True, null=True)
    previous_lesson_id = models.CharField(max_length=250, blank=True, null=True)
    certificate = models.FileField(upload_to= 'user_course_certificate', blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Orders(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    payment_name = models.CharField(max_length=250, blank=True, null=True)
    payment_type = models.CharField(max_length=250, blank=True, null=True)
    order_type = models.CharField(max_length=50, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    delivery_charges = models.IntegerField(blank=True, null=True)
    gst = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=0, blank=True, null=True)


    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)




# class Reviews(models.Model):
#     # course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
#     Custom_User = models.ForeignKey(Custom_User, on_delete= models.CASCADE,null=True)
#     Product_ID= models.ForeignKey(Product, on_delete= models.CASCADE,null=True)
#     reviewMessage = models.CharField(max_length=500, blank=True, null=True)
#     star_rating = models.CharField(max_length=20, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    postDetails = models.CharField(max_length=250, blank=True, null=True)
    post_image = models.FileField(upload_to= 'post_images', blank=True, null=True)
    post_video = models.FileField(upload_to= 'post_video', blank=True, null=True)
    status = models.BooleanField(default=1,blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    post = models.ForeignKey(Post, on_delete= models.CASCADE,null=True)
    commentsDetails = models.CharField(max_length=500, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


# class FAQs(models.Model):
#     # course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
#     # lesson = models.ForeignKey(Lesson, on_delete= models.CASCADE,null=True)
#     # user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
#     faq_name = models.CharField(max_length=250, blank=True, null=True)
#     # faq_type = models.CharField(max_length=250, blank=True, null=True)
#     description = models.TextField(max_length=5000, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


# class Leaderboard(models.Model):
#     user = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
#     points = models.CharField(max_length=250, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class RegisterationCode(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    no_of_code= models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=5000, blank=True, null=True)
    # discount = models.CharField(max_length=100, blank=True, null=True)
    # expiry_timestamp                =   models.TimeField(auto_now_add=False,verbose_name="Expiry_timestamp",blank=True,null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)



# class PromoCode(models.Model):
#     course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
#     promo_code_name = models.CharField(max_length=250, blank=True, null=True)
#     discount = models.CharField(max_length=100, blank=True, null=True)
#     expiry_timestamp                =   models.TimeField(auto_now_add=False,verbose_name="Expiry_timestamp",blank=True,null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Enquiry(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    school = models.CharField(max_length=250, blank=True, null=True)
    comment = models.CharField(max_length=250, blank=True, null=True)
    enquiry_type = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


# class Testimonials(models.Model):
#     name = models.CharField(max_length=250, blank=True, null=True)
#     category = models.CharField(max_length=250, blank=True, null=True)
#     image = models.FileField(upload_to= 'testimonials_images', blank=True, null=True)
#     video = models.FileField(upload_to= 'testimonials_video', blank=True, null=True)
#     rating = models.CharField(max_length=20, blank=True, null=True)

#     feedback_small_description = models.TextField(max_length=2000, blank=True, null=True)
#     feedback_detailed_description = models.TextField(max_length=5000, blank=True, null=True)

#     # create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     # last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Announcement(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)

    instructor_name = models.CharField(max_length=100, blank=True, null=True)
    agenda = models.CharField(max_length=250, blank=True, null=True)
    image = models.FileField(upload_to='announcement_images', blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    description = models.TextField(max_length=1000, blank=True, null=True)
    type_of_announcement = models.CharField(max_length=200, blank=True, null=True)
    recorded_link = models.CharField(max_length=500, blank=True, null=True)

    time_of_the_event                =   models.TimeField(auto_now_add=False,verbose_name="time_of_the_event",blank=True,null=True)
    day_of_the_event           =   models.DateField(auto_now_add=False,verbose_name="day_of_the_event",blank=True,null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class SpotlytTeam(models.Model):
    role=models.ForeignKey(UserRoleRef, on_delete= models.CASCADE ,null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    mobile_number = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Course_survey(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    survey_name = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Survey_question(models.Model):
    coursesurvey=models.ForeignKey(Course_survey, on_delete= models.CASCADE ,null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    # description = models.TextField(max_length=1000, blank=True, null=True)
    # instruction = models.CharField(max_length=500, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class Question_choice(models.Model):
    surveyquestion=models.ForeignKey(Survey_question, on_delete= models.CASCADE ,null=True)
    option1 = models.CharField(max_length=100, blank=True, null=True)
    option2 = models.CharField(max_length=100, blank=True, null=True)
    option3 = models.CharField(max_length=100, blank=True, null=True)
    option4 = models.CharField(max_length=100, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Notification(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=2000, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Student_update(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True)
    image = models.FileField(upload_to='student_update_images_video', blank=True, null=True)
    type_of_update = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class ActiveCourse(models.Model):
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class FAQsQuery(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True)
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    lesson=models.ForeignKey(Lesson, on_delete= models.CASCADE ,null=True)
    query_name = models.CharField(max_length=500, blank=True, null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

class What_will_you_get(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True)
    course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True)
    image= models.FileField(upload_to= 'what_will_you_get_image', blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)

# class Survey_answer(models.Model):
#     user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True,related_name='spotlytuser')
#     course=models.ForeignKey(Course, on_delete= models.CASCADE ,null=True,related_name='spotlytcourse')
#     coursesurvey=models.ForeignKey(Course_survey, on_delete= models.CASCADE ,null=True,related_name='spotlytcoursesurvey')
#     surveyquestion=models.ForeignKey(Survey_question, on_delete= models.CASCADE ,null=True,related_name='spotlytsurveyquestion')
#     answer = models.CharField(max_length=500, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Subscribe (models.Model):
    email = models.EmailField(max_length=100, blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Certificate_image(models.Model):
    image1 = models.FileField(upload_to= 'post_images', blank=True, null=True)
    barcode = models.FileField(upload_to= 'post_images', blank=True, null=True)
    certificate_bg = models.FileField(upload_to= 'post_images', blank=True, null=True)
    rakhsith = models.FileField(upload_to= 'post_images', blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


class Deal_of_the_day(models.Model):
    product_category= models.ForeignKey(Product_Category,on_delete=models.CASCADE, blank=True, null=True)

    product=models.ForeignKey(Product, on_delete= models.CASCADE ,null=True)

    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)



class Slide_Image(models.Model):
    product=models.ForeignKey(Product, on_delete= models.CASCADE ,null=True)
    image= models.FileField(upload_to= 'Slide_Image', blank=True, null=True)
    create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)



class User_PromoDetails(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,null=True)
    orderdetails =   models.ForeignKey(OrderDetails, on_delete= models.CASCADE,null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    discount = models.CharField(max_length=250, blank=True, null=True)

    status = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.CharField(max_length=250, blank=True, null=True)
    Expiry_Timestamp=models.DateField(verbose_name="Expiry_Timestamp",blank=True,null=True)


#
# class Team_Config(models.Model):
#     role = models.ForeignKey(UserRoleRef,on_delete=models.CASCADE, blank=True, null=True)
#     salary = models.CharField(max_length=250, blank=True, null=True)
#     bonus= models.CharField(max_length=250, blank=True, null=True)
#     incentives= models.CharField(max_length=250, blank=True, null=True)
#     create_timestamp                =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)





class Marketer_sales(models.Model):
    orders= models.ForeignKey(OrderDetails,on_delete=models.CASCADE, blank=True, null=True)
    marketer_id = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    sale_amt = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp                =   models.DateField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)


#
# class Marketer_salary(models.Model):
#     marketer_id = models.CharField(max_length=250, blank=True, null=True)
#     salary = models.CharField(max_length=250, blank=True, null=True)
#
#     create_timestamp                =   models.DateField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
#     last_update_timestamp           =   models.DateTimeField(auto_now_add=True,verbose_name="Last_Update_TimeStamp",blank=True,null=True)
