from django.core import paginator
from django.shortcuts import render
from django.contrib.auth.models import User
from requests.api import request
from .serializers import UserSerializer, CustUserSerializer
from .serializers import *
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
# from rest_framework.decorators import api_view
import razorpay

from django.conf import settings
from django.core.mail import message, send_mail, EmailMessage

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from datetime import datetime
from datetime import timedelta
from datetime import datetime,date,time
import time
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
import requests
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
import inspect
import random
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from spotlytapp.backends import *
from rest_framework_simplejwt.tokens import RefreshToken
import base64

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#
# from razorpay.models import *
###########################Email Verifications#############################




from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator
# Create your views here.


class ProductCategoryView(APIView):
    # queryset = Product_Category.objects.all().values()
    def get(self,request):
        id =self.request.query_params.get('id')
        arr=[]
        if id:
            all_values = Product_Category.objects.filter(id=id)
            for i in all_values:
                arr.append({
                'id':i.id,
                'image':str(i.image),
                'Product_Category_Name':i.Product_Category_Name,
                'Product_Category_Description':i.Product_Category_Description,
                'Create_TimeStamp':i.Create_TimeStamp,
                })
            return Response(arr)
        else:
            count=0
            quantity=0
            total_amount=0
            total_number=0

            all_values = Product_Category.objects.all()
            for i in all_values:
                pro_count=Product.objects.filter(Product_Category_id=i.id).count()
                product=Product.objects.filter(Product_Category_id=i.id)
                price=0
                for j in product:
                    price=int(j.Product_Selling_Price)
                    order=OrderItems.objects.filter(Product_ID_id=j.id)
                    for k in order:
                        quantity=quantity+int(k.quantity)
                sale_count=OrderItems.objects.all().count()
                percentage=quantity/sale_count*100
                # total_amount= 'total_amount '+str(int(price*quantity))
                # total_number= 'total_number '+str(quantity)
                arr.append({
                'id':i.id,
                'image':str(i.image),
                'Product_Category_Name':i.Product_Category_Name,
                'Product_Category_Description':i.Product_Category_Description,
                'Create_TimeStamp':i.Create_TimeStamp,
                'total_number':quantity,
                # 'total_number':total_number,
                'total_amount':int(price*quantity)
                # 'total_amount':total_amount
                # 'percentage':percentage
                })

            return Response(arr)

    def post(self,request):
        data = request.data
        Product_Category_Name = data.get('product_category_name')
        Product_Category_Description=data.get('product_category_description')
        image=data.get('image')


        count=str(random.randint(100,9999999))
        split_base_url_data = image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = '/kri8eve/site/public/media/product_category_image/'+count+'.png'
        fname1 = '/media/product_category_image/'+count+'.png'
        ss=  open(filename1, 'wb')
        ss.write(imgdata1)
        ss.close()



        create_create=Product_Category.objects.create(Product_Category_Name=Product_Category_Name.title(),Product_Category_Description=Product_Category_Description,image=fname1)

        return JsonResponse({'result':'Created'})

    def put(self,request,pk):
        data = request.data
        Product_Category_Name = data.get('product_category_name')
        Product_Category_Description=data.get('product_category_description')
        image=data.get('image')

        if image !=None:
            count=str(random.randint(100,9999999))
            split_base_url_data = image.split(';base64,')[1]
            imgdata1 = base64.b64decode(split_base_url_data)
            filename1 = '/kri8eve/site/public/media/product_category_image/'+count+'.png'
            fname1 = '/media/product_category_image/'+count+'.png'
            ss=  open(filename1, 'wb')
            ss.write(imgdata1)
            ss.close()





            data= Product_Category.objects.filter(id=pk).update(Product_Category_Name=Product_Category_Name.title(),Product_Category_Description=Product_Category_Description,image=fname1)



            return Response({'result':'Updated successfully'})
        else:
            data= Product_Category.objects.filter(id=pk).update(Product_Category_Name=Product_Category_Name,Product_Category_Description=Product_Category_Description)
            return Response({'result':'Updated successfully'})


    def delete(self,request,pk):
        all_values = Product_Category.objects.filter(id=pk).delete()
        return Response(all_values)


class Product_Sub_CategoryAPIView(APIView):
    def get(self, request):
        id =self.request.query_params.get('id')
        category_id =self.request.query_params.get('category_id')
        arr=[]
        if category_id:
            quantity=0
            product_sub_data = Product_Sub_Category.objects.filter(product_category_id=category_id)
            for i in product_sub_data:
                pro_count=Product.objects.filter(product_sub_category=i.id).count()
                product=Product.objects.filter(product_sub_category=i.id)
                price=0
                for j in product:
                    price=int(j.Product_Selling_Price)

                    order=OrderItems.objects.filter(Product_ID_id=j.id)
                    for k in order:
                        quantity=quantity+int(k.quantity)
                sale_count=OrderItems.objects.all().count()
                # percentage=quantity/sale_count*100
                arr.append({
                'Create_TimeStamp': i.Create_TimeStamp,
                'id': i.id,
                'image':str(i.image),
                'product_category_id': i.product_category_id,
                'product_category_name': i.product_category.Product_Category_Name,
                'product_sub_category_Description':i.product_sub_category_Description,
                'product_sub_category_name':i.product_sub_category_name,
                'total_number':quantity,
                'total_amount':int(price*quantity)
                })
            return Response(arr)

        if id:
            product_sub_data = Product_Sub_Category.objects.filter(id=id).values()
            # paginator = Paginator(product_sub_data, 10)
            # try:
            #     paginator_data = paginator.page(page_no)
            # except PageNotAnInteger:
            #     paginator_data = paginator.page(1)
            # except EmptyPage:
            #     print('except')
            #     paginator_data = paginator.page(paginator.num_pages)
            # return JsonResponse({"Data": list(paginator_data)})
            return Response(product_sub_data)
        else:
            product_sub_data = Product_Sub_Category.objects.all().values()
            # paginator = Paginator(product_sub_data, 10)
            # try:
            #     paginator_data = paginator.page(page_no)
            # except PageNotAnInteger:
            #     paginator_data = paginator.page(1)
            # except EmptyPage:
            #     print('except')
            #     paginator_data = paginator.page(paginator.num_pages)
            # return JsonResponse({"Data": list(paginator_data)})
            return Response(product_sub_data)



    def post(self, request):
        data = request.data
        # user_id = data.get('user_id')
        sub_category_id = data.get('category_id')
        product_sub_category_name = data.get('product_sub_category_name')
        product_sub_category_Description = data.get('product_sub_category_Description')
        image=data.get('image')
        count=str(random.randint(100,9999999))
        split_base_url_data = image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = '/kri8eve/site/public/media/product_sub_category_image/'+count+'.png'
        fname1 = '/media/product_sub_category_image/'+count+'.png'
        ss=  open(filename1, 'wb')
        ss.write(imgdata1)
        ss.close()

        # user_check = User.objects.filter(id= user_id)
        # if user_check:
        product_create = Product_Sub_Category.objects.create(product_category_id=sub_category_id,product_sub_category_name=product_sub_category_name,product_sub_category_Description=product_sub_category_Description,image=fname1)
        return Response("Data Added Sucessfully")

        # else:
        #     response={'message': 'Valid Id Required'}
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk):
        data = request.data

        sub_category_id = data.get('category_id')
        product_sub_category_name = data.get('product_sub_category_name')
        product_sub_category_Description = data.get('product_sub_category_Description')
        image=data.get('image')

        if image !=None:

            count=str(random.randint(100,9999999))
            split_base_url_data = image.split(';base64,')[1]
            imgdata1 = base64.b64decode(split_base_url_data)
            filename1 = '/kri8eve/site/public/media/product_sub_category_image/'+count+'.png'
            fname1 = '/media/product_sub_category_image/'+count+'.png'
            ss=  open(filename1, 'wb')
            ss.write(imgdata1)
            ss.close()



            data = Product_Sub_Category.objects.filter(id=pk).update(product_category_id=sub_category_id,
                                                                    product_sub_category_name=product_sub_category_name,
                                                                    product_sub_category_Description=product_sub_category_Description,
                                                                    image=fname1,)

            return JsonResponse({'message': 'product_sub_data Updated Sucessfully.'})

        else:
            data = Product_Sub_Category.objects.filter(id=pk).update(product_category_id=sub_category_id,
                                                                    product_sub_category_name=product_sub_category_name,
                                                                    product_sub_category_Description=product_sub_category_Description)
            return JsonResponse({'message': 'product_sub_data Updated Sucessfully.'})


    def delete(self, request,pk):

        product_sub_data =Product_Sub_Category.objects.filter(id= pk).delete()
        return Response("product_sub_data Deleted Sucessfully")





class ProductInventorApi(APIView):
    queryset = Product_Inventory.objects.all().values()
    def get(self,request):
        all_values = Product_Inventory.objects.all().values()
        return Response(all_values)

    def post(self,request):
        data = request.data
        Quantity = data.get('Quantity')
        Create_TimeStamp=data.get('Create_TimeStamp')
        Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')



        selected_page_no = 1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        if Product_Inventory.objects.filter(Quantity=Quantity).exists():
            return Response({'result':'Already Exists'})
        else:
            Product_Inventory.objects.create(Quantity=Quantity,Create_TimeStamp=Create_TimeStamp,
                                            Last_Update_TimeStamp=Last_Update_TimeStamp)

            posts = Product_Inventory.objects.all().values()
            paginator=Paginator(posts,3)

            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            # return JsonResponse({'data':list(page_obj)})
            return Response({'result':'Created','data':list(page_obj)})

    def put(self,request,pk):
        data = request.data
        Quantity = data.get('Quantity')
        Create_TimeStamp=data.get('Create_TimeStamp')
        Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')

        if Product_Inventory.objects.filter(Quantity=Quantity).exists():
            return Response({'result':'Already Exists'})
        else:
            Product_Inventory.objects.filter(id=pk).update(Quantity=Quantity,Create_TimeStamp=Create_TimeStamp,
                                            Last_Update_TimeStamp=Last_Update_TimeStamp)

            return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = Product_Inventory.objects.filter(id=pk).delete()
        return Response(all_values)


class DiscountApi(APIView):
    # queryset = Discount.objects.all().values()
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            all_values = Discount.objects.filter(id=id).values()
            return Response(all_values)
        else:
            all_values = Discount.objects.all().values()
            return Response(all_values)

    def post(self,request):
        data=request.data
        Discount_Name=data.get('discount_name')
        Discount_Description=data.get('discount_description')
        Discount_Percentage=data.get('discount_percentage')
        Status=data.get('status')
        start_date=data.get('start_date')
        end_date=data.get('end_date')
        # Create_TimeStamp=data.get('Create_TimeStamp')
        # Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')




        data_create=Discount.objects.create(Discount_Name=Discount_Name,Discount_Description=Discount_Description,Discount_Percentage=Discount_Percentage,
                                   Status=Status,start_date=start_date,end_date=end_date)


        return Response({'result':'Discount Created successfully'})

    def put(self,request,pk):
        data=request.data
        Discount_Name=data.get('discount_name')
        Discount_Description=data.get('discount_description')
        Discount_Percentage=data.get('discount_percentage')
        Status=data.get('status')
        start_date=data.get('start_date')
        end_date=data.get('end_date')



        data=Discount.objects.filter(id=pk).update(Discount_Name=Discount_Name,Discount_Description=Discount_Description,Discount_Percentage=Discount_Percentage,
                                   Status=Status,start_date=start_date,end_date=end_date)

        return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = Discount.objects.filter(id=pk).delete()
        return Response(all_values)



class Delete_slideImageApiView(APIView):
    def delete(self,request,pk):
        all_values = Slide_Image.objects.filter(id=pk).delete()
        return Response({'result':'Deleted'})


class Delete_attributeApiView(APIView):
    def delete(self,request,pk):
        all_values = AttributeOptions.objects.filter(id=pk).delete()
        return Response({'result':'Deleted'})


class Edit_productApiView(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        Arr=[]
        Arrs=[]
        Arrss=[]
        opt=[]
        image=''
        Product_Category_Name=''
        product_sub_category_name=''
        ps_image=''
        brand_name=''

        if id:


            all_values = Product.objects.filter(id=id).values()
            for i in all_values:


                brand=Brand.objects.filter(id=i['brand_id'])
                for k in brand:
                    brand_name=k.brand_name
                p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                for l in p_category:
                    Product_Category_Name=l.Product_Category_Name
                    image=str(l.image)

                ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                for m in ps_category:
                    product_sub_category_name=m.product_sub_category_name
                    ps_image=str(m.image)

                res={}
                # res['rating']=avg
                # res['review_count']=count
                # count=0
                res['id']=i['id']
                res['brand_name']=brand_name
                res['brand_id']=i['brand_id']
                res['Product_Name']=i['Product_Name']
                res['Product_Description']=i['Product_Description']
                res['Product_Image']=i['Product_Image']
                res['Product_Video']=i['Product_Video']
                res['Product_Selling_Price']=i['Product_Selling_Price']
                res['Gst']=i['Gst']
                res['Product_Listed_Price']=i['Product_Listed_Price']
                res['Product_Details']=i['Product_Details']
                res['Status']=i['Status']
                res['Create_TimeStamp']=i['Create_TimeStamp']
                res['HSN_SAC_Code']=i['HSN_SAC_Code']
                res['Wash_instructions']=i['Wash_instructions']
                res['Product_Category']=i['Product_Category_id']
                res['category_image']=image
                res['Product_Category_Name']=Product_Category_Name
                res['product_sub_category']=i['product_sub_category_id']
                res['product_sub_category_name']=product_sub_category_name
                res['sub_category_image']=ps_image

                res['attribute_color']=[]
                res['attribute_size']=[]
                res['slider_image']=[]

                res['attribute']=[]

                item=Attributes.objects.filter(Product_ID_id=i['id'])
                for k in item:
                    id=k.id
                    name=k.name
                    res['attribute'].append({
                    'id':k.id,
                    'name':k.name,
                    'options':[]
                    })

                    option=AttributeOptions.objects.filter(attributes_id=id)
                    for j in option:
                        for l in range(len(res['attribute'])):
                            e=(list(res['attribute'][l].values()))
                            des=e[2]

                        des.append({
                        'option_id':j.id,
                        'option':j.option,

                        })
                Arrss.append(res)







                item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                for k in item:
                    id=k.id

                    option=AttributeOptions.objects.filter(attributes_id=id)
                    option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                    # res['color_count']=option_count
                    for j in option:

                        res['attribute_color'].append({
                        'option_id':j.id,
                        'option':j.option,

                        })
                Arrss.append(res)

                item=Attributes.objects.filter(Product_ID_id=i['id'],name='Size')
                for k in item:
                    id=k.id

                    option=AttributeOptions.objects.filter(attributes_id=id)
                    option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                    # res['color_count']=option_count
                    for j in option:

                        res['attribute_size'].append({
                        'option_id':j.id,
                        'option':j.option,

                        })
                Arr.append(res)

                slider_image_data = Slide_Image.objects.filter(product_id=i['id'])
                for j in slider_image_data:
                    type=str(j.image).split('.')
                    # if str(type[1])=='png' or str(type[1])=='jpeg' or str(type[1])=='jpg':
                    res['slider_image'].append({
                        'id':j.id,
                        'image':str(j.image),
                        'file_type':str(type[1])
                    })
                Arrs.append(res)
            return Response(Arr)


    def put(self,request,pk):
        data = request.data
        Product_Name=data.get('Product_Name')
        Product_Description=data.get('Product_Description')
        Product_Image=data.get('Product_Image')
        Product_Video=data.get('Product_Video')
        Product_Selling_Price=data.get('Product_Selling_Price')
        GST=data.get('GST')
        Product_Listed_Price=data.get('Product_Listed_Price')
        Status=data.get('Status')
        Product_Details=data.get('Product_Details')

        HSN_SAC_Code=data.get('HSN_SAC_Code')
        Wash_instructions=data.get('Wash_instructions')
        Product_Category_ID=data.get('Product_Category_id')
        Product_Inventory_ID=data.get('Product_Inventory_id')
        product_sub_category=data.get('product_sub_category')
        brand_id=data.get('brand_id')
        discount_id=data.get('discount_id')
        what_will_you_get=data.get('slide_images')
        print(what_will_you_get,';;;;;;')


        Arr=[]
        if Product_Image:
            count=str(random.randint(100,9999999))
            split_base_url_data = Product_Image.split(';base64,')[1]
            imgdata1 = base64.b64decode(split_base_url_data)
            filename1 = '/kri8eve/site/public/media/Product_Image/'+count+'.png'
            fname1 = '/media/Product_Image/'+count+'.png'
            ss=  open(filename1, 'wb')
            ss.write(imgdata1)
            ss.close()


            data_crete=Product.objects.filter(id=pk).update(Product_Name=Product_Name,
                                    Product_Description=Product_Description,
                                    Product_Image=fname1,
                                    Product_Video=Product_Video,
                                    Product_Selling_Price=Product_Selling_Price,
                                    Gst=GST,
                                    Product_Listed_Price=Product_Listed_Price,
                                    Status=Status,
                                    Product_Details=Product_Details,
                                    HSN_SAC_Code=HSN_SAC_Code,
                                    Wash_instructions=Wash_instructions,
                                    Product_Category_id=Product_Category_ID,
                                    product_sub_category_id=product_sub_category,
                                    Product_Inventory_id=Product_Inventory_ID,
                                    brand_id=brand_id,Discount_id=discount_id)
            slide_create = Slide_Image.objects.create(product_id=pk,image=fname1)
            details = data.get('attribute_details')
            print(details,'details')
            for l in range(len(details)):
                e=(list(details[l].values()))
                print(e[0],'00')
                print(e[1],'11')

                # att=Attributes.objects.filter(Product_ID_id=pk).update(name=e[0])
                att=Attributes.objects.get(Product_ID_id=pk,name=e[0])

                # last_product = Attributes.objects.all().order_by('-id')[0]



                for j in e[1]:
                    opt=AttributeOptions.objects.create(attributes_id=att.id,option=j)


            if what_will_you_get:
                for k in range(len(what_will_you_get)):
                    e=(list(what_will_you_get[k].values()))
                    img=e[0]
                    file_type=e[1]
                    type=file_type.split('.')
                    # print(des,'dddd')
                    if str(type[1])=='mp4'or str(type[1])=='MOV' or str(type[1])=='MKV' or str(type[1])=='AVI':
                        count=str(random.randint(100,9999999))
                        split_base_url_data = img.split(';base64,')[1]
                        imgdata4 = base64.b64decode(split_base_url_data)
                        filename1 = '/kri8eve/site/public/media/Slide_Image/'+count+'.mp4'
                        fname1 = '/media/Slide_Image/'+count+'.mp4'
                        ss=  open(filename1, 'wb')
                        ss.write(imgdata4)
                        ss.close()
                        what_will_you_get_create = Slide_Image.objects.create(product_id=pk,image=fname1)

                    else:

                        count=str(random.randint(100,9999999))
                        split_base_url_data = img.split(';base64,')[1]
                        imgdata4 = base64.b64decode(split_base_url_data)
                        filename1 = '/kri8eve/site/public/media/Slide_Image/'+count+'.png'
                        fname1 = '/media/Slide_Image/'+count+'.png'
                        ss=  open(filename1, 'wb')
                        ss.write(imgdata4)
                        ss.close()
                        what_will_you_get_create = Slide_Image.objects.create(product_id=pk,image=fname1)

                return Response("Data Added Sucessfully")
            else:
                return Response("Data Added Sucessfully")
        else:
            data_crete=Product.objects.filter(id=pk).update(Product_Name=Product_Name,
                                    Product_Description=Product_Description,
                                    # Product_Image=fname1,
                                    Product_Video=Product_Video,
                                    Product_Selling_Price=Product_Selling_Price,
                                    Gst=GST,
                                    Product_Listed_Price=Product_Listed_Price,
                                    Status=Status,
                                    Product_Details=Product_Details,
                                    HSN_SAC_Code=HSN_SAC_Code,
                                    Wash_instructions=Wash_instructions,
                                    Product_Category_id=Product_Category_ID,
                                    product_sub_category_id=product_sub_category,
                                    Product_Inventory_id=Product_Inventory_ID,
                                    brand_id=brand_id,Discount_id=discount_id)
            # slide_create = Slide_Image.objects.create(product_id=data_crete.id,image=fname1)
            details = data.get('attribute_details')
            print(details,'details')
            for l in range(len(details)):
                e=(list(details[l].values()))
                print(e[0],'00')
                print(e[1],'11')

                # att=Attributes.objects.filter(Product_ID_id=pk).update(name=e[0])
                att=Attributes.objects.get(Product_ID_id=pk,name=e[0])

                # last_product = Attributes.objects.all().order_by('-id')[0]

                for j in e[1]:
                    opt=AttributeOptions.objects.create(attributes_id=att.id,option=j)


            if what_will_you_get:
                for k in range(len(what_will_you_get)):
                    e=(list(what_will_you_get[k].values()))
                    img=e[0]
                    file_type=e[1]
                    type=file_type.split('.')
                    # print(des,'dddd')
                    if str(type[1])=='mp4'or str(type[1])=='MOV' or str(type[1])=='MKV' or str(type[1])=='AVI':
                        count=str(random.randint(100,9999999))
                        split_base_url_data = img.split(';base64,')[1]
                        imgdata4 = base64.b64decode(split_base_url_data)
                        filename1 = '/kri8eve/site/public/media/Slide_Image/'+count+'.mp4'
                        fname1 = '/media/Slide_Image/'+count+'.mp4'
                        ss=  open(filename1, 'wb')
                        ss.write(imgdata4)
                        ss.close()
                        what_will_you_get_create = Slide_Image.objects.create(product_id=pk,image=fname1)

                    else:

                        count=str(random.randint(100,9999999))
                        split_base_url_data = img.split(';base64,')[1]
                        imgdata4 = base64.b64decode(split_base_url_data)
                        filename1 = '/kri8eve/site/public/media/Slide_Image/'+count+'.png'
                        fname1 = '/media/Slide_Image/'+count+'.png'
                        ss=  open(filename1, 'wb')
                        ss.write(imgdata4)
                        ss.close()
                        what_will_you_get_create = Slide_Image.objects.create(product_id=pk,image=fname1)

                return Response("Data Added Sucessfully")
            else:
                return Response("Data Added Sucessfully")










class ProductApiView(APIView):
    # queryset = Product.objects.all().values()
    def get(self,request):
        id = request.query_params.get('id')
        user_id = request.query_params.get('user_id')
        Arr=[]
        Arrs=[]
        opt=[]
        image=''
        dis_percent=0
        total_rating=0
        Product_Category_Name=''
        product_sub_category_name=''
        ps_image=''
        total_rating=0
        avg=0
        brand_name=''

        if id != 'null' and user_id =='null':
            print('lllllll')
            count=0
            rating_counts =Reviews.objects.filter(Product_ID_id=id)
            for j in rating_counts:
                if j.reviewMessage:
                    count=count+1
            rating_count =Reviews.objects.filter(Product_ID_id=id).count()
            rating =Reviews.objects.filter(Product_ID_id=id)
            if rating_count>0:
                for k in rating:
                    if k.star_rating!='':

                        total_rating=total_rating+int(k.star_rating)
                    else:
                        total_rating=0
                avg=int(total_rating)/int(rating_count)
            else:
                avg=0
            total_rating=0
            rating_count=0

            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:
                all_values = Product.objects.filter(id=id).values()
                for i in all_values:
                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    for b in dis:
                        dis_percent=dis_percent+int(b.Discount_Percentage)
                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                    f_price=float(i['Product_Selling_Price'])-after_discount
                    dis_percent=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=f_price
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    res['rating']=avg
                    res['review_count']=count
                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    # if wishlist:
                    #     res['wishlist']=True
                    res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]
                    res['slider_image']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)

                    slider_image_data = Slide_Image.objects.filter(product_id=i['id'])
                    for j in slider_image_data:
                        type=str(j.image).split('.')
                        if str(type[1])=='png' or str(type[1])=='jpeg' or str(type[1])=='jpg':
                            res['slider_image'].append({
                                'id':j.id,
                                'image':str(j.image),
                                'file_type':str(type[1])
                            })
                    Arrs.append(res)
                return Response(Arr)
            else:
                count=0
                rating_counts =Reviews.objects.filter(Product_ID_id=id)
                for j in rating_counts:
                    if j.reviewMessage:
                        count=count+1
                all_values = Product.objects.filter(id=id).values()
                for i in all_values:

                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['review_count']=count
                    count=0
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=i['Product_Selling_Price']
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    # if wishlist:
                    #     res['wishlist']=True
                    res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]
                    res['slider_image']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)

                    slider_image_data = Slide_Image.objects.filter(product_id=i['id'])
                    for j in slider_image_data:
                        type=str(j.image).split('.')
                        if str(type[1])=='png' or str(type[1])=='jpeg' or str(type[1])=='jpg':
                            res['slider_image'].append({
                                'id':j.id,
                                'image':str(j.image),
                                'file_type':str(type[1])
                            })
                    Arrs.append(res)
                return Response(Arr)





        if id and user_id:
            print(' need')
            count=0
            rating_counts =Reviews.objects.filter(Product_ID_id=id)
            for j in rating_counts:
                if j.reviewMessage:
                    count=count+1
            rating_count =Reviews.objects.filter(Product_ID_id=id).count()
            rating =Reviews.objects.filter(Product_ID_id=id)
            if rating_count>0:
                for k in rating:
                    if k.star_rating !='':

                        total_rating=total_rating+int(k.star_rating)
                    else:
                        total_rating=0
                avg=int(total_rating)/int(rating_count)
            else:
                avg=0
            total_rating=0
            rating_count=0

            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:
                all_values = Product.objects.filter(id=id).values()
                for i in all_values:
                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    for b in dis:
                        dis_percent=dis_percent+int(b.Discount_Percentage)
                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                    f_price=float(i['Product_Selling_Price'])-after_discount
                    dis_percent=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=f_price
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    res['rating']=avg
                    res['review_count']=count
                    wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    if wishlist:
                        res['wishlist']=True
                    else:
                        res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]
                    res['slider_image']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option.title(),

                            })
                    Arr.append(res)

                    slider_image_data = Slide_Image.objects.filter(product_id=i['id'])
                    for j in slider_image_data:
                        type=str(j.image).split('.')
                        if str(type[1])=='png' or str(type[1])=='jpeg' or str(type[1])=='jpg':
                            res['slider_image'].append({
                                'id':j.id,
                                'image':str(j.image),
                                'file_type':str(type[1])
                            })
                    Arrs.append(res)
                return Response(Arr)
            else:
                count=0
                rating_counts =Reviews.objects.filter(Product_ID_id=id)
                for j in rating_counts:
                    if j.reviewMessage:
                        count=count+1
                all_values = Product.objects.filter(id=id).values()
                for i in all_values:

                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['review_count']=count
                    count=0
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=i['Product_Selling_Price']
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    if wishlist:
                        res['wishlist']=True
                    else:
                        res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]
                    res['slider_image']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option.title(),

                            })
                    Arr.append(res)

                    slider_image_data = Slide_Image.objects.filter(product_id=i['id'])
                    for j in slider_image_data:
                        type=str(j.image).split('.')
                        if str(type[1])=='png' or str(type[1])=='jpeg' or str(type[1])=='jpg':
                            res['slider_image'].append({
                                'id':j.id,
                                'image':str(j.image),
                                'file_type':str(type[1])
                            })
                    Arrs.append(res)
                return Response(Arr)


        else:
            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:
                all_values = Product.objects.all().values()
                for i in all_values:
                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    for b in dis:
                        dis_percent=dis_percent+int(b.Discount_Percentage)
                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                    f_price=float(i['Product_Selling_Price'])-after_discount
                    dis_percent=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=f_price
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    # if wishlist:
                    #     res['wishlist']=True
                    res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)


                return Response(Arr)
            else:
                all_values = Product.objects.all().values()
                for i in all_values:
                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=i['Product_Selling_Price']
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    # if wishlist:
                    #     res['wishlist']=True
                    res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)
                return Response(Arr)



    def post(self,request):
        data = request.data
        Product_Name=data.get('Product_Name')
        Product_Description=data.get('Product_Description')
        Product_Image=data.get('Product_Image')
        Product_Video=data.get('Product_Video')
        Product_Selling_Price=data.get('Product_Selling_Price')
        GST=data.get('GST')
        Product_Listed_Price=data.get('Product_Listed_Price')
        Status=data.get('Status')
        Product_Details=data.get('Product_Details')

        HSN_SAC_Code=data.get('HSN_SAC_Code')
        Wash_instructions=data.get('Wash_instructions')
        Product_Category_ID=data.get('Product_Category_id')
        Product_Inventory_ID=data.get('Product_Inventory_id')
        product_sub_category=data.get('product_sub_category')
        brand_id=data.get('brand_id')
        discount_id=data.get('discount_id')
        what_will_you_get=data.get('slide_images')
        print(what_will_you_get,';;;;;;')


        Arr=[]
        count=str(random.randint(100,9999999))
        split_base_url_data = Product_Image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = '/kri8eve/site/public/media/Product_Image/'+count+'.png'
        fname1 = '/media/Product_Image/'+count+'.png'
        ss=  open(filename1, 'wb')
        ss.write(imgdata1)
        ss.close()


        data_crete=Product.objects.create(Product_Name=Product_Name,
                                Product_Description=Product_Description,
                                Product_Image=fname1,
                                Product_Video=Product_Video,
                                Product_Selling_Price=Product_Selling_Price,
                                Gst=GST,
                                Product_Listed_Price=Product_Listed_Price,
                                Status=Status,
                                Product_Details=Product_Details,
                                HSN_SAC_Code=HSN_SAC_Code,
                                Wash_instructions=Wash_instructions,
                                Product_Category_id=Product_Category_ID,
                                product_sub_category_id=product_sub_category,
                                Product_Inventory_id=Product_Inventory_ID,
                                brand_id=brand_id,Discount_id=discount_id)
        slide_create = Slide_Image.objects.create(product_id=data_crete.id,image=fname1)
        details = data.get('attribute_details')
        print(details,'details')
        for l in range(len(details)):
            e=(list(details[l].values()))
            print(e[0],'00')
            print(e[1],'11')

            att=Attributes.objects.create(Product_ID_id=data_crete.id,name=e[0])
            for j in e[1]:
                opt=AttributeOptions.objects.create(attributes_id=att.id,option=j)


        if what_will_you_get:
            for k in range(len(what_will_you_get)):
                e=(list(what_will_you_get[k].values()))
                img=e[0]
                file_type=e[1]
                type=file_type.split('.')
                # print(des,'dddd')
                if str(type[1])=='mp4'or str(type[1])=='MOV' or str(type[1])=='MKV' or str(type[1])=='AVI':
                    count=str(random.randint(100,9999999))
                    split_base_url_data = img.split(';base64,')[1]
                    imgdata4 = base64.b64decode(split_base_url_data)
                    filename1 = '/kri8eve/site/public/media/Slide_Image/'+count+'.mp4'
                    fname1 = '/media/Slide_Image/'+count+'.mp4'
                    ss=  open(filename1, 'wb')
                    ss.write(imgdata4)
                    ss.close()
                    what_will_you_get_create = Slide_Image.objects.create(product_id=data_crete.id,image=fname1)

                else:

                    count=str(random.randint(100,9999999))
                    split_base_url_data = img.split(';base64,')[1]
                    imgdata4 = base64.b64decode(split_base_url_data)
                    filename1 = '/kri8eve/site/public/media/Slide_Image/'+count+'.png'
                    fname1 = '/media/Slide_Image/'+count+'.png'
                    ss=  open(filename1, 'wb')
                    ss.write(imgdata4)
                    ss.close()
                    what_will_you_get_create = Slide_Image.objects.create(product_id=data_crete.id,image=fname1)

            return Response("Data Added Sucessfully")
        else:
            return Response("Data Added Sucessfully")
        # return Response({'result':'Product Created successfully'})


    def put(self,request,pk):

        data = request.data
        Product_Name=data.get('Product_Name')
        Product_Description=data.get('Product_Description')
        Product_Image=data.get('Product_Image')
        Product_Video=data.get('Product_Video')
        Product_Selling_Price=data.get('Product_Selling_Price')
        GST=data.get('GST')
        Product_Listed_Price=data.get('Product_Listed_Price')
        Status=data.get('Status')
        # Create_TimeStamp=data.get('Create_TimeStamp')
        # Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')
        HSN_SAC_Code=data.get('HSN_SAC_Code')
        Wash_instructions=data.get('Wash_instructions')
        Discount_ID=data.get('Discount_id')
        Product_Category_ID=data.get('Product_Category_id')
        product_sub_category=data.get('product_sub_category')
        Product_Inventory_ID=data.get('Product_Inventory_id')
        brand_id=data.get('brand_id')
        attribute_id=data.get('attribute_id')

        count=str(random.randint(100,9999999))
        split_base_url_data = Product_Image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = '/kri8eve/site/public/media/Product_Image/'+count+'.png'
        fname1 = '/media/Product_Image/'+count+'.png'
        ss=  open(filename1, 'wb')
        ss.write(imgdata1)
        ss.close()


        data=Product.objects.filter(id=pk).update(Product_Image=fname1)
        # data=Product.objects.filter(id=pk).update(Product_Name=Product_Name,
        #                         Product_Description=Product_Description,
        #                         Product_Image=fname1,
        #                         Product_Video=Product_Video,
        #                         Product_Selling_Price=Product_Selling_Price,
        #                         Gst=GST,
        #                         Product_Listed_Price=Product_Listed_Price,
        #                         Status=Status,
        #                         # Create_TimeStamp=Create_TimeStamp,
        #                         # Last_Update_TimeStamp=Last_Update_TimeStamp,
        #                         HSN_SAC_Code=HSN_SAC_Code,
        #                         Wash_instructions=Wash_instructions,
        #                         Product_Category_id=Product_Category_ID,
        #                         product_sub_category_id=product_sub_category,
        #                         Discount_id=Discount_ID,
        #                         Product_Inventory_id=Product_Inventory_ID,
        #                         attribute_id=attribute_id,brand_id=brand_id)


        return Response({'result':'Product updated successfully'})

    def delete(self, request, pk):
        all_values = Product.objects.filter(id=pk).delete()
        slider_delete=Slide_Image.objects.filter(product_id=pk).delete()
        attr_delete=Attributes.objects.filter(Product_ID_id=pk).delete()
        return Response({'result':all_values})


class Get_attributeAPIView(APIView):
    def get(self, request):
        product_id = self.request.query_params.get('product_id')
        Arr=[]
        product_attributes = Attributes.objects.filter(Product_ID_id=product_id).values()
        for i in product_attributes:
            res={}
            res['attribute_id']=i['id']
            res['product_id']=i['Product_ID_id']
            res['name']=i['name']
            res['option']=[]

            options = AttributeOptions.objects.filter(attributes_id=i['id'])
            for i in options:
                res['option'].append({
                'option_id':i.id,
                'attributes_id':i.attributes_id,
                'option':i.option
                })
            Arr.append(res)


        return Response(Arr)


class Get_color_attributeAPIView(APIView):
    def get(self, request):
        product_id = self.request.query_params.get('product_id')
        Arr=[]
        product_attributes = Attributes.objects.filter(Product_ID_id=product_id,name='Color').values()
        for i in product_attributes:
            res={}
            res['attribute_id']=i['id']
            res['product_id']=i['Product_ID_id']
            res['name']=i['name']
            res['option']=[]

            options = AttributeOptions.objects.filter(attributes_id=i['id'])
            for i in options:
                res['option'].append({
                'option_id':i.id,
                'attributes_id':i.attributes_id,
                'option':i.option
                })
            Arr.append(res)


        return Response(Arr)

class Get_size_attributeAPIView(APIView):
    def get(self, request):
        product_id = self.request.query_params.get('product_id')
        Arr=[]
        product_attributes = Attributes.objects.filter(Product_ID_id=product_id,name='Size').values()
        for i in product_attributes:
            res={}
            res['attribute_id']=i['id']
            res['product_id']=i['Product_ID_id']
            res['name']=i['name']
            res['option']=[]

            options = AttributeOptions.objects.filter(attributes_id=i['id'])
            for i in options:
                res['option'].append({
                'option_id':i.id,
                'attributes_id':i.attributes_id,
                'option':i.option
                })
            Arr.append(res)


        return Response(Arr)


class Menu_CategoryAPIView(APIView):
    def get(self, request):
        Arr=[]
        product_cat_data = Product_Category.objects.all().values()
        for i in product_cat_data:
            res={}
            res['product_category_id']=i['id']
            res['product_category_name']=i['Product_Category_Name']
            res['product_sub_category']=[]

            product_sub_cat_data = Product_Sub_Category.objects.filter(product_category_id=i['id'])
            for i in product_sub_cat_data:
                res['product_sub_category'].append({
                'product_sub_category_id':i.id,
                'product_sub_category_name':i.product_sub_category_name
                })
            Arr.append(res)


        return Response(Arr)



class Get_Product_Wise_Sub_CategoryAPIView(APIView):
    def get(self, request):
        product_sub_category_id = request.query_params.get('product_sub_category_id')
        user_id = request.query_params.get('user_id')
        Arr=[]
        dis_percent=0
        avg=0
        total_rating=0
        brand_name=''

        # print(user_id,'user_id')
        if user_id != 'null':
            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:

                product_data = Product.objects.filter(product_sub_category_id=product_sub_category_id).values()

                for i in product_data:
                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    for b in dis:
                        dis_percent=dis_percent+int(b.Discount_Percentage)
                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                    f_price=float(i['Product_Selling_Price'])-after_discount
                    dis_percent=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=f_price
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    if wishlist:
                        res['wishlist']=True
                    else:
                        res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)
                return Response(Arr)
            else:
                product_data = Product.objects.filter(product_sub_category_id=product_sub_category_id).values()

                for i in product_data:
                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    # rating_count =Reviews.objects.filter(Product_ID_id=i.id).count()
                    # rating =Reviews.objects.filter(Product_ID_id=i.id)
                    # if rating_count>0:
                    #     for k in rating:
                    #         total_rating=total_rating+int(k.star_rating)
                    #     avg=int(total_rating)/int(rating_count)
                    # else:
                    #     avg=0

                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=i['Product_Selling_Price']
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                    if wishlist:
                        res['wishlist']=True
                    else:
                        res['wishlist']=False
                    # res['wishlist']=i['wishlistss']
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)
                return Response(Arr)


        if product_sub_category_id:
            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:
                product_data = Product.objects.filter(product_sub_category_id=product_sub_category_id).values()

                for i in product_data:
                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    for b in dis:
                        dis_percent=dis_percent+int(b.Discount_Percentage)
                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                    f_price=float(i['Product_Selling_Price'])-after_discount
                    dis_percent=0

                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=f_price
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    res['wishlist']=False
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)
                return Response(Arr)
            else:
                product_data = Product.objects.filter(product_sub_category_id=product_sub_category_id).values()

                for i in product_data:
                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                    if rating_count>0:
                        for k in rating:
                            if k.star_rating!='':

                                total_rating=total_rating+int(k.star_rating)
                            else:
                                total_rating=0
                        avg=int(total_rating)/int(rating_count)
                    else:
                        avg=0
                    total_rating=0
                    rating_count=0
                    brand=Brand.objects.filter(id=i['brand_id'])
                    for k in brand:
                        brand_name=k.brand_name
                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                    for l in p_category:
                        Product_Category_Name=l.Product_Category_Name
                        image=str(l.image)

                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                    for m in ps_category:
                        product_sub_category_name=m.product_sub_category_name
                        ps_image=str(m.image)

                    res={}
                    res['rating']=avg
                    res['id']=i['id']
                    res['brand_name']=brand_name
                    res['brand_id']=i['brand_id']
                    res['Product_Name']=i['Product_Name']
                    res['Product_Description']=i['Product_Description']
                    res['Product_Image']=i['Product_Image']
                    res['Product_Video']=i['Product_Video']
                    res['Product_Selling_Price']=i['Product_Selling_Price']
                    res['Gst']=i['Gst']
                    res['Product_Listed_Price']=i['Product_Listed_Price']
                    res['Product_Details']=i['Product_Details']
                    res['Status']=i['Status']
                    res['Create_TimeStamp']=i['Create_TimeStamp']
                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                    res['Wash_instructions']=i['Wash_instructions']
                    res['Product_Category']=i['Product_Category_id']
                    res['category_image']=image
                    res['Product_Category_Name']=Product_Category_Name
                    res['product_sub_category']=i['product_sub_category_id']
                    res['product_sub_category_name']=product_sub_category_name
                    res['sub_category_image']=ps_image
                    res['wishlist']=False
                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                    # res['color_count']=items
                    res['attribute_option']=[]

                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                    for k in item:
                        id=k.id

                        option=AttributeOptions.objects.filter(attributes_id=id)
                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                        res['color_count']=option_count
                        for j in option:

                            res['attribute_option'].append({
                            'option_id':j.id,
                            'option':j.option,

                            })
                    Arr.append(res)
                return Response(Arr)

        else:
            response='product_sub_category_id required'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)




class Custom_Userapi(APIView):
    # queryset = Custom_User.objects.all().values()
    def get(self,request):
        id = self.request.query_params.get('id')
        Arr=[]
        role_name=''
        senior_role=''
        senior_name=''
        if id:
            all_values = Custom_User.objects.filter(id=id).values()
            for i in all_values:
                code=Team_Code.objects.filter(ref_code=i['referral_code'])
                for j in code:
                    senior_name=j.team.name
                    senior_role=j.team.role.user_role_name
                if senior_role=='Marketer':
                    role=UserRoleRef.objects.filter(id=i['role_id'])
                    for k in role:
                        role_name=k.user_role_name
                    res={}
                    res['id']=i['id']
                    res['user_id']=i['user_id']
                    res['username']=i['username']
                    res['email']=i['Email_ID']
                    res['mobile_number']=i['Mobile_Number']
                    res['fullname']=i['Full_Name']
                    res['date_of_birth']=i['Date_Of_Birth']
                    res['role_id']=i['role_id']
                    res['role_name']=role_name
                    res['location']=i['location']
                    res['gender']=i['gender']
                    res['alt_number']=i['alt_number']
                    res['referral_code']=i['referral_code']
                    res['ref_code']=i['user_to_user_refcode']

                    res['leader']=''
                    res['marketer']=senior_name

                    res['address']=[]
                    # res['city']=[]
                    # res['state']=[]
                    # res['pincode']=[]
                    address1 = User_Address.objects.filter(user_id=i['user_id'])
                    for j in address1:
                        res['address'].append({
                        'address':j.Address,
                        'city':j.City,
                        'state':j.State,
                        'pincode':j.Pincode,
                        })
                    Arr.append(res)
                elif senior_role=='Leader':
                    role=UserRoleRef.objects.filter(id=i['role_id'])
                    for k in role:
                        role_name=k.user_role_name
                    res={}
                    res['id']=i['id']
                    res['user_id']=i['user_id']
                    res['username']=i['username']
                    res['email']=i['Email_ID']
                    res['mobile_number']=i['Mobile_Number']
                    res['fullname']=i['Full_Name']
                    res['date_of_birth']=i['Date_Of_Birth']
                    res['role_id']=i['role_id']
                    res['role_name']=role_name
                    res['location']=i['location']
                    res['gender']=i['gender']
                    res['alt_number']=i['alt_number']
                    res['referral_code']=i['referral_code']
                    res['ref_code']=i['user_to_user_refcode']
                    res['leader']=senior_name
                    res['marketer']=''

                    res['address']=[]
                    # res['city']=[]
                    # res['state']=[]
                    # res['pincode']=[]
                    address1 = User_Address.objects.filter(user_id=i['user_id'])
                    for j in address1:
                        res['address'].append({
                        'address':j.Address,
                        'city':j.City,
                        'state':j.State,
                        'pincode':j.Pincode,
                        })
                    Arr.append(res)
                else:
                    role=UserRoleRef.objects.filter(id=i['role_id'])
                    for k in role:
                        role_name=k.user_role_name
                    res={}
                    res['id']=i['id']
                    res['user_id']=i['user_id']
                    res['username']=i['username']
                    res['email']=i['Email_ID']
                    res['mobile_number']=i['Mobile_Number']
                    res['fullname']=i['Full_Name']
                    res['date_of_birth']=i['Date_Of_Birth']
                    res['role_id']=i['role_id']
                    res['role_name']=role_name
                    res['location']=i['location']
                    res['gender']=i['gender']
                    res['alt_number']=i['alt_number']
                    res['referral_code']=i['referral_code']
                    res['ref_code']=i['user_to_user_refcode']
                    res['leader']=''
                    res['marketer']=''

                    res['address']=[]
                    # res['city']=[]
                    # res['state']=[]
                    # res['pincode']=[]
                    address1 = User_Address.objects.filter(user_id=i['user_id'])
                    for j in address1:
                        res['address'].append({
                        'address':j.Address,
                        'city':j.City,
                        'state':j.State,
                        'pincode':j.Pincode,
                        })
                    Arr.append(res)


            return Response(Arr)
        else:

            all_values = Custom_User.objects.all().values()
            for i in all_values:
                if i['referral_code']:
                    code=Team_Code.objects.filter(ref_code=i['referral_code'])
                    for j in code:
                        senior_name=j.team.name
                        senior_role=j.team.role.user_role_name
                        if senior_role=='Marketer':
                            role=UserRoleRef.objects.filter(id=i['role_id'])
                            for k in role:
                                role_name=k.user_role_name
                            res={}
                            res['id']=i['id']
                            res['user_id']=i['user_id']
                            res['username']=i['username']
                            res['email']=i['Email_ID']
                            res['mobile_number']=i['Mobile_Number']
                            res['fullname']=i['Full_Name']
                            res['date_of_birth']=i['Date_Of_Birth']
                            res['role_id']=i['role_id']
                            res['role_name']=role_name
                            res['location']=i['location']
                            res['gender']=i['gender']
                            res['alt_number']=i['alt_number']
                            res['referral_code']=i['referral_code']
                            res['leader']=''
                            res['marketer']=senior_name

                            res['address']=[]
                            # res['city']=[]
                            # res['state']=[]
                            # res['pincode']=[]
                            address1 = User_Address.objects.filter(user_id=i['user_id'])
                            for j in address1:
                                res['address'].append({
                                'address':j.Address,
                                'city':j.City,
                                'state':j.State,
                                'pincode':j.Pincode,
                                })
                            Arr.append(res)
                        elif senior_role=='Leader':
                            role=UserRoleRef.objects.filter(id=i['role_id'])
                            for k in role:
                                role_name=k.user_role_name
                            res={}
                            res['id']=i['id']
                            res['user_id']=i['user_id']
                            res['username']=i['username']
                            res['email']=i['Email_ID']
                            res['mobile_number']=i['Mobile_Number']
                            res['fullname']=i['Full_Name']
                            res['date_of_birth']=i['Date_Of_Birth']
                            res['role_id']=i['role_id']
                            res['role_name']=role_name
                            res['location']=i['location']
                            res['gender']=i['gender']
                            res['alt_number']=i['alt_number']
                            res['referral_code']=i['referral_code']
                            res['leader']=senior_name
                            res['marketer']=''

                            res['address']=[]
                            # res['city']=[]
                            # res['state']=[]
                            # res['pincode']=[]
                            address1 = User_Address.objects.filter(user_id=i['user_id'])
                            for j in address1:
                                res['address'].append({
                                'address':j.Address,
                                'city':j.City,
                                'state':j.State,
                                'pincode':j.Pincode,
                                })
                            Arr.append(res)
                else:
                    role=UserRoleRef.objects.filter(id=i['role_id'])
                    for k in role:
                        role_name=k.user_role_name
                    res={}
                    res['id']=i['id']
                    res['user_id']=i['user_id']
                    res['username']=i['username']
                    res['email']=i['Email_ID']
                    res['mobile_number']=i['Mobile_Number']
                    res['fullname']=i['Full_Name']
                    res['date_of_birth']=i['Date_Of_Birth']
                    res['role_id']=i['role_id']
                    res['role_name']=role_name
                    res['location']=i['location']
                    res['gender']=i['gender']
                    res['alt_number']=i['alt_number']
                    res['referral_code']=i['referral_code']
                    res['leader']=''
                    res['marketer']=''

                    res['address']=[]
                    # res['city']=[]
                    # res['state']=[]
                    # res['pincode']=[]
                    address1 = User_Address.objects.filter(user_id=i['user_id'])
                    for j in address1:
                        res['address'].append({
                        'address':j.Address,
                        'city':j.City,
                        'state':j.State,
                        'pincode':j.Pincode,
                        })
                    Arr.append(res)

            return Response(Arr)

    def post(self,request):
        data = request.data
        # user_id=data.get('user_id')
        username=data.get('username')
        password=data.get('password')
        mobile_number=data.get('mobile_number')
        email=data.get('email')
        address    =data.get('address')
        city        =data.get('city')
        state            =data.get('state')
        pincode            =data.get('pincode')
        fullname        =data.get('fullname')
        role_id                = data.get('role_id')
        date_of_birth=data.get('date_of_birth')
        referral_code=data.get('referral_code')



        if User.objects.filter(username=username,email=email,last_name=mobile_number).exists():
            header_response = {}
            response['error'] = {'error': {
                'detail': 'Username or email already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)
        else:
            user_create = User.objects.create_user(username=username,email=email,password=password,first_name=fullname)
            ref=fullname.upper()+str(user_create.id)

            custom_user = Custom_User.objects.create(user_id=user_create.id,username=username,Full_Name=fullname,Mobile_Number=mobile_number,Email_ID=email,Date_Of_Birth=date_of_birth,role_id=role_id,referral_code=referral_code,user_to_user_refcode=ref)
            user_address_create = User_Address.objects.create(user_id=user_create.id,Address=address,City=city,State=state,Pincode=pincode)


            return Response({'result':'Created'})


    def put(self,request,pk):

        data = request.data

        user_id=data.get('user_id')
        mobile_number=data.get('mobile_number')
        address    =data.get('address')
        city        =data.get('city')
        state            =data.get('state')
        pincode            =data.get('pincode')
        fullname        =data.get('fullname')
        date_of_birth=data.get('date_of_birth')
        # role_id                = data.get('role_id')

        email=data.get('email')
        gender=data.get('gender')
        location=data.get('location')
        alt_number=data.get('alt_number')
        # referral_code=data.get('referral_code')


        # data= Custom_User.objects.filter(user_id=user_id).update(referral_code=referral_code)
        data= Custom_User.objects.filter(user_id=user_id).update(Full_Name=fullname,Date_Of_Birth=date_of_birth,
                                            Mobile_Number=mobile_number,Email_ID=email,gender=gender,location=location,alt_number=alt_number)

        address_update = User_Address.objects.filter(user_id=user_id).update(Address=address,City=city,State=state,Pincode=pincode)


        return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = Custom_User.objects.get(id=pk)
        del_user=User.objects.filter(id=all_values.user_id).delete()
        return Response({'result':'Deleted'})




#
# class UserAuthenticationApi(APIView):
#     queryset = User_Authentication.objects.all().values()
#     def get(self,request):
#         all_values = User_Authentication.objects.all().values()
#         return Response(all_values)
#
#     def post(self,request):
#
#         data = request.data
#         User_Name=data.get('User_Name')
#         User_Password=data.get('User_Password')
#         Status=data.get('Status')
#         Create_TimeStamp=data.get('Create_TimeStamp')
#         Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')
#
#         selected_page_no = 1
#         page_number = request.GET.get('page')
#         if page_number:
#             selected_page_no = int(page_number)
#
#
#         if User_Authentication.objects.filter(User_Name=User_Name).exists():
#             return Response({'result':'Email exists'})
#         else:
#             User_Authentication.objects.create(User_Name=User_Name,
#                                                 User_Password=User_Password,
#                                                 Status=Status,
#                                                 Create_TimeStamp=Create_TimeStamp,
#                                                 Last_Update_TimeStamp=Last_Update_TimeStamp)
#
#             posts = User_Authentication.objects.all().values()
#             paginator = Paginator(posts,3)
#             try:
#                 page_obj = paginator.get_page(selected_page_no)
#             except PageNotAnInteger:
#                 page_obj = paginator.page(1)
#             except EmptyPage:
#                 page_obj = paginator.page(paginator.num_pages)
#             return Response({'result':'Created', 'data':list(page_obj)})
#
#
#     def put(self,request,pk):
#
#
#         data = request.data
#         User_Name=data.get('User_Name')
#         User_Password=data.get('User_Password')
#         Status=data.get('Status')
#         Create_TimeStamp=data.get('Create_TimeStamp')
#         Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')
#
#         if User_Authentication.objects.filter(User_Name=User_Name).exists():
#             return Response({'result':'Email exists'})
#         else:
#             User_Authentication.objects.filter(id=pk).update(User_Name=User_Name,
#                                                 User_Password=User_Password,
#                                                 Status=Status,
#                                                 Create_TimeStamp=Create_TimeStamp,
#                                                 Last_Update_TimeStamp=Last_Update_TimeStamp)
#
#             return Response({'result':'Updated'})
#
#     def delete(self,request,pk):
#         all_values = User_Authentication.objects.filter(id=pk).delete()
#         return Response(all_values)
#
#


class UserAddressApi(APIView):

    def get(self,request):
        user_id=self.request.query_params.get('user_id')
        id=self.request.query_params.get('id')
        Arr=[]
        mobile_number=0
        email=''
        m=''
        if id:
            all_values = User_Address.objects.filter(id=id)
            for i in all_values:
                c_user=Custom_User.objects.get(user_id=i.user_id)

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'fullname':c_user.Full_Name,
                'mobile_number':c_user.Mobile_Number,
                'email':c_user.Email_ID,
                'Address':i.Address,
                'City':i.City,
                'State':i.State,
                'Country':i.Country,
                'Pincode':i.Pincode,
                'street':i.street,
                'address_type':i.address_type,
                'delfault_address':i.delfault_address,
                })
            return Response(Arr)
        if user_id:
            all_values = User_Address.objects.filter(user_id=user_id)

            for i in all_values:
                c_user=Custom_User.objects.get(user_id=i.user_id)
                # for k in c_user:
                #     mobile_number=k.Mobile_Number,
                #     email=k.Email_ID
                # m= mobile_number
                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'fullname':c_user.Full_Name,
                'mobile_number':c_user.Mobile_Number,
                'email':c_user.Email_ID,
                'Address':i.Address,
                'City':i.City,
                'State':i.State,
                'Country':i.Country,
                'Pincode':i.Pincode,
                'street':i.street,
                'address_type':i.address_type,
                'delfault_address':i.delfault_address,
                })
            return Response(Arr)


        else:
            all_values = User_Address.objects.all()
            for i in all_values:
                c_user=Custom_User.objects.get(user_id=i.user_id)

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'fullname':c_user.Full_Name,
                'mobile_number':c_user.Mobile_Number,
                'email':c_user.Email_ID,
                'Address':i.Address,
                'City':i.City,
                'State':i.State,
                'Country':i.Country,
                'Pincode':i.Pincode,
                'street':i.street,
                'address_type':i.address_type,
                'delfault_address':i.delfault_address,
                })
            return Response(Arr)


    def post(self,request):

        data = request.data
        user_id=data.get('user_id')
        Address=data.get('Address')
        City=data.get('City')
        State=data.get('State')
        Country=data.get('Country')
        Pincode=data.get('Pincode')
        street=data.get('street')
        address_type=data.get('address_type')
        default_address=data.get('default_address')
        # print(default_address,'lll')
        print(type(default_address),'type')
        if default_address==True:
            address=User_Address.objects.filter(user_id=user_id).update(delfault_address=False)


        # address=User_Address.objects.filter(user_id=user_id)
        # if address:
        #     address=User_Address.objects.filter(user_id=user_id).update(user_id=user_id,Address=Address,
        #                                                                 City=City,
        #                                                                 State=State,
        #                                                                 Country=Country,
        #                                                                 Pincode=Pincode,
        #                                                                 street=street,
        #                                                                 address_type=address_type,
        #                                                                 default_address=default_address)
        #     return Response('data updated successfully')
        # else:
        data=User_Address.objects.create(user_id=user_id,
                                                Address=Address,
                                                City=City,
                                                State=State,
                                                Country=Country,
                                                Pincode=Pincode,
                                                street=street,
                                                address_type=address_type,
                                                delfault_address=default_address)


        return Response('data added successfully')


    def put(self,request,pk):


        data = request.data
        default_address=data.get('default_address')
        user_id=data.get('user_id')
        Address=data.get('Address')
        City=data.get('City')
        State=data.get('State')
        Country=data.get('Country')
        Pincode=data.get('Pincode')
        street=data.get('street')
        address_type=data.get('address_type')
        default_address=data.get('default_address')
        # print(default_address,'lll')
        # print(type(default_address),'type')
        if default_address==True:
            address=User_Address.objects.filter(user_id=user_id).update(delfault_address=False)


        # address=User_Address.objects.filter(user_id=user_id)
        # if address:
        #     address=User_Address.objects.filter(user_id=user_id).update(user_id=user_id,Address=Address,
        #                                                                 City=City,
        #                                                                 State=State,
        #                                                                 Country=Country,
        #                                                                 Pincode=Pincode,
        #                                                                 street=street,
        #                                                                 address_type=address_type,
        #                                                                 default_address=default_address)
        #     return Response('data updated successfully')
        # else:
        data=User_Address.objects.filter(id=pk).update(user_id=user_id,
                                                Address=Address,
                                                City=City,
                                                State=State,
                                                Country=Country,
                                                Pincode=Pincode,
                                                street=street,
                                                address_type=address_type,
                                                delfault_address=default_address)


        # return Response('data added successfully')


        # data=User_Address.objects.filter(id=pk).update(default_address=default_address)

        return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = User_Address.objects.filter(id=pk).delete()
        return Response(all_values)



class Update_default_addressApi(APIView):

    def put(self,request,pk):


        data = request.data
        default_address=data.get('default_address')
        user_id=data.get('user_id')
        val=User_Address.objects.filter(user_id=user_id).update(delfault_address=False)


        data=User_Address.objects.filter(id=pk).update(delfault_address=default_address)

        return Response({'result':'Updated'})


class UserPaymentApi(APIView):
    queryset = User_Payment.objects.all().values()
    def get(self,request):
        all_values = User_Payment.objects.all().values()
        return Response(all_values)

    def post(self,request):

        data = request.data
        custom_user=data.get('user_id')
        Payment_Name=data.get('Payment_Name')
        Payment_Type=data.get('Payment_Type')
        GST=data.get('GST')
        Delivery_Charges=data.get('Delivery_Charges')
        Amount=data.get('Amount')
        Create_TimeStamp=data.get('Create_TimeStamp')
        Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')


        selected_page_no = 1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)


        if User_Payment.objects.filter(Payment_Name=Payment_Name).exists():
            return Response({'result':'payment name exists'})
        else:
            User_Payment.objects.create(custom_user_id=custom_user,
                                            Payment_Name=Payment_Name,
                                            Payment_Type=Payment_Type,
                                            GST=GST,
                                            Delivery_Charges=Delivery_Charges,
                                            Amount=Amount,
                                            Create_TimeStamp=Create_TimeStamp,
                                            Last_Update_TimeStamp=Last_Update_TimeStamp

                                            )

            posts = User_Payment.objects.all().values()
            paginator = Paginator(posts,3)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':'Created', 'data':list(page_obj)})


    def put(self,request,pk):


        data = request.data
        custom_user=data.get('user_id')
        Payment_Name=data.get('Payment_Name')
        Payment_Type=data.get('Payment_Type')
        GST=data.get('GST')
        Delivery_Charges=data.get('Delivery_Charges')
        Amount=data.get('Amount')
        Create_TimeStamp=data.get('Create_TimeStamp')
        Last_Update_TimeStamp=data.get('Last_Update_TimeStamp')
        if User_Payment.objects.filter(Payment_Name=Payment_Name).exists():
            return Response({'result':'payment name exists'})
        else:
            User_Payment.objects.filter(id=pk).update(custom_user_id=custom_user,
                                            Payment_Name=Payment_Name,
                                            Payment_Type=Payment_Type,
                                            GST=GST,
                                            Delivery_Charges=Delivery_Charges,
                                            Amount=Amount,
                                            Create_TimeStamp=Create_TimeStamp,
                                            Last_Update_TimeStamp=Last_Update_TimeStamp)

            return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = User_Payment.objects.filter(id=pk).delete()
        return Response(all_values)



#
# class UserRefRoleApi(APIView):
#     queryset = UserRoleRef.objects.all().values()
#     def get(self,request):
#         all_values = UserRoleRef.objects.all().values()
#         return Response(all_values)
#
#     def post(self,request):
#
#         data = request.data
#         custom_user=data.get('user_id')
#
#         user_role_name=data.get('user_role_name')
#
#
#
#         create_timestamp=data.get('create_timestamp')
#         last_update_timestamp=data.get('last_update_timestamp')
#
#
#         selected_page_no = 1
#         page_number = request.GET.get('page')
#         if page_number:
#             selected_page_no = int(page_number)
#
#
#         if UserRoleRef.objects.filter(user_role_name=user_role_name).exists():
#             return Response({'result':' user role name exists'})
#         else:
#             UserRoleRef.objects.create(custom_user_id=custom_user,
#                                             user_role_name=user_role_name,
#                                             create_timestamp=create_timestamp,
#                                             last_update_timestamp=last_update_timestamp
#
#                                             )
#
#             posts = UserRoleRef.objects.all().values()
#             paginator = Paginator(posts,3)
#             try:
#                 page_obj = paginator.get_page(selected_page_no)
#             except PageNotAnInteger:
#                 page_obj = paginator.page(1)
#             except EmptyPage:
#                 page_obj = paginator.page(paginator.num_pages)
#             return Response({'result':'Created', 'data':list(page_obj)})
#
#
#     def put(self,request,pk):
#
#
#         data = request.data
#         custom_user=data.get('user_id')
#
#         user_role_name=data.get('user_role_name')
#
#         create_timestamp=data.get('create_timestamp')
#         last_update_timestamp=data.get('last_update_timestamp')
#
#
#         if UserRoleRef.objects.filter(user_role_name=user_role_name).exists():
#             return Response({'result':'user role name exists'})
#         else:
#             UserRoleRef.objects.filter(id=pk).update(custom_user_id=custom_user,
#                                             user_role_name=user_role_name,
#                                            create_timestamp=create_timestamp,
#                                             last_update_timestamp=last_update_timestamp)
#
#             return Response({'result':'Updated'})
#
#     def delete(self,request,pk):
#         all_values = UserRoleRef.objects.filter(id=pk).delete()
#         return Response(all_values)
#


class FAQAPIVIEW(APIView):
    # queryset = FAQs.objects.all().values()

    def get(self,request):
        id =self.request.query_params.get('id')
        if id:
            all_values = FAQs.objects.filter(id=id).values()
            return Response(all_values)
        else:
            all_values = FAQs.objects.all().values()
            return Response(all_values)

    def post(self,request):
        data = request.data
        faq_name = data.get('faq_name')
        description= data.get('description')





        data_create=FAQs.objects.create(faq_name=faq_name,
                                description=description)



        return Response({'result':'Created'})

    def put(self,request,pk):
        data = request.data
        faq_name = data.get('faq_name')
        description= data.get('description')



        data= FAQs.objects.filter(id=pk).update(faq_name=faq_name,
                                description=description)

        if data:
            return Response({'result':'Updated'})
        else:
            response='Invalid id'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        all_values = FAQs.objects.filter(id=pk).delete()
        return Response({'result':'Deleted'})



class ReviewApiViews(APIView):
    # queryset = Reviews.objects.all()
    def get(self,request):

        id = self.request.query_params.get('id')
        product_id = self.request.query_params.get('product_id')
        Arr=[]
        profile=''
        total_rating=0
        avg=0.0

        if product_id:
            review_count =Reviews.objects.filter(Product_ID_id=product_id).count()
            rating_count =Reviews.objects.filter(Product_ID_id=product_id).count()
            rating =Reviews.objects.filter(Product_ID_id=product_id)
            if rating_count>0:
                for k in rating:
                    if k.star_rating!='':
                        total_rating=total_rating+int(k.star_rating)
                avg=int(total_rating)/int(rating_count)

            test1 =Reviews.objects.filter(Product_ID_id=product_id).order_by('-id')
            for i in test1:
                fullname=''
                user=Custom_User.objects.filter(user_id=i.user_id)
                for k in user:
                    fullname=k.Full_Name

                user_profile=Custom_user_profile.objects.filter(user_id=i.user_id)
                for j in user_profile:
                    profile=str(j.profile_img)

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                # 'username':i.user.username,
                'fullname':fullname,
                'product_id':i.Product_ID_id,
                'product_name':i.Product_ID.Product_Name,
                'reviewMessage':i.reviewMessage,
                'star_rating':i.star_rating,
                'review_image':str(i.review_image),
                'create_timestamp':i.create_timestamp,
                'profile_img':profile,

                })
            return Response({'data':Arr,'review_count':review_count,'rating_avg':avg,'total_rating':total_rating})

        if id:
            test1 =Reviews.objects.filter(id=id)
            for i in test1:
                fullname=''
                user=Custom_User.objects.filter(user_id=i.user_id)
                for k in user:
                    fullname=k.Full_Name

                user_profile=Custom_user_profile.objects.filter(user_id=i.user_id)
                for j in user_profile:
                    profile=str(j.profile_img)

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                # 'username':i.user.username,
                'fullname':fullname,
                'product_id':i.Product_ID_id,
                'product_name':i.Product_ID.Product_Name,
                'reviewMessage':i.reviewMessage,
                'star_rating':i.star_rating,
                'review_image':str(i.review_image),
                'create_timestamp':i.create_timestamp,
                'profile_img':profile,

                })
            return Response(Arr)

        else:
            test1 =Reviews.objects.all().order_by('-id')
            for i in test1:
                print(i.Product_ID)
                print(i.Product_ID)
                fullname=''
                user=Custom_User.objects.filter(user_id=i.user_id)
                for k in user:
                    fullname=k.Full_Name

                user_profile=Custom_user_profile.objects.filter(user_id=i.user_id)
                for j in user_profile:
                    profile=str(j.profile_img)

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                # 'username':i.user.username,
                'fullname':fullname,
                'product_id':i.Product_ID_id,
                'product_name':i.Product_ID.Product_Name,
                'reviewMessage':i.reviewMessage,
                'star_rating':i.star_rating,
                'review_image':str(i.review_image),
                'create_timestamp':i.create_timestamp,
                'profile_img':profile,

                })
            return Response(Arr)



    def post(self,request):
        data = request.data
        user_id = data.get('user_id')
        Product_ID= data.get('Product_ID')
        reviewMessage= data.get('reviewMessage')
        star_rating= data.get('star_rating')
        # review_image =data.get('review_image')

        # count=str(random.randint(100,9999999))
        #
        #
        # split_base_url_data = review_image.split(';base64,')[1]
        # imgdata1 = base64.b64decode(split_base_url_data)
        # filename1 = '/kri8eve/site/public/media/review_image/'+count+'.png'
        # fname1 = '/media/review_image/'+count+'.png'
        # ss=  open(filename1, 'wb')
        # ss.write(imgdata1)
        # ss.close()



        data_create=Reviews.objects.create(user_id=user_id,
                                    Product_ID_id=Product_ID,
                                    reviewMessage=reviewMessage,
                                    # review_image=fname1,
                                    star_rating=star_rating)


        return Response({'result':'Created'})

    def put(self,request,pk):
        data = request.data
        user_id = data.get('user_id')
        Product_ID= data.get('Product_ID')
        reviewMessage= data.get('reviewMessage')
        star_rating= data.get('star_rating')
        review_image =data.get('review_image')

        count=str(random.randint(100,9999999))

        split_base_url_data = review_image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = '/kri8eve/site/public/media/review_image/'+count+'.png'
        fname1 = '/media/review_image/'+count+'.png'
        ss=  open(filename1, 'wb')
        ss.write(imgdata1)
        ss.close()


        Reviews.objects.filter(id=pk).update(user_id=user_id,
                                    Product_ID_id=Product_ID,
                                    reviewMessage=reviewMessage,
                                    star_rating=star_rating,review_image=fname1)

        return Response({'result':'updated'})

    def delete(self,request,pk):
        all_values = Reviews.objects.filter(id=pk).delete()
        return Response(all_values)




class TestimonialsAPIView(APIView):
    def get(self, request):
        id = self.request.query_params.get('id')
        # user_id =self.request.query_params.get('user_id')

        # user_check = User.objects.filter(id= user_id)
        # if user_check:


        if id:
            testimonials_data = Testimonials.objects.filter(id=id).values()
            return Response(testimonials_data)
        else:
            testimonials_data = Testimonials.objects.all().values()
            return Response(testimonials_data)
        # else:
            # return JsonResponse({'message': 'Valid user Id Required'})


    def post(self, request):


        data = request.data
        # user_id = data.get('user_id')

        name = data.get('name')
        image = data.get('image')
        category = data.get('category')
        video      = data.get('video')
        rating = data.get('rating')
        feedback_small_description = data.get('feedback_small_description')
        feedback_detailed_description=data.get('feedback_detailed_description')


        count=str(random.randint(100,9999999))


        split_base_url_data = image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = '/kri8eve/site/public/media/testimonials_images/'+count+'.png'
        fname1 = '/media/testimonials_images/'+count+'.png'
        ss=  open(filename1, 'wb')
        ss.write(imgdata1)
        ss.close()




        # count1=str(random.randint(100,9999999))
        # split_base_url_data = video.split(';base64,')[1]
        # viddata = base64.b64decode(split_base_url_data)
        # filenames = '/kri8eve/site/public/media/testimonials_video/'+count1+'.mp4'
        # fnames = '/media/testimonials_video/'+count1+'.mp4'
        # ss=  open(filenames, 'wb')
        # ss.write(viddata)
        # ss.close()


        testimonials_create = Testimonials.objects.create(name= name,image=fname1,video=video,category=category,rating=rating,feedback_small_description=feedback_small_description,feedback_detailed_description=feedback_detailed_description)
        return Response("Data Added Sucessfully")


    def put(self, request,pk):
        data = request.data
        image = data.get('image')
        video      = data.get('video')
        name = data.get('name')

        if image !=None:
            count=str(random.randint(100,9999999))
            split_base_url_data = image.split(';base64,')[1]
            imgdata = base64.b64decode(split_base_url_data)
            filename = '/kri8eve/site/public/media/testimonials_images/'+count+'.png'
            fname = '/media/testimonials_images/'+count+'.png'
            ss=  open(filename, 'wb')
            ss.write(imgdata)
            ss.close()

            # count1=str(random.randint(100,9999999))
            # split_base_url_data = video.split(';base64,')[1]
            # viddata = base64.b64decode(split_base_url_data)
            # filename = '/kri8eve/site/public/media/testimonials_video/'+count1+'.png'
            # fnames = '/media/testimonials_video/'+count1+'.png'
            # ss=  open(filename, 'wb')
            # ss.write(viddata)
            # ss.close()
            data = Testimonials.objects.filter(id=pk).update(name = data.get('name'),
                                                                image =fname,
                                                                category = data.get('category'),
                                                                video      = video,
                                                                rating = data.get('rating'),
                                                                feedback_small_description = data.get('feedback_small_description'),
                                                                feedback_detailed_description=data.get('feedback_detailed_description'), )
            if data:
                return JsonResponse({'message': 'Testimonials details Updated Sucessfully.'})
            else:
                return JsonResponse({'message': 'Invalid Testimonials ID'})

        else:
            data = Testimonials.objects.filter(id=pk).update(name = data.get('name'),
                                                                category = data.get('category'),
                                                                video      = video,
                                                                rating = data.get('rating'),
                                                                feedback_small_description = data.get('feedback_small_description'),
                                                                feedback_detailed_description=data.get('feedback_detailed_description'), )
            if data:
                return JsonResponse({'message': 'Testimonials details Updated Sucessfully.'})
            else:
                return JsonResponse({'message': 'Invalid Testimonials ID'})


    def delete(self, request,pk):
        # data = request.data
        # id = data.get('id')
        # user_id = data.get('user_id')
        # id =self.request.query_params.get('id')
        # user_id =self.request.query_params.get('user_id')


        # user_check = User.objects.filter(Q(id= user_id))
        # if user_check:
        testimonials_data = Testimonials.objects.filter(id= pk)

        if len(testimonials_data) > 0:
            testimonials_data.delete()
            return Response("Testimonials details  Deleted Sucessfully")
        else:
            return Response("Id Required.")
        # else:
            # return JsonResponse({'message': 'Invalid User ID.'})


class OrderDetailsApis(APIView):
    def get(self,request):
        print('kiii')
        user_id =self.request.query_params.get('user_id')
        id =self.request.query_params.get('id')
        Arr=[]
        address=''
        city=''
        state=''
        street=''
        locationname=''
        pincode=''
        delivery_charges=''
        name=''
        names=''

        if id:
            test1 = OrderDetails.objects.filter(id=id)
            for i in test1:

                # address=User_Address.objects.filter(user_id=i.user_id,delfault_address=True)
                # for j in address:
                #     address=j.Address
                #     city=j.City
                #     state=j.State
                #     street=j.street
                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'total':i.total,
                'delivery_boy_name':i.kri8evTeam.name,
                'delivery_status':i.delivery_status,
                'shipping_id':i.shippingcharges_id,
                'locationname':i.shippingcharges.locationname,
                'pincode':i.shippingcharges.pincode,
                'delivery_charges':i.shippingcharges.amount,
                'date':i.create_timestamp
                # 'address':address,
                # 'city':city,
                # 'state':state,
                # 'street':street,
                })
            return Response(Arr)

        if user_id:
            test1 = OrderDetails.objects.filter(user_id=user_id)
            for i in test1:

                # address=User_Address.objects.filter(user_id=i.user_id,delfault_address=True)
                # for j in address:
                #     address=j.Address
                #     city=j.City
                #     state=j.State
                #     street=j.street
                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'total':i.total,
                'shipping_id':i.shippingcharges_id,
                'locationname':i.shippingcharges.locationname,
                'pincode':i.shippingcharges.pincode,
                'delivery_charges':i.shippingcharges.amount,
                'date':i.create_timestamp
                # 'address':address,
                # 'city':city,
                # 'state':state,
                # 'street':street,
                # 'product_name':product_name,
                })
            return Response(Arr)

        else:
            option=[]
            tests = OrderDetails.objects.all().values()
            for i in tests:
                payment=PaymentDetails.objects.filter(orderdetails_id=i['id'],status=True)
                if payment:
                    username=User.objects.get(id=i['user_id'])
                    c_user=Custom_User.objects.get(user_id=i['user_id'])
                    shipping=ShippingCharges.objects.filter(id=i['shippingcharges_id'])
                    for k in shipping:
                        locationname=k.locationname
                        pincode=k.pincode
                        delivery_charges  =k.amount

                    address=User_Address.objects.filter(user_id=i['user_id'],delfault_address=True)
                    for j in address:
                        address=j.Address
                        city=j.City
                        state=j.State
                        street=j.street
                    print(i['delivery_boy_id'],'delivery_boy_id')
                    kr_team=kri8evTeam.objects.filter(id=i['delivery_boy_id'])
                    if kr_team:
                        for l in kr_team:
                            name=l.name
                        print(name,'nameee')
                        res={}
                        res['id']=i['id']
                        res['user_id']=i['user_id']
                        res['username']=username.username
                        res['fullname']=username.first_name
                        res['mobile_number']=c_user.Mobile_Number
                        res['alt_number']=c_user.alt_number
                        res['total']=i['total']
                        res['locationname']=locationname
                        res['pincode']=i['Pincode']
                        res['delivery_charges']=delivery_charges
                        res['address']=i['Address']
                        res['city']=i['City']
                        res['state']=i['State']
                        res['street']=i['street']
                        res['delivery_boy_name']=name
                        res['delivery_status']=i['delivery_status']
                        res['date']=i['create_timestamp']
                        res['product_details']=[]
                    else:

                        res={}
                        res['id']=i['id']
                        res['user_id']=i['user_id']
                        res['username']=username.username
                        res['fullname']=username.first_name
                        res['mobile_number']=c_user.Mobile_Number
                        res['alt_number']=c_user.alt_number
                        res['total']=i['total']
                        res['locationname']=locationname
                        res['pincode']=pincode
                        res['delivery_charges']=delivery_charges
                        res['address']=i['Address']
                        res['city']=i['City']
                        res['state']=i['State']
                        res['street']=i['street']
                        res['delivery_boy_name']=''
                        res['delivery_status']=i['delivery_status']
                        res['date']=i['create_timestamp']
                        res['product_details']=[]
                    item=OrderItems.objects.filter(OrderDetails_id=i['id'])

                    for l in item:

                        res['product_details'].append({
                        'product_name':l.Product_ID.Product_Name,
                        'quantity':l.quantity,
                        'product_image':str(l.Product_ID.Product_Image),
                        'size':l.size,
                        'color':l.color,
                        # 'date':l.create_timestamp
                        })
                    Arr.append(res)
            return Response(Arr)


            # for i in tests:
            #     item=OrderItems.objects.filter(OrderDetails_id=i.id)
            #     print(item,'ite')
            #     for k in item:
            #         product_name.append(k.Product_ID.Product_Name)
            #     address=User_Address.objects.filter(user_id=i.user_id,delfault_address=True)
            #     for j in address:
            #         address=j.Address
            #         city=j.City
            #         state=j.State
            #         street=j.street
            #
            #     Arr.append({
            #     'id':i.id,
            #     'user_id':i.user_id,
            #     'username':i.user.username,
            #     'total':i.total,
            #     'locationname':i.shippingcharges.locationname,
            #     'pincode':i.shippingcharges.pincode,
            #     'delivery_charges':i.shippingcharges.amount,
            #     'address':address,
            #     'city':city,
            #     'state':state,
            #     'street':street,
            #     'product_name':product_name,
            #     })
            # return Response(Arr)




    def post(self,request):
        data = request.data
        user_id = data.get('user_id')
        total = data.get('total')
        shippingcharges_id=data.get('shippingcharges_id')
        print(data,'data')

        # PaymentDetails= data.get('PaymentDetails')

        data=    OrderDetails.objects.create(user_id=user_id,
                                        total=total,
                                        shippingcharges_id=shippingcharges_id)



        return Response({'result':'Created'})

    def put(self,request,pk):
        data = request.data
        # user_id = data.get('user_id')
        # total = data.get('total')
        # shippingcharges=data.get('shippingcharges_id')
        delivery_boy_id=data.get('delivery_boy_id')
        delivery_status=data.get('delivery_status')
        id=kri8evTeam.objects.get(user_id=delivery_boy_id)
        if delivery_status:


            data =OrderDetails.objects.filter(id=pk).update(delivery_boy_id=id.id,delivery_status=delivery_status)
                                        # total=total,
                                        # shippingcharges_id=shippingcharges)
        else:
            data =OrderDetails.objects.filter(id=pk).update(delivery_boy_id=id.id)



        return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = OrderDetails.objects.filter(id=pk).delete()
        return Response(all_values)


class PaymentDetailsApi(APIView):
    queryset = PaymentDetails.objects.all().values()

    def get(self,request):

        user_id = request.query_params.get('user_id')
        if PaymentDetails.objects.filter(custom_user_id=user_id).exists():
            test1 =PaymentDetails.objects.filter(custom_user_id=user_id).values()
            return Response({'result':{'All PaymentDetails':test1}})

        else:
            return Response({'result':'Id doesnt exists'})

    def post(self,request):
        data = request.data
        custom_user_id=data.get('user_id')
        orderdetails_id = data.get('orderdetails_id')
        amount= data.get('amount')
        provider= data.get('provider')
        status= data.get('status')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        Arr=[]

        order_details = OrderDetails.objects.all()

        for i in order_details:

            get_data = PaymentDetails.objects.filter(orderdetails_id = i.id).values('orderdetails_id')

            get_order_id = OrderDetails.objects.filter(id__in = get_data ).values('custom_user_id')

            filter_order = OrderDetails.objects.filter(custom_user_id__in = custom_user_id).values('id')
            print(filter_order,"filterrrrrrrr")
            final_data = PaymentDetails.objects.filter(orderdetails_id__in = filter_order).values()
            print(final_data,"Finalllllll")

            print(get_data,'printtttttttttttttttttt')
            print(get_order_id,'sampleeeeeeeeeeeeeeeee')


            Arr.append({
                # 'data':get_data,
                # 'response':get_order_id,
                'final_data':final_data

            })

        return Response({'result':final_data})

        # payment = PaymentDetails.objects.prefetch_related(OrderDetails_id).get(amount).prefetch_related(provider).prefetch_related(status).prefetch_related(create_timestamp).prefetch_related(last_update_timestamp).prefetch_related(Custom_User_id)
        # # payment = PaymentDetails.objects.get(OrderDetails_id).prefetch_related(amount).prefetch_related(provider).prefetch_related(status).prefetch_related(create_timestamp).prefetch_related(last_update_timestamp)

        # user_list=[]
        # for OrderDetails in payment.PaymentDetails.all():
        #     OrderDetails = {}

        #     OrderDetails['OrderDetails_id'] = OrderDetails.OrderDetails_id
        #     OrderDetails['amount']=OrderDetails.amount
        #     OrderDetails['Custom_User_id']=OrderDetails.Custom_User_id
        #     OrderDetails['provider']=OrderDetails.provider
        #     OrderDetails['create_timestamp']=OrderDetails.create_timestamp
        #     OrderDetails['last_update_timestamp']=OrderDetails.last_update_timestamp

        # result = {}
        # # result['id']=payment.pk
        # # result['name']=payment.name
        # result['users']=user_list



        # selected_page_no = 1
        # page_number = request.GET.get('page')
        # if page_number:
        #     selected_page_no = int(page_number)

        # if PaymentDetails.objects.filter(amount=amount).exists():
        #     return Response({'result':'Exists'})
        # else:
        #     PaymentDetails.objects.create(OrderDetails_id = OrderDetails,
        #                                     amount=amount,
        #                                         provider=provider,
        #                                         status=status,
        #                                         create_timestamp=create_timestamp,
        #                                         last_update_timestamp=last_update_timestamp,
        #                                         Custom_User_id=Custom_User)

        #     posts = PaymentDetails.objects.all().values()
        #     paginator = Paginator(posts,3)
        #     try:
        #         page_obj = paginator.get_page(selected_page_no)
        #     except PageNotAnInteger:
        #         page_obj = paginator.page(1)
        #     except EmptyPage:
        #         page_obj = paginator.page(paginator.num_pages)
        #     return Response({'result':'Created', 'data':list(page_obj)})


    def put(self,request,pk):
        data = request.data
        OrderDetails = data.get('OrderDetails_id')
        amount= data.get('amount')
        provider= data.get('provider')
        status= data.get('status')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        if PaymentDetails.objects.filter(amount=amount).exists():
            return Response({'result':' amount already exists'})
        else:
            PaymentDetails.objects.filter(id=pk).update(OrderDetails_id = OrderDetails,
                                                amount=amount,
                                                provider=provider,
                                                status=status,
                                                create_timestamp=create_timestamp,
                                                last_update_timestamp=last_update_timestamp
                                            )#OrderDetails_id = OrderDetails,
            return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = PaymentDetails.objects.filter(id=pk).delete()
        return Response(all_values)


class OrderItemsApi(APIView):
    queryset = OrderItems.objects.all().values()

    def get(self,request):
        all_values = OrderItems.objects.all().values()
        return Response(all_values)

        # test = request.query_params.get('Custom_User_id')
        # if OrderItems.objects.filter(Custom_User_id=test).exists():
        #     test1 =OrderItems.objects.filter(Custom_User_id=test).values()
        #     return Response({'result':{'All PaymentDetails':test1}})

        # else:
        #     return Response({'result':'Id doesnt exists'})

    def post(self,request):
        data = request.data
        OrderDetails= data.get('OrderDetails_id')
        Product_ID= data.get('Product_ID_id')
        quantity= data.get('quantity')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp = data.get('last_update_timestamp')

        selected_page_no = 1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        if OrderItems.objects.filter(quantity=quantity).exists():
            return Response({'result':'quantity already exists'})
        else:
            OrderItems.objects.create(OrderDetails_id = OrderDetails,
                                               Product_ID_id=Product_ID,
                                                quantity=quantity,
                                                create_timestamp=create_timestamp,
                                                last_update_timestamp=last_update_timestamp)

            posts = OrderItems.objects.all().values()
            paginator = Paginator(posts,3)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':'Created', 'data':list(page_obj)})


    def put(self,request,pk):
        data = request.data
        OrderDetails = data.get('OrderDetails_id')
        Product_ID= data.get('Product_ID_id')
        quantity= data.get('quantity')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp = data.get('last_update_timestamp')

        if OrderItems.objects.filter(quantity=quantity).exists():
            return Response({'result':'quantity already exists'})
        else:
            OrderItems.objects.filter(id=pk).update(OrderDetails_id = OrderDetails,
                                                Product_ID_id=Product_ID,
                                                quantity=quantity,
                                                create_timestamp=create_timestamp,
                                                last_update_timestamp=last_update_timestamp
                                            )
            return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = OrderItems.objects.filter(id=pk).delete()
        return Response(all_values)



class ShoppingSessionApi(APIView):
    queryset = ShoppingSession.objects.all().values()

    def get(self,request):

        user_id = request.query_params.get('user_id')
        if user_id:
            test1 =ShoppingSession.objects.filter(user_id=user_id).values()
            return Response({'result':{'All PaymentDetails':test1}})
        else:
            test1 =ShoppingSession.objects.all().values()
            return Response({'result':{'All PaymentDetails':test1}})


    def post(self,request):
        data = request.data
        user_id=data.get('user_id')
        total=data.get('total')


        obj=ShoppingSession.objects.filter(user_id=user_id)
        if obj:
            for i in obj:
                totals=int(i.total)
                ids=i.id
            data=ShoppingSession.objects.filter(user_id=user_id).update(total=int(totals)+1)

            return Response({'shopping_session_id':ids})
        else:
            data=ShoppingSession.objects.create(user_id=user_id,total=total)
            return Response({'shopping_session_id':data.id})





    def put(self,request,pk):
        data = request.data
        custom_user=data.get('user_id')
        total=data.get('total')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp = data.get('last_update_timestamp')

        if ShoppingSession.objects.filter(total=total).exists():
            return Response({'result':'Exists'})
        else:
            ShoppingSession.objects.filter(id=pk).update(custom_user_id=custom_user,
                                                total=total,
                                                create_timestamp=create_timestamp,
                                                last_update_timestamp=last_update_timestamp
                                            )
            return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = ShoppingSession.objects.filter(id=pk).delete()
        return Response(all_values)



class Get_CartItemApi(APIView):
    queryset = CartItem.objects.all().values()

    def get(self,request):

        # user_id = request.query_params.get('user_id')
        data=[]

        test1 =CartItem.objects.all()
        for i in test1:
            data.append({
            'id':i.id,
            'ShoppingSession_id':i.ShoppingSession_id,
            'username':i.ShoppingSession.user.username,
            'quantity':i.quantity,
            'product_id':i.Product_ID_id,

            'product_name':i.Product_ID.Product_Name,
            'product_Image':str(i.Product_ID.Product_Image),
            'Product_Selling_Price':i.Product_ID.Product_Selling_Price
            })
        return Response(data)




class Buy_NowCartItemApi(APIView):
    def get(self,request):
        user_id = request.query_params.get('user_id')
        ShoppingSessions=ShoppingSession.objects.get(user_id=user_id)

        buy_now_data=[]
        test1 =Buy_NowCartItem.objects.filter(ShoppingSession_id=ShoppingSessions.id)
        count=0
        count1=0
        for i in test1:
            if i.selectedoptions:
                res=eval(i.selectedoptions)
                if res[1].upper()=='S' or res[1].upper()=='M' or res[1].upper()=='L' or res[1].upper()=='XL' or res[1].upper()=='XXL' or res[1].upper()=='XXXL':

                    buy_now_data.append({
                    # 'attribute':res[0],
                    'size':res[1],
                    'color':res[0],
                    'id':i.id,
                    'ShoppingSession_id':i.ShoppingSession_id,
                    'quantity':int(i.quantity),
                    'product_id':i.Product_ID_id,
                    'brand_name':i.Product_ID.brand.brand_name,

                    'product_name':i.Product_ID.Product_Name,
                    'product_Image':str(i.Product_ID.Product_Image),
                    'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                    'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                    })
                else:
                    buy_now_data.append({
                    # 'attribute':res[0],
                    'size':res[0],
                    'color':res[1],
                    'id':i.id,
                    'ShoppingSession_id':i.ShoppingSession_id,
                    'quantity':int(i.quantity),
                    'product_id':i.Product_ID_id,
                    'brand_name':i.Product_ID.brand.brand_name,

                    'product_name':i.Product_ID.Product_Name,
                    'product_Image':str(i.Product_ID.Product_Image),
                    'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                    'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                    })
                count=count+1
                count1=count1+1
            else:
                buy_now_data.append({
                # 'attribute':res[0],
                'size':'',
                'color':'',
                'id':i.id,
                'ShoppingSession_id':i.ShoppingSession_id,
                'quantity':int(i.quantity),
                'product_id':i.Product_ID_id,
                'brand_name':i.Product_ID.brand.brand_name,

                'product_name':i.Product_ID.Product_Name,
                'product_Image':str(i.Product_ID.Product_Image),
                'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                })



        return Response(buy_now_data)



    def post(self,request):
        data = request.data
        ShoppingSession=data.get('shopping_session_id')
        Product_ID=data.get('Product_ID')
        quantity=data.get('quantity')
        attributeSize =data.get('attributeSize')
        attributeColor =data.get('attributeColor')
        user_id =data.get('user_id')
        response = {}
        b=[]


        buy_now_data=[]
        count=0

        # if User_Address.objects.filter(user_id=user_id).exists():

        if attributeSize:
            a=[]
            for l in range(len(attributeSize)):
                e=(list(attributeSize[l].values()))

                attributes_id=e[1]
                option=e[2]
                st=e[3]
                if st==True:
                    count=count+1
                    a.append(option)

            if count!=2:
                response['error'] = {'error': {
                'detail': 'Please selcect your color/size!', 'status': status.HTTP_401_UNAUTHORIZED}}

                return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)
            else:
                val=Buy_NowCartItem.objects.filter(Q(ShoppingSession_id=ShoppingSession))
                if val:
                    val=Buy_NowCartItem.objects.filter(Q(ShoppingSession_id=ShoppingSession)).delete()
                    value=Buy_NowCartItem.objects.create(ShoppingSession_id=ShoppingSession,
                                            Product_ID_id=Product_ID,
                                            quantity=quantity)
                    Arr=[]
                    a=[]

                    if attributeSize:
                        for l in range(len(attributeSize)):
                            e=(list(attributeSize[l].values()))

                            attributes_id=e[1]
                            option=e[2]
                            st=e[3]
                            if st==True:
                                a.append(option)
                                datas=ProductAttributes.objects.filter(Q(user_id=user_id)&Q(Product_ID_id=Product_ID))
                                if datas:
                                    datas=ProductAttributes.objects.filter(Q(user_id=user_id)&Q(Product_ID_id=Product_ID)).delete()

                                data=ProductAttributes.objects.create(user_id=user_id,attributes_id=attributes_id,Product_ID_id=Product_ID,selectedoptions=option)
                        cart=Buy_NowCartItem.objects.filter(id=value.id).update(selectedoptions=a)


                        test1 =Buy_NowCartItem.objects.filter(ShoppingSession_id=ShoppingSession)
                        count=0
                        count1=0
                        for i in test1:
                            if i.selectedoptions:
                                res=eval(i.selectedoptions)
                                if res[1].upper()=='S' or res[1].upper()=='M' or res[1].upper()=='L' or res[1].upper()=='XL' or res[1].upper()=='XXL' or res[1].upper()=='XXXL':

                                    buy_now_data.append({
                                    # 'attribute':res[0],
                                    'size':res[1],
                                    'color':res[0],
                                    'id':i.id,
                                    'ShoppingSession_id':i.ShoppingSession_id,
                                    'quantity':int(i.quantity),
                                    'product_id':i.Product_ID_id,
                                    'brand_name':i.Product_ID.brand.brand_name,

                                    'product_name':i.Product_ID.Product_Name,
                                    'product_Image':str(i.Product_ID.Product_Image),
                                    'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                                    'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                                    })
                                else:
                                    buy_now_data.append({
                                    # 'attribute':res[0],
                                    'size':res[0],
                                    'color':res[1],
                                    'id':i.id,
                                    'ShoppingSession_id':i.ShoppingSession_id,
                                    'quantity':int(i.quantity),
                                    'product_id':i.Product_ID_id,
                                    'brand_name':i.Product_ID.brand.brand_name,

                                    'product_name':i.Product_ID.Product_Name,
                                    'product_Image':str(i.Product_ID.Product_Image),
                                    'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                                    'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                                    })
                                count=count+1
                                count1=count1+1
                            else:
                                buy_now_data.append({
                                # 'attribute':res[0],
                                'size':'',
                                'color':'',
                                'id':i.id,
                                'ShoppingSession_id':i.ShoppingSession_id,
                                'quantity':int(i.quantity),
                                'product_id':i.Product_ID_id,
                                'brand_name':i.Product_ID.brand.brand_name,

                                'product_name':i.Product_ID.Product_Name,
                                'product_Image':str(i.Product_ID.Product_Image),
                                'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                                'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                                })



                        return Response(buy_now_data)






                else:
                    value=Buy_NowCartItem.objects.create(ShoppingSession_id=ShoppingSession,
                                            Product_ID_id=Product_ID,
                                            quantity=quantity)

                Arr=[]
                a=[]

                if attributeSize:
                    for l in range(len(attributeSize)):
                        e=(list(attributeSize[l].values()))

                        attributes_id=e[1]
                        option=e[2]
                        st=e[3]
                        if st==True:
                            a.append(option)
                            datas=ProductAttributes.objects.filter(Q(user_id=user_id)&Q(Product_ID_id=Product_ID))
                            if datas:
                                datas=ProductAttributes.objects.filter(Q(user_id=user_id)&Q(Product_ID_id=Product_ID)).delete()

                            data=ProductAttributes.objects.create(user_id=user_id,attributes_id=attributes_id,Product_ID_id=Product_ID,selectedoptions=option)
                    cart=Buy_NowCartItem.objects.filter(id=value.id).update(selectedoptions=a)



                    test1 =Buy_NowCartItem.objects.filter(ShoppingSession_id=ShoppingSession)
                    count=0
                    count1=0
                    for i in test1:
                        if i.selectedoptions:
                            res=eval(i.selectedoptions)
                            if res[1].upper()=='S' or res[1].upper()=='M' or res[1].upper()=='L' or res[1].upper()=='XL' or res[1].upper()=='XXL' or res[1].upper()=='XXXL':

                                buy_now_data.append({
                                # 'attribute':res[0],
                                'size':res[1],
                                'color':res[0],
                                'id':i.id,
                                'ShoppingSession_id':i.ShoppingSession_id,
                                'quantity':int(i.quantity),
                                'product_id':i.Product_ID_id,
                                'brand_name':i.Product_ID.brand.brand_name,

                                'product_name':i.Product_ID.Product_Name,
                                'product_Image':str(i.Product_ID.Product_Image),
                                'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                                'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                                })
                            else:
                                buy_now_data.append({
                                # 'attribute':res[0],
                                'size':res[0],
                                'color':res[1],
                                'id':i.id,
                                'ShoppingSession_id':i.ShoppingSession_id,
                                'quantity':int(i.quantity),
                                'product_id':i.Product_ID_id,
                                'brand_name':i.Product_ID.brand.brand_name,

                                'product_name':i.Product_ID.Product_Name,
                                'product_Image':str(i.Product_ID.Product_Image),
                                'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                                'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                                })
                            count=count+1
                            count1=count1+1
                        else:
                            buy_now_data.append({
                            # 'attribute':res[0],
                            'size':'',
                            'color':'',
                            'id':i.id,
                            'ShoppingSession_id':i.ShoppingSession_id,
                            'quantity':int(i.quantity),
                            'product_id':i.Product_ID_id,
                            'brand_name':i.Product_ID.brand.brand_name,

                            'product_name':i.Product_ID.Product_Name,
                            'product_Image':str(i.Product_ID.Product_Image),
                            'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                            'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                            })



                    return Response(buy_now_data)


                else:

                    response['error'] = {'error': {
                            'detail': 'Please selcect your color/size!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)

                wish=Wishlist.objects.filter(user_id=user_id,product_id=Product_ID).delete()
                return Response({'result':'Created'})

        response['error'] = {'error': {
        'detail': 'Please selcect your color/size!', 'status': status.HTTP_401_UNAUTHORIZED}}

        return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)
        # else:
        #     response['error'] = {'error': {
        #     'detail': 'Please add your default address!', 'status': status.HTTP_401_UNAUTHORIZED}}
        #
        #     return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)





class CartItemApi(APIView):
    queryset = CartItem.objects.all().values()

    def get(self,request):

        user_id = request.query_params.get('user_id')
        data=[]
        Arr1=[]
        Arr2=[]
        new=[]
        if user_id:
            shoppingsession=ShoppingSession.objects.filter(user_id=user_id)

            if shoppingsession:
                for k in shoppingsession:
                    ids=k.id

                test1 =CartItem.objects.filter(ShoppingSession_id=ids)
                count=0
                count1=0
                for i in test1:
                    if i.selectedoptions:
                        res=eval(i.selectedoptions)
                        if res[1].upper()=='S' or res[1].upper()=='M' or res[1].upper()=='L' or res[1].upper()=='XL' or res[1].upper()=='XXL' or res[1].upper()=='XXXL':
                            data.append({
                            'size':res[1],
                            'color':res[0],
                            'id':i.id,
                            'ShoppingSession_id':i.ShoppingSession_id,
                            'quantity':int(i.quantity),
                            'product_id':i.Product_ID_id,
                            'brand_name':i.Product_ID.brand.brand_name,

                            'product_name':i.Product_ID.Product_Name,
                            'product_Image':str(i.Product_ID.Product_Image),
                            'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                            'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                            })
                        else:
                            data.append({
                            'size':res[0],
                            'color':res[1],
                            'id':i.id,
                            'ShoppingSession_id':i.ShoppingSession_id,
                            'quantity':int(i.quantity),
                            'product_id':i.Product_ID_id,
                            'brand_name':i.Product_ID.brand.brand_name,

                            'product_name':i.Product_ID.Product_Name,
                            'product_Image':str(i.Product_ID.Product_Image),
                            'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                            'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                            })

                        count=count+1
                        count1=count1+1
                    else:
                        data.append({
                        # 'attribute':res[0],
                        'size':'',
                        'color':'',
                        'id':i.id,
                        'ShoppingSession_id':i.ShoppingSession_id,
                        'quantity':int(i.quantity),
                        'product_id':i.Product_ID_id,
                        'brand_name':i.Product_ID.brand.brand_name,

                        'product_name':i.Product_ID.Product_Name,
                        'product_Image':str(i.Product_ID.Product_Image),
                        'Product_Selling_Price':int(i.Product_ID.Product_Selling_Price),
                        'total':int(i.Product_ID.Product_Selling_Price)*int(i.quantity)
                        })



                return Response(data)

            else:
                return Response({'result':'data not available for this user'})
        else:
            return Response({'result':'user id required'})

    def post(self,request):
        data = request.data
        ShoppingSession=data.get('shopping_session_id')
        Product_ID=data.get('Product_ID')
        quantity=data.get('quantity')
        attributeSize =data.get('attributeSize')
        attributeColor =data.get('attributeColor')
        user_id =data.get('user_id')
        response = {}
        b=[]
        count=0


        if attributeSize:
            for l in range(len(attributeSize)):
                e=(list(attributeSize[l].values()))

                attributes_id=e[1]
                option=e[2]
                st=e[3]
                if st==True:
                    count=count+1
                    b.append(option)
            if count!=2:
                response['error'] = {'error': {
                'detail': 'Please selcect your color/size!', 'status': status.HTTP_401_UNAUTHORIZED}}

                return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)
            else:
                val=CartItem.objects.filter(Q(ShoppingSession_id=ShoppingSession)&Q(Product_ID_id=Product_ID)&Q(selectedoptions=b))
                print(val,'val')
                if val:
                    for i in val:
                        qunt=i.quantity
                    # vals=CartItem.objects.filter(ShoppingSession_id=ShoppingSession,Product_ID_id=Product_ID).update(quantity=int(qunt)+1)
                    vals=CartItem.objects.filter(ShoppingSession_id=ShoppingSession,Product_ID_id=Product_ID).update(quantity=int(qunt)+1)
                    # value=CartItem.objects.create(ShoppingSession_id=ShoppingSession,
                    #                         Product_ID_id=Product_ID,
                    #                         quantity=quantity)
                    return Response({'result':'Created'})

                else:
                    value=CartItem.objects.create(ShoppingSession_id=ShoppingSession,
                                            Product_ID_id=Product_ID,
                                            quantity=quantity)

                Arr=[]
                a=[]
                # val=ProductAttributes.objects.filter(user_id=user_id,Product_ID_id=Product_ID)
                # if val:
                #     val=ProductAttributes.objects.filter(user_id=user_id,Product_ID_id=Product_ID).delete()
                if attributeSize:
                    for l in range(len(attributeSize)):
                        e=(list(attributeSize[l].values()))

                        attributes_id=e[1]
                        option=e[2]
                        st=e[3]
                        if st==True:
                            a.append(option)
                            data=ProductAttributes.objects.create(user_id=user_id,attributes_id=attributes_id,Product_ID_id=Product_ID,selectedoptions=option)
                    cart=CartItem.objects.filter(id=value.id).update(selectedoptions=a)


                else:
                    # return Response({
                    #     'error':{'message':'Please selcect your size!',
                    #     'status_code':status.HTTP_404_NOT_FOUND,
                    #     }},status=status.HTTP_404_NOT_FOUND)
                    response['error'] = {'error': {
                            'detail': 'Please selcect your color/size!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)

                # if attributeColor:
                #     for l in range(len(attributeColor)):
                #         e=(list(attributeColor[l].values()))
                #         attributes_id=e[1]
                #         option=e[2]
                #
                #         data=ProductAttributes.objects.create(user_id=user_id,attributes_id=attributes_id,Product_ID_id=Product_ID,selectedoptions=option)
                # else:
                #     # return Response({
                #     #     'error':{'message':'Please selcect your color!',
                #     #     'status_code':status.HTTP_404_NOT_FOUND,
                #     #     }},status=status.HTTP_404_NOT_FOUND)
                #     response['error'] = {'error': {
                #             'detail': 'Please selcect your color!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)


                wish=Wishlist.objects.filter(user_id=user_id,product_id=Product_ID).delete()
                # wish=Product.objects.filter(id=Product_ID).update(wishlistss=False)
                return Response({'result':'Created'})

        response['error'] = {'error': {
        'detail': 'Please selcect your color/size!', 'status': status.HTTP_401_UNAUTHORIZED}}

        return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)


    def put(self,request,pk):
        data = request.data
        ShoppingSession=data.get('ShoppingSession_id')
        Product_ID=data.get('Product_ID')
        quantity=data.get('quantity')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp = data.get('last_update_timestamp')


        if CartItem.objects.filter(quantity=quantity).exists():
            return Response({'result':' quantity already exists'})
        else:
            CartItem.objects.filter(id=pk).update(ShoppingSession_id=ShoppingSession,
                                    Product_ID_id=Product_ID,
                                    quantity=quantity,
                                    create_timestamp=create_timestamp,
                                    last_update_timestamp=last_update_timestamp
                                            )
            return Response({'result':'Updated'})

    def delete(self,request,pk):
        # all_values = CartItem.objects.filter(id=pk)
        # for i in all_values:
        #     Product_ID=i.Product_ID_id
        #     selectedoptions=i.selectedoptions
        #     ShoppingSession=ShoppingSession.objects.get(id=i.ShoppingSession_id)
        #
        #     data=ProductAttributes.objects.filter(user_id=ShoppingSession.user_id,Product_ID_id=i.Product_ID_id,selectedoptions=i.selectedoptions).delete()
        all_values = CartItem.objects.filter(id=pk).delete()

        return Response(all_values)


class Quantity_update_CartItemApi(APIView):
    def put(self,request,pk):
        data = request.data
        ShoppingSession=data.get('ShoppingSession_id')
        Product_ID=data.get('Product_ID')
        quantity=data.get('quantity')
        size=data.get('size')


        # user_id=ShoppingSession.objects.filter(id=ShoppingSession)
        # for i in user_id:
        #     u_id=i.user_id
        data=CartItem.objects.filter(id=pk).update(quantity=quantity)
        # size_update=ProductAttributes.objects.filter(user_id=u_id,Product_ID_id=Product_ID)
        # for j in size_update:
        # attr=Attributes.objects.filter(Product_ID_id=Product_ID,name='Size')
        # for k in attr:
        #     size_update=ProductAttributes.objects.filter(attributes_id=id).update(selectedoptions=size)


        return Response({'result':'Updated'})


class LeaderBoardOneApi(APIView):

    def get(self,request):
        Arr=[]
        user_id = request.query_params.get('user_id')
        if LeaderBoardOne.objects.filter(user_id=user_id).exists():
            test1 =LeaderBoardOne.objects.filter(user_id=user_id)
            for i in test1:
                custom=Custom_User.objects.filter(user_id=user_id)
                for k in custom:
                    code=k.user_to_user_refcode
                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'code':code,
                'points':i.points,

                })
            return Response(Arr)

        else:
            return Response({'result':'Id doesnt exists'})




class OrderDetailItemApi(APIView):
    # queryset = OrderDetails.objects.all()
    def get(self,request):
        order_detail_id = request.query_params.get('order_id')

        order_details = OrderDetails.objects.get(id=order_detail_id)
        order_item = OrderItems.objects.filter(OrderDetails_id=order_detail_id).values()
        order_payments = PaymentDetails.objects.filter(orderdetails_id=order_detail_id).values()
        return Response({'result':{'order_details':{'id':order_details.id,'custom_user':order_details.custom_user_id,'total':order_details.total,
            'create_timestamp':order_details.create_timestamp,
            'last_update_timestamp':order_details.last_update_timestamp},'order_item':order_item,'order_payments':order_payments}})



class User_PromoDetailsApi(APIView):
    def get(self,request):
        user_id =self.request.query_params.get('user_id')
        Arr=[]

        promo_data = PromoCode.objects.all().order_by('-id')
        for i in promo_data:
            if i.status=="Active":
                if i.marketer_id==None:

                    user=User.objects.all()
                    for k in user:
                        assign_code_user=User_PromoDetails.objects.filter(Q(user_id=k.id)&Q(code=i.Code)&Q(Expiry_Timestamp=i.Expiry_Timestamp)&Q(discount=i.discount))
                        if assign_code_user:
                            pass
                        else:
                            assign_code_user=User_PromoDetails.objects.create(user_id=k.id,code=i.Code,status=i.status,quantity=i.quantity,Expiry_Timestamp=i.Expiry_Timestamp,discount=i.discount)
                else:
                    pass
            else:
                pass

        today = datetime.date.today()
        u_promo=User_PromoDetails.objects.filter(Q(Expiry_Timestamp__lt=today)).update(status='Inactive')

        promo_data = User_PromoDetails.objects.filter(Q(user_id=user_id)&Q(status='Active'))
        if promo_data:
            for i in promo_data:
                print(i.quantity,'quanttttttttttttttt')
                if int(i.quantity)>0:
                    Arr.append({
                    'id':i.id,
                    'promo_code_name':i.code,
                    'discount':i.discount,
                    'status':i.status,
                    'quantity':i.quantity,
                    'expiry_timestamp':i.Expiry_Timestamp,

                    })
            return Response(Arr)

class PromoCodeApi(APIView):
    def get(self,request):

        id =self.request.query_params.get('id')
        marketer_id =self.request.query_params.get('marketer_id')
        Arr=[]
        today = datetime.date.today()
        promo=PromoCode.objects.filter(Q(Expiry_Timestamp__lt=today)).update(status='Inactive')
        # u_promo=User_PromoDetails.objects.filter(Q(Expiry_Timestamp__lt=today)).update(status='Inactive')

        if marketer_id:
            promo_data = PromoCode.objects.filter(marketer_id=marketer_id).order_by('-id')
            for i in promo_data:
                Arr.append({
                'id':i.id,
                # 'product':i.product_id,
                # 'product_name':i.product.Product_Name,
                'promo_code_name':i.Code,
                'discount':i.discount,
                'status':i.status,
                'quantity':i.quantity,
                'marketer_id':i.marketer_id,
                'expiry_timestamp':i.Expiry_Timestamp,

                })

            return Response(Arr)


        if id:

            promo_data = PromoCode.objects.filter(id=id)
            for i in promo_data:

                Arr.append({
                'id':i.id,
                # 'product':i.product_id,
                # 'product_name':i.product.Product_Name,
                'promo_code_name':i.Code,
                'discount':i.discount,
                'status':i.status,
                'quantity':i.quantity,
                'marketer_id':i.marketer_id,
                'expiry_timestamp':i.Expiry_Timestamp,

                })

            return Response(Arr)
        else:

            promo_data = PromoCode.objects.all().order_by('-id')
            for i in promo_data:


                Arr.append({
                'id':i.id,
                # 'product':i.product_id,
                # 'product_name':i.product.Product_Name,
                'promo_code_name':i.Code,
                'discount':i.discount,
                'status':i.status,
                'quantity':i.quantity,
                'marketer_id':i.marketer_id,
                'expiry_timestamp':i.Expiry_Timestamp,

                })
            return Response(Arr)

    def post(self,request):
        data = request.data
        discount = data.get('discount')
        Expiry_Timestamp= data.get('Expiry_Timestamp')
        quantity = data.get('no_of_code')
        marketer_id = data.get('marketer_id')


        code_quantity = data.get('code_quantity')

        if marketer_id:
            data = 'KRI8'
            count=0
            for i in range(int(code_quantity)):
                # count=int(count)+1
                alpha=random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                alpha1=random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                access= random.randint(1000, 9999)
                new_code=data+str(alpha)+str(alpha1)+str(access)
                if PromoCode.objects.filter(Q(Code=new_code)&Q(status='Active')).exists():
                    count=int(count)+1
                    pass
                else:
                    reg_create = PromoCode.objects.create(status='Active',Code=new_code,Expiry_Timestamp=Expiry_Timestamp,discount=discount,marketer_id=marketer_id)

            if count==0:
                response="Access Code Created Sucessfully"
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                # value=int(code_quantity)-count
                # response="We are unable to create %s promocode please try again",% (count)
                # response="We are unable to create {0} promocode please try again",.format(count)
                response="We are unable to create some promocode please try again"
                return Response(response, status=status.HTTP_201_CREATED)


        else:
            new_code=''
            codesss=[]
            response=''
            str1=''
            data='KRI8EVE'
            course = PromoCode.objects.all().last()
            if course:
                no=course.Code
                no=list(no)
                st=no[7:12]
                for ele in st:
                    str1 += ele
                count=int(str1)
                # for i in range(int(no_of_code)):
                count=int(count)+1
                new_code=data+str(count)
                if PromoCode.objects.filter(Q(Code=new_code)&Q(status='Active')).exists():
                    response="Unable to create promocode try again"
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                else:
                    reg_create = PromoCode.objects.create(status='Active',Code=new_code,Expiry_Timestamp=Expiry_Timestamp,discount=discount,quantity=quantity,marketer_id=marketer_id)
                    # user=User.objects.all()
                    # for k in user:
                    #     assign_code_user=User_PromoDetails.objects.create(user_id=k.id,code=new_code,status='Active',quantity=quantity,Expiry_Timestamp=Expiry_Timestamp,discount=discount)
                response="Promo Code Created Sucessfully"
                return Response(response, status=status.HTTP_201_CREATED)

            else:
                count=1000
                # for i in range(int(no_of_code)):
                count=int(count)+1

                new_code=data+str(count)
                if PromoCode.objects.filter(Q(Code=new_code)&Q(status='Active')).exists():
                    response="Unable to create promocode try again"
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    reg_create = PromoCode.objects.create(status='Active',Code=new_code,Expiry_Timestamp=Expiry_Timestamp,discount=discount,quantity=quantity,marketer_id=marketer_id)

                response="Promo Code Created Sucessfully"
                return Response(response, status=status.HTTP_404_NOT_FOUND)









    def put(self,request,pk):
        data = request.data

        Code = data.get('Code')
        discount = data.get('discount')
        Expiry_Timestamp=data.get('Expiry_Timestamp')



        data=PromoCode.objects.filter(id=pk).update(Code=Code,discount=discount,
                                        Expiry_Timestamp=Expiry_Timestamp)

        return Response({'result':'Updated'})

    def delete(self,request,pk):
        # all_values = PromoCode.objects.filter(id=pk).delete()

        promo_data = PromoCode.objects.filter(id=pk)
        for i in promo_data:
            user=User.objects.all()
            for k in user:
                assign_code_user=User_PromoDetails.objects.filter(Q(user_id=k.id)&Q(code=i.Code)).delete()
        all_values = PromoCode.objects.filter(id=pk).delete()
        return Response({'result':'Deleted'})



class Promo_code_validationsAPIView(APIView):
    def post(self, request):
        data = request.data
        code = data.get('code')
        ShoppingSession_id = data.get('ShoppingSession_id')

        Arr=[]
        response='invalid code'
        # data=CartItem.objects.filter(ShoppingSession_id=ShoppingSession_id)
        # for k in data:
        today = datetime.date.today()
        promo=PromoCode.objects.filter(Q(Expiry_Timestamp__lt=today)).update(status='Inactive')
        # st_promo=User_PromoDetails.objects.filter(Q(Expiry_Timestamp__lt=today)).update(status='Inactive')
        reg_create = PromoCode.objects.all()
        for i in reg_create:
            print(i.Code)
            print(code)
            if str(i.Code) == code and i.status=='Active':
                    Arr.append({
                    'code':i.Code,
                    'discount':i.discount
                    })
                    return Response(Arr)
            # else:
                # response="invalid code"
                # return Response(response, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     response=" code not available for this product"
        #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ShippingChargesApi(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            test1 = ShippingCharges.objects.filter(id=id).values()
            return Response(test1)


        else:
            test1 = ShippingCharges.objects.all().values()
            return Response({'result':{'all_shipping_charges':test1}})



    def post(self,request):
        data = request.data

        locationname = data.get('locationname')
        pincode= data.get('pincode')
        amount= data.get('amount')
        days=data.get('days')



        data_create=ShippingCharges.objects.create(locationname=locationname,
                                            pincode=pincode,
                                            amount=amount,days=days)

        return Response({'result':'Created'})


    def put(self,request,pk):
        data = request.data

        locationname = data.get('locationname')
        pincode= data.get('pincode')
        amount= data.get('amount')
        days=data.get('days')



        data=ShippingCharges.objects.filter(id=pk).update(locationname=locationname,
                                            pincode=pincode,
                                            amount=amount,
                                            days=days)
        return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = ShippingCharges.objects.filter(id=pk).delete()
        return Response(all_values)


import datetime
class Shipping_validationApi(APIView):
    def get(self,request):
        pincode = request.query_params.get('pincode')
        Arr=[]
        test1 = ShippingCharges.objects.filter(pincode=pincode)
        if test1:
            for i in test1:
                today = datetime.date.today()
                next_date = today + datetime.timedelta(days=int(i.days))
                Arr.append({
                'id':i.id,
                'amount':i.amount,
                'date':next_date
                })
            return Response(Arr)
        else:
            return Response({'No shipping available for this pincode'})




class EnquiryAPIView(APIView):
    def get(self, request):

        id =self.request.query_params.get('id')
        if id:
            enq_data = Enquiry.objects.filter(id=id).values()
            return Response(enq_data)
        else:
            enq_data = Enquiry.objects.all().values()
            return Response(enq_data)

    def post(self, request):
        data = request.data


        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        location = data.get('location')
        school = data.get('school')
        comment = data.get('comment')
        enquiry_type = data.get('enquiry_type')



        enq_create = Enquiry.objects.create(name=name,email=email,phone_number=phone_number,location=location,school=school,comment=comment,enquiry_type=enquiry_type)
        return Response("Data Added Sucessfully")


    def put(self, request,pk):
        data = request.data

        if id:
            data = Enquiry.objects.filter(id=pk).update(name=data.get('name'),
                                                                    email = data.get('email'),
                                                                    phone_number = data.get('phone_number'),
                                                                    location = data.get('location'),
                                                                    school = data.get('school'),
                                                                    comment = data.get('comment'),
                                                                    enquiry_type = data.get('enquiry_type'),)

            if data:
                return JsonResponse({'message': 'Enquiry Updated Sucessfully.'})
            else:
                return JsonResponse({'message': ' Invalid Enquiry '})

        else:
            return JsonResponse({'message': 'Id Required for updating.'})

    def delete(self, request,pk):

        enq_data =Enquiry.objects.filter(id= pk)

        if len(enq_data) > 0:
            enq_data.delete()
            return Response("Enquiry  Deleted Sucessfully")
        else:
            return Response("Id Required for deleting.")


class Final_amountApi(APIView):
    def get(self,request):
        user_id = self.request.query_params.get('user_id')
        buy_now = self.request.query_params.get('buy_now')
        Arr=[]
        total_Mrp=0
        pin=0
        points=0
        five_percent=0
        dis_percent=0
        if buy_now=='true':

            pincode=User_Address.objects.filter(user_id=user_id,delfault_address=True)
            for j in pincode:
                pin=j.Pincode
            shipping=ShippingCharges.objects.filter(pincode=str(pin))
            if shipping:
                for m in shipping:
                    amount=m.amount
                shopping_session = ShoppingSession.objects.filter(user_id=user_id)
                for i in shopping_session:
                    test1 = Buy_NowCartItem.objects.filter(ShoppingSession_id=i.id)
                    # test1s =LeaderBoardOne.objects.filter(user_id=user_id)
                    # for l in test1s:
                    #     points=l.points
                    #     five_percent=int(l.points)*5/100
                    #     if int(five_percent)>50:
                    #         five_percent=50



                    for k in test1:
                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:
                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                            for b in dis:
                                dis_percent=dis_percent+int(b.Discount_Percentage)
                            after_discount=float(k.Product_ID.Product_Selling_Price)*dis_percent/100
                            f_price=float(k.Product_ID.Product_Selling_Price)-after_discount
                            dis_percent=0
                            total_Mrp=int(total_Mrp)+int(f_price)*int(k.quantity)


                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                        else:
                            total_Mrp=int(total_Mrp)+int(k.Product_ID.Product_Selling_Price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                Arr.append({
                'amount':0,
                'code':'',
                'discount':0,
                'total_Mrp':total_Mrp,
                'shipping_charge':amount,
                'total_amount':int(total_Mrp)+int(amount),
                'points':points,
                'five_percent':int(five_percent)
                })
                return Response(Arr)
            else:
                shopping_session = ShoppingSession.objects.filter(user_id=user_id)
                for i in shopping_session:
                    test1 = Buy_NowCartItem.objects.filter(ShoppingSession_id=i.id)

                    for k in test1:
                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:
                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                            for b in dis:
                                dis_percent=dis_percent+int(b.Discount_Percentage)
                            after_discount=float(k.Product_ID.Product_Selling_Price)*dis_percent/100
                            f_price=float(k.Product_ID.Product_Selling_Price)-after_discount
                            dis_percent=0
                            total_Mrp=int(total_Mrp)+int(f_price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                        else:
                            total_Mrp=int(total_Mrp)+int(k.Product_ID.Product_Selling_Price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50

                            coin=LeaderBoardOne.objects.filter(user_id=user_id)
                            for k in coin:
                                if int(k.points)>=int(five_percent):
                                    pass
                                else:
                                    five_percent=0

                Arr.append({
                'total_Mrp':total_Mrp,
                'shipping_charge':0,
                'total_amount':total_Mrp,
                'points':points,
                'five_percent':int(five_percent)

                })
                return Response(Arr)

        else:

            pincode=User_Address.objects.filter(user_id=user_id,delfault_address=True)
            for j in pincode:
                pin=j.Pincode
            shipping=ShippingCharges.objects.filter(pincode=str(pin))
            if shipping:
                for m in shipping:
                    amount=m.amount
                shopping_session = ShoppingSession.objects.filter(user_id=user_id)
                for i in shopping_session:
                    test1 = CartItem.objects.filter(ShoppingSession_id=i.id)
                    # test1s =LeaderBoardOne.objects.filter(user_id=user_id)
                    # for l in test1s:
                    #     points=l.points
                    #     five_percent=int(l.points)*5/100
                    #     if int(five_percent)>50:
                    #         five_percent=50



                    for k in test1:
                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:
                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                            for b in dis:
                                dis_percent=dis_percent+int(b.Discount_Percentage)
                            after_discount=float(k.Product_ID.Product_Selling_Price)*dis_percent/100
                            f_price=float(k.Product_ID.Product_Selling_Price)-after_discount
                            dis_percent=0
                            total_Mrp=int(total_Mrp)+int(f_price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                        else:
                            total_Mrp=int(total_Mrp)+int(k.Product_ID.Product_Selling_Price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                Arr.append({
                'amount':0,
                'code':'',
                'discount':0,
                'total_Mrp':total_Mrp,
                'shipping_charge':amount,
                'total_amount':int(total_Mrp)+int(amount),
                'points':points,
                'five_percent':int(five_percent)
                })
                return Response(Arr)
            else:
                shopping_session = ShoppingSession.objects.filter(user_id=user_id)
                for i in shopping_session:
                    test1 = CartItem.objects.filter(ShoppingSession_id=i.id)

                    for k in test1:
                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:
                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                            for b in dis:
                                dis_percent=dis_percent+int(b.Discount_Percentage)
                            after_discount=float(k.Product_ID.Product_Selling_Price)*dis_percent/100
                            f_price=float(k.Product_ID.Product_Selling_Price)-after_discount
                            dis_percent=0
                            total_Mrp=int(total_Mrp)+int(f_price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                        else:
                            total_Mrp=int(total_Mrp)+int(k.Product_ID.Product_Selling_Price)*int(k.quantity)
                            five_percent=int(total_Mrp)*5/100
                            if int(five_percent)>50:
                                five_percent=50
                Arr.append({
                'total_Mrp':total_Mrp,
                'shipping_charge':0,
                'total_amount':total_Mrp,
                'points':points,
                'five_percent':int(five_percent)

                })
                return Response(Arr)






class AttributesApi(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        Arr=[]
        if id:
            test1 =Master_Attributes.objects.filter(id=id).values()
            for i in test1:
                res={}
                res['id']=i['id']
                res['name']=i['name']
                res['option']=[]
                opt=Master_AttributeOptions.objects.filter(attributes_id=i['id'])
                for k in opt:
                    res['option'].append(
                    k.option
                    )
                Arr.append(res)
            return Response(Arr)
        else:
            test1 =Master_Attributes.objects.all().values()
            for i in test1:
                res={}
                res['id']=i['id']
                res['name']=i['name']
                res['option']=[]
                opt=Master_AttributeOptions.objects.filter(attributes_id=i['id'])
                for k in opt:
                    res['option'].append(

                    k.option
                    )
                Arr.append(res)
            return Response(Arr)

    def post(self,request):
        data = request.data
        name = data.get('name')
        option=data.get('option')
        attr_id = Master_Attributes.objects.create(name=name.title())
        print(option,'opt')

        for k in option:

            attribute_options = Master_AttributeOptions.objects.create(attributes_id=attr_id.id,option=k.title())
        return Response({'result':'data added successfully'})


    def put(self,request,pk):
        data = request.data
        name = data.get('name')
        option=data.get('option')
        attr_id = Master_Attributes.objects.filter(id=pk).update(name=name)
        print(option,'opt')

        for k in option:
            attribute_options = Master_AttributeOptions.objects.filter(attributes_id=pk).delete()

        for a in option:

            attribute_options = Master_AttributeOptions.objects.create(attributes_id=pk,option=a)
        # return Response({'result':'data added successfully'})



        return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = Master_Attributes.objects.filter(id=pk).delete()
        return Response({'result':'Deleted'})


# class AttributeOptionsApi(APIView):
#     def get(self,request):
#         def get(self,request):
#             test = request.query_params.get('id')
#             if Attributes.objects.filter(id=test).exists():
#                 test1 =Attributes.objects.filter(id=test).values()
#                 return Response({'result':{'All attribute names':test1}})
#             else:
#                 return Response({'error':'id doesnt exists'})

#     def post(self,request):
#         data = request.data

#         name = data.get('name')
#         attributes=data.get('attributes')

#         selected_page_no = 1
#         page_number = request.GET.get('page')
#         if page_number:
#             selected_page_no = int(page_number)

#         if AttributeOptions.objects.filter(name=name).exists():
#             return Response({'result':'Exists'})
#         else:
#             AttributeOptions.objects.create(name=name,attributes_id=attributes)

#             posts = AttributeOptions.objects.all().values()
#             paginator = Paginator(posts,10)
#             try:
#                 page_obj = paginator.get_page(selected_page_no)
#             except PageNotAnInteger:
#                 page_obj = paginator.page(1)
#             except EmptyPage:
#                 page_obj = paginator.page(paginator.num_pages)
#             return Response({'result':'Created', 'data':list(page_obj)})


#     def put(self,request,pk):
#         data = request.data

#         name = data.get('name')
#         attributes=data.get('attributes')


#         if AttributeOptions.objects.filter(name=name).exists():
#             return Response({'result':'Exists'})
#         else:
#             AttributeOptions.objects.filter(id=pk).update(name=name,attributes_id=attributes)
#             return Response({'result':'Updated'})

#     def delete(self,request,pk):
#         all_values = AttributeOptions.objects.filter(id=pk).delete()
#         return Response(all_values)



class ProductsAttributeApi(APIView):
    def get(self,request):
        user_id=request.query_params.get('user_id')
        product_id=request.query_params.get('product_id')
        if user_id and product_id:
            test1 =ProductAttributes.objects.filter(user_id=user_id,Product_ID_id=product_id).values()
            return Response(test1)
        else:
            return Response({
                'error':{'message':'user_id product_id required!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        data = request.data
        user_id =data.get('user_id')
        attributes =data.get('attributes_id')
        Product_ID=data.get('Product_ID_id')
        selectedoptions=data.get('selectedoptions')
        Arr=[]
        for i in attributes:
            data=ProductAttributes.objects.create(user_id=user_id,attributes_id=i,Product_ID_id=Product_ID)
            Arr.append(data.id)
        count1=0
        for l in selectedoptions:
            val=str(Arr[count1])
            data=ProductAttributes.objects.filter(id=int(val)).update(selectedoptions=l)
            count1=count1+1

        return Response({'result':'Created'})


    def put(self,request,pk):
        data = request.data

        attributes =data.get('attributes_id')
        Product_ID=data.get('Product_ID_id')
        selectedoptions=data.get('selectedoptions')



        if ProductAttributes.objects.filter(selectedoptions=selectedoptions).exists():
            return Response({'result':'selectedpoints already exists'})
        else:
            ProductAttributes.objects.filter(id=pk).update(attributes_id=attributes,Product_ID_id=Product_ID,
                                                selectedoptions=selectedoptions)

            return Response({'result':'Updated'})

    def delete(self,request,pk):
        all_values = ProductAttributes.objects.filter(id=pk).delete()
        return Response(all_values)






@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    # amount=request.data['amount']
    user_id=request.data['user_id']
    # quantity=request.data['quantity']
    # product_id=request.data['product_id']

    # promocode=request.data['code']
    final_price=request.data['final_price']
    product_details=request.data['product_details']


    for l in range(len(final_price)):
            e=(list(final_price[l].values()))
            amount=e[5]


    # return Response('hello')


    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    # client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    payment = client.order.create({"amount": int(amount) * 100,
                                   "currency": "INR",
                                   "payment_capture": "1"})


    address=User_Address.objects.filter(user_id=user_id,delfault_address=True)
    for i in address:
        pin=i.Pincode
        Address=i.Address
        City=i.City
        State=i.State
        Country=i.Country
        street=i.street
    shippingcharges= ShippingCharges.objects.filter(pincode=pin)
    if shippingcharges:
        for j in shippingcharges:
            ids=j.id



        value=0
        order_details=OrderDetails.objects.create(user_id=user_id,total=amount,
                                                shippingcharges_id=ids,delivery_status='Pending',
                                                Address=Address,
                                                City=City,
                                                State=State,
                                                Country=Country,
                                                Pincode=pin,
                                                street=street,)

        for l in range(len(product_details)):
                e=(list(product_details[l].values()))
                size=e[0]
                color=e[1]
                quantity=e[4]
                product_id=e[5]

                pro=Product.objects.get(id=product_id)
                value=int(pro.count_sold)
                prod=Product.objects.filter(id=product_id).update(count_sold=value+int(quantity))
                order_item=OrderItems.objects.create(OrderDetails_id=order_details.id,quantity=quantity,Product_ID_id=product_id,size=size,color=color)
        order= PaymentDetails.objects.create(orderdetails_id=order_details.id,
                                        amount=amount,
                                        provider='Razorpay',
                                        payment_id=payment['id'])


        serializer = PaymentDetailsSerializer(order)

        """order response will be
        {'id': 17,
        'order_date': '23 January 2021 03:28 PM',
        'order_product': '*product name from frontend*',
        'order_amount': '*product amount from frontend*',
        'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
        'isPaid': False}"""

        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data)
    else:
        return Response('No shipping available for this pincode')

@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    # res = json.loads(request.data["response"])
    # amount=request.data['amount']
    user_id=request.data['user_id']

    ord_id=request.data['razorpay_order_id']
    raz_pay_id=request.data['razorpay_payment_id']
    raz_signature=request.data['razorpay_signature']

    promocode=request.data['code']
    referral_coin=request.data['referral_coin']

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e',
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ',
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    """

    # ord_id = ""
    # raz_pay_id = ""
    # raz_signature = ""

    # res.keys() will give us list of keys in res
    # for key in res.keys():
    #     if key == 'razorpay_order_id':
    #         ord_id = res[key]
    #     elif key == 'razorpay_payment_id':
    #         raz_pay_id = res[key]
    #     elif key == 'razorpay_signature':
    #         raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = PaymentDetails.objects.get(payment_id=ord_id)

    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }
    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    # client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.status = True
    order.save()

    two_percent=int(float(order.amount))*2/100
    if referral_coin:
        points=LeaderBoardOne.objects.filter(user_id=user_id)
        if points:
            for j in points:
                pointss=j.points
            updated_points=LeaderBoardOne.objects.filter(user_id=user_id).update(points=int(pointss)-int(referral_coin))


    if promocode:
        marketer=PromoCode.objects.get(Code=promocode)
        if marketer.marketer_id:

            sales=Marketer_sales.objects.create(marketer_id=marketer.marketer_id,code=promocode,orders_id=order.id,sale_amt=order.amount)
            user_promo=PromoCode.objects.filter(Code=promocode).update(status='Inactive')
        quant=0
        promo=User_PromoDetails.objects.filter(Q(user_id=user_id)&Q(code=promocode))
        if promo:
            for k in promo:
                quant=k.quantity
            user_promo=User_PromoDetails.objects.filter(Q(user_id=user_id)&Q(code=promocode)).update(quantity=int(quant)-1)

    userss=User_Address.objects.filter(user_id=user_id,delfault_address=True)
    for l in userss:
        pin=l.Pincode
    user=User.objects.filter(id=user_id)
    for k in user:
        usernamess=k.username
        fullname=k.first_name.title()

    shippingcharges=ShippingCharges.objects.filter(pincode=pin)
    for j in shippingcharges:
        amt=j.amount
    order = User_Payment.objects.create(Payment_Name=usernamess,
                                        Payment_Type='Razorpay',
                                        Delivery_Charges=amt,
                                        Amount=order.amount,
                                        user_id=user_id)
    shoppingsession=ShoppingSession.objects.filter(user_id=user_id)
    for k in shoppingsession:
        id=k.id


    delete_cart=CartItem.objects.filter(ShoppingSession_id=id).delete()
    coin=0

    orderss=OrderDetails.objects.filter(user_id=user_id).count()
    if orderss==1:
        leader=LeaderBoardOne.objects.filter(user_id=user_id)
        if leader:
            for k in leader:
                used_code=k.used_code
            data=Custom_User.objects.get(user_to_user_refcode=used_code)
            leaders=LeaderBoardOne.objects.filter(user_id=data.user_id)
            if leaders:
                for j in leaders:
                    coin=int(j.points)
                leaders=LeaderBoardOne.objects.filter(user_id=data.user_id).update(points=int(coin)+100)
            else:
                leaders=LeaderBoardOne.objects.create(user_id=data.user_id,points=100)


    coins=0
    points=LeaderBoardOne.objects.filter(user_id=user_id)
    if points:
        for l in points:
            coins=int(l.points)
        points_update=LeaderBoardOne.objects.filter(user_id=user_id).update(points=int(coins)+int(two_percent))
    else:
        leaders=LeaderBoardOne.objects.create(user_id=user_id,points=int(two_percent))


    if '@' in usernamess:

        message = inspect.cleandoc('''Hi %s,\nThank you for purchasing with us.\nWelcome to Kri8ev,
                              \nWith Warm Regards,\nTeam Kri8ev,
                               ''' % (fullname))
        send_mail(
            'Kri8ev Registration Confirmation', message
            ,
            'info.aceventures18@gmail.com',
            [usernamess],

        )
    else:
        pass



    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)
































#######################################################END##############################################################





















        # posts = Product.objects.all() # fetching all post objects from database
        # p = Paginator(posts, 10) # creating a paginator object
        # # getting the desired page number from url
        # page_number = request.GET.get('page')
        # try:
        #     page_obj = p.get_page(page_number) # returns the desired page object
        # except PageNotAnInteger:
        #     # if page_number is not an integer then assign the first page
        #     page_obj = p.page(1)
        # except EmptyPage:
        #     # if page is empty then return last page
        #     page_obj = p.page(p.num_pages)
        # # context = {'page_obj': page_obj}
        # # sending the page object to index.html
        # return Response({[request,  post]})


#
#
#
#
# class EmailVerification(APIView):
#
#     @csrf_exempt
#     def post(self, request):
#         data = request.data
#         email=data.get('email')
#         print(data,'lll')
#         # userdata=CustomUser.objects.filter(email=email).values()
#         # if userdata:
#             # return JsonResponse({"msg": "User is already exist with this email"}, safe=False)
#
#         # else:
#         if data:
#             otp = random.randint(1000, 9999)
#             message = inspect.cleandoc('''Thank you for registering,
#                                    Please enter This OTP %s verify your email id,
#                                    ''' % (otp))
#             send_mail(
#                 'Greetings from Spotlyt', message
#                 ,
#                 'Spotlyt',
#                 [email],
#
#             )
#             data_dict = {}
#             data_dict["Otp"] = otp
#             return JsonResponse(data_dict, safe=False)
#         else:
#             return JsonResponse({"msg": "Email-id required"}, safe=False)
#
# #############################SignupApi###########################################

class SignupApi(APIView):
    serializer_class    = CustUserSerializer
    queryset            = CustomUser.objects.all()
    @csrf_exempt
    def post(self, request):

        data = request.data
        print(data)
        response = {}
        Full_Name        =data.get('Full_Name')
        username        =data.get('username')
        password                = data.get('password')
        confirm_password                = data.get('confirm_password')


        Mobile_Number        = data.get('Mobile_Number')
        Email_ID                   = data.get('Email_ID')
        # role_id                = data.get('role_id')
        Date_Of_Birth        =data.get('Date_Of_Birth')
        Terms        =data.get('Terms')
        referral_code=data.get('referral_code')
        ref_code=data.get('ref_code')




        if '@' in username:
            if password == confirm_password:
                if User.objects.filter(Q(username=username) | Q(email=username)|Q(last_name=Mobile_Number)).exists():
                    header_response = {}
                    response['error'] = {'error': {
                        'detail': 'Username or email already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)

                else:

                    user_create = User.objects.create_user(username=username,email=username,password=password,first_name=Full_Name,last_name=Mobile_Number)
                    ref=Full_Name.upper()+str(user_create.id)
                    custom_user = Custom_User.objects.create(user_id=user_create.id,username=username,Full_Name=Full_Name,Mobile_Number=Mobile_Number,Email_ID=username,Date_Of_Birth=Date_Of_Birth,Terms=Terms,referral_code=referral_code,user_to_user_refcode=ref)
                    if ref_code:
                        code=Custom_User.objects.filter(user_to_user_refcode=ref_code)
                        if code:
                            leader=LeaderBoardOne.objects.create(user_id=user_create.id,points=0,used_code=ref_code)
                    response['result'] = 'Register Successfully'

                    auth_token = jwt.encode(
                        {'user_id': user_create.id, 'username': user_create.username, 'email': user_create.email, 'mobile_number': custom_user.Mobile_Number }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                    authorization = 'Bearer'+' '+auth_token
                    user = auth.authenticate(username=username, password=password)
                    custom=''
                    custom_user = User.objects.get(id=user.id)

                    custom = Custom_User.objects.get(user_id=custom_user.id)
                    auth_token = jwt.encode(
                        {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    serializer = CustUserSerializer(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    response_result['result'] = {
                        'detail': 'Login successfull',
                        'token': authorization,
                        'user_id':user.id,
                        'username':user.username,
                        'id':custom.id,
                        'fullname':user.first_name,
                        'email':user.email,
                        'mobile_number':custom.Mobile_Number,
                        'status': status.HTTP_200_OK}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK

                    message = inspect.cleandoc('''Hi %s,\nThank you for registering with us.\nWelcome to Kri8ev,
                                          \nWith Warm Regards,\nTeam Kri8ev,
                                           ''' % (user.first_name.title()))
                    send_mail(
                        'Kri8ev Registration Confirmation', message
                        ,
                        'info.aceventures18@gmail.com',
                        [username],

                    )


                    return Response(response_result, headers=response,status=status.HTTP_200_OK)


            else:
                return Response({'result': 'password not matched'})
                # response_error = {}
                # response_error['error'] = {'details':'password not matched'}
                # return Response(response_error, status=status.HTTP_400_BAD_REQUEST)

        else:
            if password == confirm_password:
                if User.objects.filter(Q(username=username) | Q(email=Email_ID)|Q(last_name=Mobile_Number)).exists():
                    header_response = {}
                    response['error'] = {'error': {
                        'detail': 'Username or email already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)
                    # response=" Username or email already exist!"
                    # return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    # return Response({'result': 'username or email taken'})

                else:

                    user_create = User.objects.create_user(username=username,email=Email_ID,password=password,first_name=Full_Name,last_name=Mobile_Number)
                    ref=Full_Name.upper()+str(user_create.id)
                    custom_user = Custom_User.objects.create(user_id=user_create.id,username=username,Full_Name=Full_Name,Mobile_Number=username,Email_ID=Email_ID,Date_Of_Birth=Date_Of_Birth,Terms=Terms,user_to_user_refcode=ref)
                    code=Custom_User.objects.filter(user_to_user_refcode=ref_code)
                    if code:
                        leader=LeaderBoardOne.objects.create(user_id=user_create.id,points=0,used_code=ref_code)

                    response['result'] = 'Register Successfully'

                    auth_token = jwt.encode(
                        {'user_id': user_create.id, 'username': user_create.username, 'email': user_create.email, 'mobile_number': custom_user.Mobile_Number }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                    authorization = 'Bearer'+' '+auth_token

                    # response_result = {}
                    # response_result['Result'] = {
                    #     'result': {'data': 'Register successful'}}
                    # response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    # response['status'] = status.HTTP_200_OK


                    user = auth.authenticate(username=username, password=password)
                    custom=''
                    # if user:
                    custom_user = User.objects.get(id=user.id)

                    custom = Custom_User.objects.get(user_id=custom_user.id)
                    #     print(custom_user)
                    auth_token = jwt.encode(
                        {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    serializer = CustUserSerializer(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    response_result['result'] = {
                        'detail': 'Login successfull',
                        'token': authorization,
                        'user_id':user.id,
                        'username':user.username,
                        'id':custom.id,
                        'fullname':user.first_name,
                        'email':user.email,
                        'mobile_number':custom.Mobile_Number,
                        'status': status.HTTP_200_OK}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK

                    return Response(response_result, headers=response,status=status.HTTP_200_OK)
                    # else:
                        # return Response({'result': 'Something went wrong'})

            else:
                return Response({'result': 'password not matched'})


class WishlistApi(APIView):
    def get(self,request):

        user_id =self.request.query_params.get('user_id')
        Arr=[]
        dis_percent=0
        today = datetime.date.today()
        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
        if discount:
            wishlist_data = Wishlist.objects.filter(user_id=user_id)
            for i in wishlist_data:

                dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                for b in dis:
                    dis_percent=dis_percent+int(b.Discount_Percentage)
                after_discount=float(i.product.Product_Selling_Price)*dis_percent/100
                f_price=float(i.product.Product_Selling_Price)-after_discount
                dis_percent=0

        # wishlist_data = Wishlist.objects.filter(user_id=user_id)
        # for i in wishlist_data:
                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'product_id':i.product.id,
                'product_name':i.product.Product_Name,
                'product_image':str(i.product.Product_Image),
                'status':i.status,
                'product_description':i.product.Product_Description,
                'product_selling_price':f_price,
                'product_listed_price':i.product.Product_Listed_Price


                })

            return Response(Arr)
        else:
            wishlist_data = Wishlist.objects.filter(user_id=user_id)
            for i in wishlist_data:


                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'product_id':i.product.id,
                'product_name':i.product.Product_Name,
                'product_image':str(i.product.Product_Image),
                'status':i.status,
                'product_description':i.product.Product_Description,
                'product_selling_price':i.product.Product_Selling_Price,
                'product_listed_price':i.product.Product_Listed_Price


                })

            return Response(Arr)



    def post(self,request):
        data = request.data

        product_id = data.get('product_id')
        user_id = data.get('user_id')
        status = data.get('wishlist_status')

        val= Wishlist.objects.filter(product_id=product_id,user_id=user_id)
        if val:
            return Response('this product is already added in your wishlist')
        else:
            data=Wishlist.objects.create(product_id=product_id,
                                    user_id=user_id,
                                    status=status,

                            )
            # pro_update=Product.objects.filter(id=product_id).update(wishlistss=True)



            return Response({'result':'wish list added successfully'})


    def delete(self, request):
        user_id =self.request.query_params.get('user_id')
        id =self.request.query_params.get('id')


        all_values = Wishlist.objects.filter(Q(user_id=user_id)&Q(id=id))
        for i in all_values:
            pro_id=i.product_id
            # pro=Product.objects.filter(id=pro_id).update(wishlistss=False)
        if len(all_values) > 0:
            all_values.delete()
            return Response("Wishlist  Deleted Sucessfully")
        else:
            return Response("Id Required.")

class Delete_wishlist_based_on_product_idAPIView(APIView):

        def delete(self, request):
            user_id =self.request.query_params.get('user_id')
            id =self.request.query_params.get('id')


            all_values = Wishlist.objects.filter(Q(user_id=user_id)&Q(product_id=id)).delete()

            return Response("Wishlist  Deleted Sucessfully")

#################################Deal of the day###################################

class Deal_of_the_dayAPIView(APIView):
    def get(self,request):


        Arr=[]
        dis_percent=0
        today = datetime.date.today()
        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
        if discount:
            deal_data = Deal_of_the_day.objects.all()
            for i in deal_data:
                dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                for b in dis:
                    dis_percent=dis_percent+int(b.Discount_Percentage)
                after_discount=float(i.product.Product_Selling_Price)*dis_percent/100
                f_price=float(i.product.Product_Selling_Price)-after_discount
                dis_percent=0
                Arr.append({
                'id':i.id,
                'product_id':i.product.id,
                'product_name':i.product.Product_Name,
                'product_image':str(i.product.Product_Image),
                'product_details':i.product.Product_Details,
                'category_name':i.product.Product_Category.Product_Category_Name,

                'product_selling_price':f_price

                })

            return Response(Arr)
        else:
            deal_data = Deal_of_the_day.objects.all()
            for i in deal_data:
                Arr.append({
                'id':i.id,
                'product_id':i.product.id,
                'product_name':i.product.Product_Name,
                'product_image':str(i.product.Product_Image),
                'category_name':i.product.Product_Category.Product_Category_Name,
                'product_details':i.product.Product_Details,
                'product_selling_price':i.product.Product_Selling_Price

                })

            return Response(Arr)

    def post(self,request):
        data = request.data

        product_category_id = data.get('product_category_id')
        product_id = data.get('product_id')

        data=Deal_of_the_day.objects.create(product_category_id=product_category_id,product_id=product_id)

        return Response({'result':'Deal_of_the_day added successfully'})

    #
    # def put(self, request):
    #     data = request.data
    #     id = data.get('id')
    #
    #     if id:
    #         data = Deal_of_the_day.objects.filter(id=id).update(product_id=data.get('product_id'),)
    #
    #         if data:
    #             return JsonResponse({'message': 'Deal_of_the_day details Updated Sucessfully.'})
    #         else:
    #             return JsonResponse({'message': 'Invalid Deal_of_the_day'})
    #
    #     else:
    #         return JsonResponse({'message': 'Id Required for updating.'})
    #
    def delete(self, request,pk):

        all_values = Deal_of_the_day.objects.filter(id=pk).delete()

        return Response("Deal_of_the_day  Deleted Sucessfully")



# # ?-------------------------  JWT   LOG-IN-------------------------------------------------------------------------------

class LoginView(GenericAPIView):
    serializer_class = CustUserSerializer

    def post(self, request):
        response = {}
        data = request.data
        username = data.get('username')
        password = data.get('password')
        # otp = data.get('otp')
        c_user_check = User.objects.filter(Q(username= username)|Q(last_name=username))
        user_check = User.objects.filter(username= username)

        #
        if user_check:
            # if '@' in username:
            user = auth.authenticate(username=username, password=password)
            # new_user = auth.authenticate(last_name=username, password=password)
            custom=''
            if user:

                custom_user = User.objects.get(id=user.id)
                custom_users = Custom_User.objects.filter(user_id=user.id)
                custom_team = kri8evTeam.objects.filter(name=custom_user.username)
                if custom_users:
                    custom = Custom_User.objects.get(user_id=user.id)
                    print(custom_user)
                    auth_token = jwt.encode(
                        {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    serializer = CustUserSerializer(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    role=UserRoleRef.objects.filter(id=custom.role_id)
                    for k in role:
                        name=k.user_role_name
                    response_result['result'] = {
                        'detail': 'Login successfull',
                        'token':authorization,
                        'user_id':user.id,
                        'username':user.username,
                        'fullname':user.first_name,
                        'id':custom.id,
                        'email':user.email,
                        # 'role':custom.role_id,
                        # 'role_name':name,
                        'mobile_number':custom.Mobile_Number,
                        'status': status.HTTP_200_OK}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK
                elif custom_team:
                    kri8ev = kri8evTeam.objects.get(name=custom_user.username)
                    auth_token = jwt.encode(
                        {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    serializer = CustUserSerializer(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    role=UserRoleRef.objects.filter(id=kri8ev.role_id)
                    for k in role:
                        name=k.user_role_name
                    response_result['result'] = {
                        'detail': 'Login successfull',
                        'token':authorization,
                        'user_id':user.id,
                        # 'username':user.username,
                        'username':kri8ev.name,
                        'email':user.email,
                        'role':kri8ev.role_id,
                        'role_name':kri8ev.role.user_role_name,
                        # 'mobile_number':custom_user.mobile_number,
                        'status': status.HTTP_200_OK}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK
                else:
                    auth_token = jwt.encode(
                        {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    serializer = CustUserSerializer(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    response_result['result'] = {
                        'detail': 'Login successfull',
                        'token':authorization,
                        'user_id':user.id,
                        'username':user.username,
                        # 'fullname':custom.fullname,
                        'fullname':user.first_name,
                        'email':user.email,
                        'role_name':'Admin',
                        # 'mobile_number':custom_user.mobile_number,
                        'status': status.HTTP_200_OK}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK


            else:
                header_response = {}
                response['error'] = {'error': {
                    'detail': 'Invalid credentials', 'status': status.HTTP_401_UNAUTHORIZED}}

                return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)
            return Response(response_result, headers=response,status= status.HTTP_200_OK)

        elif c_user_check:
            print('mobile_number',username)
            new_user = User.objects.get(last_name=username)
            if new_user.check_password(password):
            # new_user = auth.authenticate(last_name=username, password=password)
            # print(new_user,'new_user')

            # if new_user:
                custom_users = Custom_User.objects.filter(user_id=new_user.id)
                if custom_users:
                    custom = Custom_User.objects.get(user_id=new_user.id)
                    auth_token = jwt.encode(
                        {'user_id': new_user.id, 'username': new_user.username, 'email': new_user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    serializer = CustUserSerializer(new_user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}

                    response_result['result'] = {
                        'detail': 'Login successfull',
                        'token':authorization,
                        'user_id':new_user.id,
                        'username':new_user.username,
                        'fullname':new_user.first_name,
                        'id':custom.id,
                        'email':new_user.email,
                        # 'role':custom.role_id,
                        # 'role_name':name,
                        'mobile_number':custom.Mobile_Number,
                        'status': status.HTTP_200_OK}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK
            else:
                header_response = {}
                response['error'] = {'error': {
                    'detail': 'Invalid credentials', 'status': status.HTTP_401_UNAUTHORIZED}}

                return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)
            return Response(response_result, headers=response,status= status.HTTP_200_OK)
        else:
            header_response = {}
            response['error'] = {'error': {
                'detail': 'Invalid username', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)


class SocialMdGmailSignupApi(APIView):

    def post(self, request):
        data = request.data

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        response = {}

        user_check = User.objects.filter(Q(username= email) & Q(email= email))

        if user_check:

            user = User.objects.get(Q(username= email) & Q(email= email))
            c_user = Custom_User.objects.get(user_id=user.id)



            # token, created = Token.objects.get_or_create(user=User.objects.get(id= user.id))
            auth_token = jwt.encode(
                {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

            serializer = CustUserSerializer(user)
            authorization = 'Bearer'+' '+auth_token


            response_result = {}
            response_result['result'] = {
                'detail': 'Login successfull',
                'token': authorization,
                'user_id': user.id,
                'id':c_user.id,
                'email': user.email,
                'username':user.username,
                'fullname' : user.first_name,
                'mobile_number':c_user.Mobile_Number,
                'status': status.HTTP_200_OK}
            response['Authorization'] = authorization,
            # response['Token-Type']      =   'Bearer'
            response['status'] = status.HTTP_200_OK

            return Response(response_result, headers=response,status=status.HTTP_200_OK)


        else:

            user_create = User.objects.create_user(username= email, email= email,first_name=name)
            ref=name.upper()+str(user_create.id)

            cust_user_create = Custom_User.objects.create(user_id=user_create.id,username= email, Email_ID= email,Full_Name=name,user_to_user_refcode=ref)

            # token, created = Token.objects.get_or_create(user=User.objects.get(id=user_create.id))
            auth_token = jwt.encode(
                {'user_id': user_create.id, 'username': user_create.username, 'email': user_create.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

            serializer = CustUserSerializer(user_create)
            authorization = 'Bearer'+' '+auth_token


            response_result = {}
            response_result['result'] = {
                'detail': 'Login successfull',
                'token': authorization,
                'user_id': user_create.pk,
                'id':cust_user_create.id,
                'email': user_create.email,
                'username':user_create.username,
                'fullname' : user_create.first_name,
                'mobile_number':cust_user_create.Mobile_Number,
                'status': status.HTTP_200_OK}
            response['Authorization'] = authorization,
            # response['Token-Type']      =   'Bearer'
            response['status'] = status.HTTP_200_OK

            return Response(response_result, headers=response,status=status.HTTP_200_OK)





#############################User Role###########################################

class UserRoleRefAPIView(APIView):
    def get(self, request):
        # data = request.data
        # user_id = data.get('user_id')
        id =self.request.query_params.get('id')

        if id:
            userRole_data = UserRoleRef.objects.filter(id=id).values()
            return Response(userRole_data)
        else:
            userRole_data = UserRoleRef.objects.all().values()
            return Response(userRole_data)


    def post(self, request):
        data = request.data

        user_role_name = data.get('user_role_name')
        salary= data.get('salary')
        bonus= data.get('bonus')
        incentives= data.get('incentives')





        userRole_create = UserRoleRef.objects.create(user_role_name=user_role_name.title(),
                                                        salary=salary,bonus=bonus,incentives=incentives)
        return Response("Data Added Sucessfully")


    def put(self, request,pk):
        data = request.data

        data = UserRoleRef.objects.filter(id=pk).update(user_role_name=data.get('user_role_name'),
                                                        salary= data.get('salary'),
                                                        bonus= data.get('bonus'),
                                                        incentives= data.get('incentives'),)


        if data:
            return JsonResponse({'message': 'UserRoleRef Updated Sucessfully.'})
        else:
            response=' Invalid UserRoleRef'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,pk):
        # id =self.request.query_params.get('id')


        userRole_data =UserRoleRef.objects.filter(id= pk)

        if len(userRole_data) > 0:
            userRole_data.delete()
            return Response("UserRoleRef  Deleted Sucessfully")
        else:
            return Response("Id Required.")

####################################Kri8eve Team###################################

class kri8evTeamApiView(APIView):
    serializer_class    = CustUserSerializer
    queryset            = CustomUser.objects.all()
    @csrf_exempt
    def get(self, request):
        # CheckAuth(request)

        id =self.request.query_params.get('id')

        Arr=[]
        if id:
            spotlytTeam_data = kri8evTeam.objects.filter(id=id)
            for i in spotlytTeam_data:

                Arr.append({
                'id':i.id,
                'name':i.name,
                'email':i.email,
                'mobile_number':i.mobile_number,
                'role':i.role.user_role_name,
                'role_id':i.role.id
                })

            return Response(Arr)
        else:
            spotlytTeam_data = kri8evTeam.objects.all()
            for i in spotlytTeam_data:

                Arr.append({
                'id':i.id,
                'name':i.name,
                'email':i.email,
                'mobile_number':i.mobile_number,
                'role':i.role.user_role_name,
                'role_id':i.role.id
                })

            return Response(Arr)


    def post(self, request):

        data = request.data
        print(data)
        response = {}
        password                = data.get('password')
        mobile_number        = data.get('mobile_number')
        email                   = data.get('email')
        role                = data.get('role_id')
        name        =data.get('name')

        user_id=data.get('user_id')
        role_name=''



        # team=kri8evTeam.objects.all()
        # role=UserRoleRef.objects.filter(id=role)
        # for i in role:
        #     r_name=i.user_role_name
        # codes=name[:3]+'001'+r_name[-2:-1]

        if data:
            team=kri8evTeam.objects.filter(user_id=user_id)
            for i in team:
                role_name=i.role.user_role_name
            if role_name=='Leader':
                if User.objects.filter(Q(username=name) | Q(email=email)).exists():
                    header_response = {}
                    response['error'] = {'error': {
                        'detail': 'Username or email already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_create = User.objects.create_user(username=name,email=email,password=password,first_name=name)
                    custom_user = kri8evTeam.objects.create(user_id=user_create.id,role_id=role,name=name,email=email,mobile_number=mobile_number,created_by=user_id)

                    role=UserRoleRef.objects.filter(id=role)
                    for k in role:
                        if k.user_role_name=='Marketer':

                            val=str(custom_user.name)[:2].upper()+'0'+str(custom_user.id)+"M"
                            team=Team_Code.objects.create(team_id=custom_user.id,ref_code=val)

                        if k.user_role_name=='Leader':

                            val=str(custom_user.name)[:2].upper()+'0'+str(custom_user.id)+"L"
                            team=Team_Code.objects.create(team_id=custom_user.id,ref_code=val)

                    response['result'] = 'data Added Successfully'

                    auth_token = jwt.encode(
                        {'user_id': user_create.id, 'username': user_create.username, 'email': user_create.email, 'mobile_number': custom_user.mobile_number }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                    authorization = 'Bearer'+' '+auth_token

                    response_result = {}
                    response_result['Result'] = {
                        'result': {'data': 'data submit successful'}}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK
                    return Response(response_result['Result'], headers=response,status=status.HTTP_200_OK)
            else:
                if User.objects.filter(Q(username=name) | Q(email=email)).exists():
                    header_response = {}
                    response['error'] = {'error': {
                        'detail': 'Username or email already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

                    return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_create = User.objects.create_user(username=name,email=email,password=password,first_name=name)
                    custom_user = kri8evTeam.objects.create(user_id=user_create.id,role_id=role,name=name,email=email,mobile_number=mobile_number)

                    role=UserRoleRef.objects.filter(id=role)
                    for k in role:
                        if k.user_role_name=='Marketer':

                            val=str(custom_user.name)[:2].upper()+'0'+str(custom_user.id)+"M"
                            team=Team_Code.objects.create(team_id=custom_user.id,ref_code=val)

                        if k.user_role_name=='Leader':

                            val=str(custom_user.name)[:2].upper()+'0'+str(custom_user.id)+"L"
                            team=Team_Code.objects.create(team_id=custom_user.id,ref_code=val)

                    response['result'] = 'data Added Successfully'

                    auth_token = jwt.encode(
                        {'user_id': user_create.id, 'username': user_create.username, 'email': user_create.email, 'mobile_number': custom_user.mobile_number }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                    authorization = 'Bearer'+' '+auth_token

                    response_result = {}
                    response_result['Result'] = {
                        'result': {'data': 'data submit successful'}}
                    response['Authorization'] = authorization
                    # response['Token-Type']      =   'Bearer'
                    response['status'] = status.HTTP_200_OK
                    return Response(response_result['Result'], headers=response,status=status.HTTP_200_OK)

        else:
            return Response({'result': 'Please fill all the OPTIONS'})

    def put(self, request,pk):
        data = request.data
        # id = data.get('id')

        # if id:
        data = kri8evTeam.objects.filter(id=pk).update(mobile_number        = data.get('mobile_number'),
                                                # mobile_number        = data.get('mobile_number'),
                                                # email                   = data.get('email')
                                                role                = data.get('role_id'),)
                                                # name        =data.get('name'),)
        if data:
            return JsonResponse({'message': 'kri8evTeam details Updated Sucessfully.'})
        else:
            return JsonResponse({'message': 'Invalid kri8evTeam'})

        # else:
        #     return JsonResponse({'message': 'Id Required for updating.'})



    def delete(self,request,pk):
        all_values = kri8evTeam.objects.get(id=pk)
        del_user=User.objects.filter(id=all_values.user_id).delete()
        return Response({'result':'Deleted'})


class Get_leader_roleapi(APIView):
    def get(self,request):
        id = self.request.query_params.get('id')
        Arr=[]
        if id:
            spotlytTeam_data = kri8evTeam.objects.filter(id=id)
            for i in spotlytTeam_data:

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'name':i.name,
                'email':i.email,
                'mobile_number':i.mobile_number,
                'role':i.role.user_role_name,
                'role_id':i.role_id
                })

            return Response(Arr)
        else:
            role=''
            roles=UserRoleRef.objects.filter(user_role_name='Leader')
            for i in roles:
                role=i.id
            spotlytTeam_data = kri8evTeam.objects.filter(Q(role__user_role_name='Marketer')|Q(role__user_role_name='Leader'))
            for i in spotlytTeam_data:

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'name':i.name,
                'email':i.email,
                'mobile_number':i.mobile_number,
                'role':i.role.user_role_name,
                'role_id':i.role_id
                })

            return Response(Arr)



    # def put(self,request,pk):
    #
    #     data = request.data
    #
    #     user_id=data.get('user_id')
    #     mobile_number=data.get('mobile_number')
    #     address    =data.get('address')
    #     city        =data.get('city')
    #     state            =data.get('state')
    #     pincode            =data.get('pincode')
    #     fullname        =data.get('fullname')
    #     date_of_birth=data.get('date_of_birth')
    #     role_id                = data.get('role_id')
    #
    #
    #
    #     data= Custom_User.objects.filter(user_id=user_id).update(Full_Name=fullname,Date_Of_Birth=date_of_birth,
    #                                         Mobile_Number=mobile_number,role_id=role_id)
    #     address_update = User_Address.objects.filter(user_id=user_id).update(Address=address,City=city,State=state,Pincode=pincode)
    #
    #
    #     return Response({'result':'Updated'})
    #
    # def delete(self,request,pk):
    #     all_values = kri8evTeam.objects.get(id=pk)
    #     del_user=User.objects.filter(id=all_values.user_id).delete()
    #     return Response({'result':'Deleted'})
    #


class Get_marketer_roleapi(APIView):
    def get(self,request):
        # id = self.request.query_params.get('id')
        user_id = self.request.query_params.get('user_id')
        Arr=[]
        if user_id:
            kri8evTeam_data = kri8evTeam.objects.filter(created_by=user_id)
            kri8evTeam_data_count = kri8evTeam.objects.filter(created_by=user_id).count()
            for i in kri8evTeam_data:

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'name':i.name,
                'email':i.email,
                'mobile_number':i.mobile_number,
                'role':i.role.user_role_name,
                'role_id':i.role_id
                })

            return Response({'data':Arr,'count':kri8evTeam_data_count})
        # if id:
        #     spotlytTeam_data = kri8evTeam.objects.filter(id=id)
        #     for i in spotlytTeam_data:
        #
        #         Arr.append({
        #         'id':i.id,
        #         'user_id':i.user_id,
        #         'username':i.user.username,
        #         'name':i.name,
        #         'email':i.email,
        #         'mobile_number':i.mobile_number,
        #         'role':i.role.user_role_name,
        #         'role_id':i.role_id
        #         })
        #
        #     return Response(Arr)
        else:
            role=''
            roles=UserRoleRef.objects.filter(user_role_name='Marketer')
            print(roles,';;;;1111')
            for i in roles:
                role=i.id
            print(role,'role_id')
            spotlytTeam_data = kri8evTeam.objects.filter(role__user_role_name='Marketer')
            print(spotlytTeam_data,'spotlytTeam_data')
            for i in spotlytTeam_data:

                Arr.append({
                'id':i.id,
                'user_id':i.user_id,
                'username':i.user.username,
                'name':i.name,
                'email':i.email,
                'mobile_number':i.mobile_number,
                'role':i.role.user_role_name,
                'role_id':i.role_id
                })

            return Response(Arr)


    #
    # def put(self,request,pk):
    #
    #     data = request.data
    #
    #     user_id=data.get('user_id')
    #     mobile_number=data.get('mobile_number')
    #     address    =data.get('address')
    #     city        =data.get('city')
    #     state            =data.get('state')
    #     pincode            =data.get('pincode')
    #     fullname        =data.get('fullname')
    #     date_of_birth=data.get('date_of_birth')
    #     role_id                = data.get('role_id')
    #
    #
    #
    #     data= Custom_User.objects.filter(user_id=user_id).update(Full_Name=fullname,Date_Of_Birth=date_of_birth,
    #                                         Mobile_Number=mobile_number,role_id=role_id)
    #     address_update = User_Address.objects.filter(user_id=user_id).update(Address=address,City=city,State=state,Pincode=pincode)
    #
    #
    #     return Response({'result':'Updated'})
    #
    # def delete(self,request,pk):
    #     all_values = kri8evTeam.objects.get(id=pk)
    #     del_user=User.objects.filter(id=all_values.user_id).delete()
    #     return Response({'result':'Deleted'})
class BrandAPIView(APIView):
    def get(self, request):

        id =self.request.query_params.get('id')


        if id:
            brand_data = Brand.objects.filter(id=id).values()
            if not brand_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response(brand_data)
        else:
            brand_data = Brand.objects.all().values()
            return Response(brand_data)
            # selected_page_no =1
            # page_number = request.query_params.get('page')
            # if page_number:
            #     selected_page_no = int(page_number)
            #     product_sub_data = Brand.objects.all().values()
            #     paginator = Paginator(product_sub_data, 10)
            #     try:
            #         paginator_data = paginator.page(selected_page_no)
            #     except PageNotAnInteger:
            #         paginator_data = paginator.page(1)
            #     except EmptyPage:
            #         print('except')
            #         paginator_data = paginator.page(paginator.num_pages)
            #     return JsonResponse({"Data": list(paginator_data)})
            # return Response(brand_data)



    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        brand_name = data.get('brand_name')
        description = data.get('description')


        brand_create = Brand.objects.create(brand_name=brand_name.title(),description=description)
        return Response("Data Added Sucessfully")



    def put(self, request,pk):
        data = request.data
        brand_name=data.get('brand_name')


        data = Brand.objects.filter(id=pk).update(brand_name=brand_name.title(),
                                                                description = data.get('description'),)



        if data:
            return JsonResponse({'message': 'Brand Updated Sucessfully.'})
        else:
            return JsonResponse({'message': ' Invalid Brand '})


    def delete(self, request,pk):

        brand_data =Brand.objects.filter(id= pk).delete()
        return Response("Brand Deleted Sucessfully")

class Get_category_wise_brandAPIView(APIView):
    def get(self, request):

        product_sub_category_id =self.request.query_params.get('product_sub_category_id')
        Arr=[]
        brand=Product.objects.filter(product_sub_category__id=product_sub_category_id)
        for i in brand:
            # print(i.brand_id,'')
            Arr.append({
            'brand_id':i.brand_id,
            'brand_name':i.brand.brand_name
            })
        output = []
        for x in Arr:
            if x not in output:
                output.append(x)
        return Response(output)


#
#
# class Get_brand_wise_prductAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         Arr=[]
#         res=[]
#         ids=[]
#         Arr=[]
#         opt=[]
#         image=''
#         Product_Category_Name=''
#         product_sub_category_name=''
#         ps_image=''
#         pricess=[0,0]
#         brand_id=[]
#         product_sub_category_id = data.get('product_sub_category_id')
#         brand_id = data.get('brand_id')
#         price=data.get('price')
#         color=data.get('color')
#         size=data.get('size')
#         newprice=[]
#         l1=[]
#         l2=[0]
#
#
#         if price:
#             if len(price)==1:
#                 l1=l2+price
#                 newprice=min(l1),max(l1)
#                 pricess=list(newprice)
#
#             else:
#                 newprice=min(price),max(price)
#                 print(newprice,'mul')
#                 pricess=list(newprice)
#
#         if brand_id or price or color or size:
#             qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id) & Q(brand_id__in=brand_id) | Q(Product_Selling_Price__range=pricess) ).values()
#             return Response(qs)
#


class Get_brand_wise_prductAPIView(APIView):
    def post(self, request):
        data = request.data
        Arr=[]
        res=[]
        ids=[]
        Arr=[]
        opt=[]
        image=''
        Product_Category_Name=''
        product_sub_category_name=''
        ps_image=''
        product_sub_category_id = data.get('product_sub_category_id')
        brand_id = data.get('brand_id')
        price=data.get('price')
        color=data.get('color')
        size=data.get('size')
        newprice=[]
        l1=[]
        l2=[0]

        dis_percent=0
        avg=0
        total_rating=0

        if price:
            if len(price)==1:
                l1=l2+price
                newprice=min(l1),max(l1)
                pricess=list(newprice)

            else:
                newprice=min(price),max(price)
                print(newprice,'mul')
                pricess=list(newprice)


        if brand_id:
            if price:
                if color:
                    if size:
                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:
                            att_op=AttributeOptions.objects.filter(Q(option__in=size)|Q(option__in=color))
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                                print(pro,'aaaa')
                                if pro:
                                    for i in pro:
                                        qs=Product.objects.filter(id=i.id).values()

                                        for i in qs:
                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0
                                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                            for b in dis:
                                                dis_percent=dis_percent+int(b.Discount_Percentage)
                                            after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                            f_price=float(i['Product_Selling_Price'])-after_discount
                                            dis_percent=0

                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg
                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=f_price
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)
                        else:
                            att_op=AttributeOptions.objects.filter(Q(option__in=size)|Q(option__in=color))
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                                print(pro,'aaaa')
                                if pro:
                                    for i in pro:
                                        qs=Product.objects.filter(id=i.id).values()

                                        for i in qs:
                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0

                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg
                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=i['Product_Selling_Price']
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)


                    else:
                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:
                            att_op=AttributeOptions.objects.filter(option__in=color)
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) )
                                if pro:
                                    for i in pro:

                                        qs=Product.objects.filter(id=i.id).values()
                                        # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                    # return Response(qs)
                                        for i in qs:
                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0
                                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                            for b in dis:
                                                dis_percent=dis_percent+int(b.Discount_Percentage)
                                            after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                            f_price=float(i['Product_Selling_Price'])-after_discount
                                            dis_percent=0

                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg
                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=f_price
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)
                        else:
                            att_op=AttributeOptions.objects.filter(option__in=color)
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) )
                                if pro:
                                    for i in pro:

                                        qs=Product.objects.filter(id=i.id).values()
                                        # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                    # return Response(qs)
                                        for i in qs:
                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0
                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg
                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=i['Product_Selling_Price']
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)
                            # else:
                            #     qs = Product.objects.filter( Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                            #     return Response(qs)

                else:
                    #######
                    today = datetime.date.today()
                    discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    if discount:
                        qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                        for i in qs:
                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                            if rating_count>0:
                                for k in rating:
                                    if k.star_rating!='':

                                        total_rating=total_rating+int(k.star_rating)
                                    else:
                                        total_rating=0
                                avg=int(total_rating)/int(rating_count)
                            else:
                                avg=0
                            total_rating=0
                            rating_count=0
                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                            for b in dis:
                                dis_percent=dis_percent+int(b.Discount_Percentage)
                            after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                            f_price=float(i['Product_Selling_Price'])-after_discount
                            dis_percent=0

                            brand=Brand.objects.filter(id=i['brand_id'])
                            for k in brand:
                                brand_name=k.brand_name
                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                            for l in p_category:
                                Product_Category_Name=l.Product_Category_Name
                                image=str(l.image)

                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                            for m in ps_category:
                                product_sub_category_name=m.product_sub_category_name
                                ps_image=str(m.image)

                            res={}
                            res['rating']=avg
                            res['id']=i['id']
                            res['brand_name']=brand_name
                            res['brand_id']=i['brand_id']
                            res['Product_Name']=i['Product_Name']
                            res['Product_Description']=i['Product_Description']
                            res['Product_Image']=i['Product_Image']
                            res['Product_Video']=i['Product_Video']
                            res['Product_Selling_Price']=f_price
                            res['Gst']=i['Gst']
                            res['Product_Listed_Price']=i['Product_Listed_Price']
                            res['Product_Details']=i['Product_Details']
                            res['Status']=i['Status']
                            res['Create_TimeStamp']=i['Create_TimeStamp']
                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                            res['Wash_instructions']=i['Wash_instructions']
                            res['Product_Category']=i['Product_Category_id']
                            res['category_image']=image
                            res['Product_Category_Name']=Product_Category_Name
                            res['product_sub_category']=i['product_sub_category_id']
                            res['product_sub_category_name']=product_sub_category_name
                            res['sub_category_image']=ps_image
                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                            # if wishlist:
                            #     res['wishlist']=True
                            res['wishlist']=False
                            # res['wishlist']=i['wishlistss']
                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                            # res['color_count']=items
                            res['attribute_option']=[]

                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                            for k in item:
                                id=k.id

                                option=AttributeOptions.objects.filter(attributes_id=id)
                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                res['color_count']=option_count
                                for j in option:

                                    res['attribute_option'].append({
                                    'option_id':j.id,
                                    'option':j.option,

                                    })
                            Arr.append(res)
                        return Response(Arr)
                    else:
                        qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                        for i in qs:
                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                            if rating_count>0:
                                for k in rating:
                                    if k.star_rating!='':

                                        total_rating=total_rating+int(k.star_rating)
                                    else:
                                        total_rating=0
                                avg=int(total_rating)/int(rating_count)
                            else:
                                avg=0
                            total_rating=0
                            rating_count=0
                            brand=Brand.objects.filter(id=i['brand_id'])
                            for k in brand:
                                brand_name=k.brand_name
                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                            for l in p_category:
                                Product_Category_Name=l.Product_Category_Name
                                image=str(l.image)

                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                            for m in ps_category:
                                product_sub_category_name=m.product_sub_category_name
                                ps_image=str(m.image)

                            res={}
                            res['rating']=avg
                            res['id']=i['id']
                            res['brand_name']=brand_name
                            res['brand_id']=i['brand_id']
                            res['Product_Name']=i['Product_Name']
                            res['Product_Description']=i['Product_Description']
                            res['Product_Image']=i['Product_Image']
                            res['Product_Video']=i['Product_Video']
                            res['Product_Selling_Price']=i['Product_Selling_Price']
                            res['Gst']=i['Gst']
                            res['Product_Listed_Price']=i['Product_Listed_Price']
                            res['Product_Details']=i['Product_Details']
                            res['Status']=i['Status']
                            res['Create_TimeStamp']=i['Create_TimeStamp']
                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                            res['Wash_instructions']=i['Wash_instructions']
                            res['Product_Category']=i['Product_Category_id']
                            res['category_image']=image
                            res['Product_Category_Name']=Product_Category_Name
                            res['product_sub_category']=i['product_sub_category_id']
                            res['product_sub_category_name']=product_sub_category_name
                            res['sub_category_image']=ps_image
                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                            # if wishlist:
                            #     res['wishlist']=True
                            res['wishlist']=False
                            # res['wishlist']=i['wishlistss']
                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                            # res['color_count']=items
                            res['attribute_option']=[]

                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                            for k in item:
                                id=k.id

                                option=AttributeOptions.objects.filter(attributes_id=id)
                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                res['color_count']=option_count
                                for j in option:

                                    res['attribute_option'].append({
                                    'option_id':j.id,
                                    'option':j.option,

                                    })
                            Arr.append(res)
                        return Response(Arr)


            else:

                today = datetime.date.today()
                discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                if discount:
                    print('disssssss')
                    qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) ).values()
                    for i in qs:
                    # for i in all_values:
                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        for b in dis:
                            dis_percent=dis_percent+int(b.Discount_Percentage)
                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                        f_price=float(i['Product_Selling_Price'])-after_discount
                        dis_percent=0

                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg
                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=f_price
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                        # if wishlist:
                        #     res['wishlist']=True
                        res['wishlist']=False
                        # res['wishlist']=i['wishlistss']
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                    return Response(Arr)
                else:

                    qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) ).values()
                    for i in qs:
                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg
                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=i['Product_Selling_Price']
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                        # if wishlist:
                        #     res['wishlist']=True
                        res['wishlist']=False
                        # res['wishlist']=i['wishlistss']
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                    return Response(Arr)

        if price:
            if brand_id:
                if color:
                    if size:

                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:

                            att_op=AttributeOptions.objects.filter(Q(option__in=size)|Q(option__in=color))
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) )
                                print(pro,'aaaa')
                                if pro:
                                    for i in pro:
                                        qs = Product.objects.filter(id=i.id).values()
                                        # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                    # return Response(qs)
                                        for i in qs:

                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0
                                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                            for b in dis:
                                                dis_percent=dis_percent+int(b.Discount_Percentage)
                                            after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                            f_price=float(i['Product_Selling_Price'])-after_discount
                                            dis_percent=0

                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg

                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=f_price
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)
                        else:
                            att_op=AttributeOptions.objects.filter(Q(option__in=size)|Q(option__in=color))
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) )
                                print(pro,'aaaa')
                                if pro:
                                    for i in pro:
                                        qs = Product.objects.filter(id=i.id).values()
                                        # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                    # return Response(qs)
                                        for i in qs:

                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0
                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg
                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=i['Product_Selling_Price']
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)
                            # else:
                            #     qs = Product.objects.filter( Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                            #     return Response(qs)
                    else:

                        today = datetime.date.today()
                        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        if discount:

                            att_op=AttributeOptions.objects.filter(option__in=color)
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)&Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                                if pro:
                                    for i in pro:
                                        qs = Product.objects.filter(id=i.id).values()
                                        # qs = Product.objects.filter( Q(product_sub_category_id=product_sub_category_id)&Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                    # return Response(qs)
                                        for i in qs:
                                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                            for b in dis:
                                                dis_percent=dis_percent+int(b.Discount_Percentage)
                                            after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                            f_price=float(i['Product_Selling_Price'])-after_discount
                                            dis_percent=0

                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg

                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=f_price
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)
                        else:
                            att_op=AttributeOptions.objects.filter(option__in=color)
                            for j in att_op:
                                att=Attributes.objects.get(id=j.attributes_id)
                                pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)&Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                                if pro:
                                    for i in pro:
                                        qs = Product.objects.filter(id=i.id).values()
                                        # qs = Product.objects.filter( Q(product_sub_category_id=product_sub_category_id)&Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                    # return Response(qs)
                                        for i in qs:
                                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                            if rating_count>0:
                                                for k in rating:
                                                    if k.star_rating!='':

                                                        total_rating=total_rating+int(k.star_rating)
                                                    else:
                                                        total_rating=0
                                                avg=int(total_rating)/int(rating_count)
                                            else:
                                                avg=0
                                            total_rating=0
                                            rating_count=0
                                            brand=Brand.objects.filter(id=i['brand_id'])
                                            for k in brand:
                                                brand_name=k.brand_name
                                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                            for l in p_category:
                                                Product_Category_Name=l.Product_Category_Name
                                                image=str(l.image)

                                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                            for m in ps_category:
                                                product_sub_category_name=m.product_sub_category_name
                                                ps_image=str(m.image)

                                            res={}
                                            res['rating']=avg

                                            res['id']=i['id']
                                            res['brand_name']=brand_name
                                            res['brand_id']=i['brand_id']
                                            res['Product_Name']=i['Product_Name']
                                            res['Product_Description']=i['Product_Description']
                                            res['Product_Image']=i['Product_Image']
                                            res['Product_Video']=i['Product_Video']
                                            res['Product_Selling_Price']=i['Product_Selling_Price']
                                            res['Gst']=i['Gst']
                                            res['Product_Listed_Price']=i['Product_Listed_Price']
                                            res['Product_Details']=i['Product_Details']
                                            res['Status']=i['Status']
                                            res['Create_TimeStamp']=i['Create_TimeStamp']
                                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                            res['Wash_instructions']=i['Wash_instructions']
                                            res['Product_Category']=i['Product_Category_id']
                                            res['category_image']=image
                                            res['Product_Category_Name']=Product_Category_Name
                                            res['product_sub_category']=i['product_sub_category_id']
                                            res['product_sub_category_name']=product_sub_category_name
                                            res['sub_category_image']=ps_image
                                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                            # if wishlist:
                                            #     res['wishlist']=True
                                            res['wishlist']=False
                                            # res['wishlist']=i['wishlistss']
                                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                            # res['color_count']=items
                                            res['attribute_option']=[]

                                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                            for k in item:
                                                id=k.id

                                                option=AttributeOptions.objects.filter(attributes_id=id)
                                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                                res['color_count']=option_count
                                                for j in option:

                                                    res['attribute_option'].append({
                                                    'option_id':j.id,
                                                    'option':j.option,

                                                    })
                                            Arr.append(res)
                            output = []
                            for x in Arr:
                                if x not in output:
                                    output.append(x)
                            return Response(output)

                else:

                    today = datetime.date.today()
                    discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    if discount:

                        qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                        for i in qs:
                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                            if rating_count>0:
                                for k in rating:
                                    if k.star_rating!='':

                                        total_rating=total_rating+int(k.star_rating)
                                    else:
                                        total_rating=0
                                avg=int(total_rating)/int(rating_count)
                            else:
                                avg=0
                            total_rating=0
                            rating_count=0
                            dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                            for b in dis:
                                dis_percent=dis_percent+int(b.Discount_Percentage)
                            after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                            f_price=float(i['Product_Selling_Price'])-after_discount
                            dis_percent=0

                            brand=Brand.objects.filter(id=i['brand_id'])
                            for k in brand:
                                brand_name=k.brand_name
                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                            for l in p_category:
                                Product_Category_Name=l.Product_Category_Name
                                image=str(l.image)

                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                            for m in ps_category:
                                product_sub_category_name=m.product_sub_category_name
                                ps_image=str(m.image)

                            res={}
                            res['rating']=avg
                            res['id']=i['id']
                            res['brand_name']=brand_name
                            res['brand_id']=i['brand_id']
                            res['Product_Name']=i['Product_Name']
                            res['Product_Description']=i['Product_Description']
                            res['Product_Image']=i['Product_Image']
                            res['Product_Video']=i['Product_Video']
                            res['Product_Selling_Price']=f_price
                            res['Gst']=i['Gst']
                            res['Product_Listed_Price']=i['Product_Listed_Price']
                            res['Product_Details']=i['Product_Details']
                            res['Status']=i['Status']
                            res['Create_TimeStamp']=i['Create_TimeStamp']
                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                            res['Wash_instructions']=i['Wash_instructions']
                            res['Product_Category']=i['Product_Category_id']
                            res['category_image']=image
                            res['Product_Category_Name']=Product_Category_Name
                            res['product_sub_category']=i['product_sub_category_id']
                            res['product_sub_category_name']=product_sub_category_name
                            res['sub_category_image']=ps_image
                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                            # if wishlist:
                            #     res['wishlist']=True
                            res['wishlist']=False
                            # res['wishlist']=i['wishlistss']
                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                            # res['color_count']=items
                            res['attribute_option']=[]

                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                            for k in item:
                                id=k.id

                                option=AttributeOptions.objects.filter(attributes_id=id)
                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                res['color_count']=option_count
                                for j in option:

                                    res['attribute_option'].append({
                                    'option_id':j.id,
                                    'option':j.option,

                                    })
                            Arr.append(res)
                        return Response(Arr)
                    else:
                        qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                        for i in qs:
                            rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                            rating =Reviews.objects.filter(Product_ID_id=i['id'])
                            if rating_count>0:
                                for k in rating:
                                    if k.star_rating!='':

                                        total_rating=total_rating+int(k.star_rating)
                                    else:
                                        total_rating=0
                                avg=int(total_rating)/int(rating_count)
                            else:
                                avg=0
                            total_rating=0
                            rating_count=0

                            brand=Brand.objects.filter(id=i['brand_id'])
                            for k in brand:
                                brand_name=k.brand_name
                            p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                            for l in p_category:
                                Product_Category_Name=l.Product_Category_Name
                                image=str(l.image)

                            ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                            for m in ps_category:
                                product_sub_category_name=m.product_sub_category_name
                                ps_image=str(m.image)

                            res={}
                            res['rating']=avg
                            res['id']=i['id']
                            res['brand_name']=brand_name
                            res['brand_id']=i['brand_id']
                            res['Product_Name']=i['Product_Name']
                            res['Product_Description']=i['Product_Description']
                            res['Product_Image']=i['Product_Image']
                            res['Product_Video']=i['Product_Video']
                            res['Product_Selling_Price']=i['Product_Selling_Price']
                            res['Gst']=i['Gst']
                            res['Product_Listed_Price']=i['Product_Listed_Price']
                            res['Product_Details']=i['Product_Details']
                            res['Status']=i['Status']
                            res['Create_TimeStamp']=i['Create_TimeStamp']
                            res['HSN_SAC_Code']=i['HSN_SAC_Code']
                            res['Wash_instructions']=i['Wash_instructions']
                            res['Product_Category']=i['Product_Category_id']
                            res['category_image']=image
                            res['Product_Category_Name']=Product_Category_Name
                            res['product_sub_category']=i['product_sub_category_id']
                            res['product_sub_category_name']=product_sub_category_name
                            res['sub_category_image']=ps_image
                            # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                            # if wishlist:
                            #     res['wishlist']=True
                            res['wishlist']=False
                            # res['wishlist']=i['wishlistss']
                            # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                            # res['color_count']=items
                            res['attribute_option']=[]

                            item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                            for k in item:
                                id=k.id

                                option=AttributeOptions.objects.filter(attributes_id=id)
                                option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                res['color_count']=option_count
                                for j in option:

                                    res['attribute_option'].append({
                                    'option_id':j.id,
                                    'option':j.option,

                                    })
                            Arr.append(res)
                        return Response(Arr)
            else:

                today = datetime.date.today()
                discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                if discount:
                    qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(Product_Selling_Price__range=pricess) ).values()
                    for i in qs:

                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        for b in dis:
                            dis_percent=dis_percent+int(b.Discount_Percentage)
                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                        f_price=float(i['Product_Selling_Price'])-after_discount
                        dis_percent=0

                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg

                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=f_price
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                        # if wishlist:
                        #     res['wishlist']=True
                        res['wishlist']=False
                        # res['wishlist']=i['wishlistss']
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                    return Response(Arr)
                else:
                    qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(Product_Selling_Price__range=pricess) ).values()
                    for i in qs:

                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg

                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=i['Product_Selling_Price']
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                        # if wishlist:
                        #     res['wishlist']=True
                        res['wishlist']=False
                        # res['wishlist']=i['wishlistss']
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                    return Response(Arr)
        # else:
        #     qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)).values()
        #     return Response(qs)

        if size:
            if brand_id:
                if price:

                    today = datetime.date.today()
                    discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    if discount:

                        att_op=AttributeOptions.objects.filter(option__in=size)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                # return Response(qs)
                                    for i in qs:

                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0
                                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                        for b in dis:
                                            dis_percent=dis_percent+int(b.Discount_Percentage)
                                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                        f_price=float(i['Product_Selling_Price'])-after_discount
                                        dis_percent=0

                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg
                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=f_price
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                    else:
                        att_op=AttributeOptions.objects.filter(option__in=size)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                # return Response(qs)
                                    for i in qs:

                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0
                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg
                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=i['Product_Selling_Price']
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                        # else:
                        #     qs = Product.objects.filter( Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                        #     return Response(qs)
                else:
                    today = datetime.date.today()
                    discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    if discount:

                        att_op=AttributeOptions.objects.filter(option__in=size)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) )
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) ).values()
                                # return Response(qs)
                                    for i in qs:
                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0
                                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                        for b in dis:
                                            dis_percent=dis_percent+int(b.Discount_Percentage)
                                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                        f_price=float(i['Product_Selling_Price'])-after_discount
                                        dis_percent=0

                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg

                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=f_price
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                    else:
                        att_op=AttributeOptions.objects.filter(option__in=size)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id) )
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) ).values()
                                # return Response(qs)
                                    for i in qs:
                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0


                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg

                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=i['Product_Selling_Price']
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                        # else:
                        #     qs = Product.objects.filter( Q(brand_id__in=brand_id)).values()
                        #     return Response(qs)

            else:

                today = datetime.date.today()
                discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                if discount:

                    att_op=AttributeOptions.objects.filter(option__in=size)
                    for j in att_op:
                        att=Attributes.objects.get(id=j.attributes_id)
                        pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id))
                        if pro:
                            for i in pro:
                                qs = Product.objects.filter(id=i.id).values()
                                # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)&Q(id=i.id) ).values()
                            # return Response(qs)
                                for i in qs:
                                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                    if rating_count>0:
                                        for k in rating:
                                            if k.star_rating!='':

                                                total_rating=total_rating+int(k.star_rating)
                                            else:
                                                total_rating=0
                                        avg=int(total_rating)/int(rating_count)
                                    else:
                                        avg=0
                                    total_rating=0
                                    rating_count=0
                                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                    for b in dis:
                                        dis_percent=dis_percent+int(b.Discount_Percentage)
                                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                    f_price=float(i['Product_Selling_Price'])-after_discount
                                    dis_percent=0

                                    brand=Brand.objects.filter(id=i['brand_id'])
                                    for k in brand:
                                        brand_name=k.brand_name
                                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                    for l in p_category:
                                        Product_Category_Name=l.Product_Category_Name
                                        image=str(l.image)

                                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                    for m in ps_category:
                                        product_sub_category_name=m.product_sub_category_name
                                        ps_image=str(m.image)

                                    res={}
                                    res['rating']=avg
                                    res['id']=i['id']
                                    res['brand_name']=brand_name
                                    res['brand_id']=i['brand_id']
                                    res['Product_Name']=i['Product_Name']
                                    res['Product_Description']=i['Product_Description']
                                    res['Product_Image']=i['Product_Image']
                                    res['Product_Video']=i['Product_Video']
                                    res['Product_Selling_Price']=f_price
                                    res['Gst']=i['Gst']
                                    res['Product_Listed_Price']=i['Product_Listed_Price']
                                    res['Product_Details']=i['Product_Details']
                                    res['Status']=i['Status']
                                    res['Create_TimeStamp']=i['Create_TimeStamp']
                                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                    res['Wash_instructions']=i['Wash_instructions']
                                    res['Product_Category']=i['Product_Category_id']
                                    res['category_image']=image
                                    res['Product_Category_Name']=Product_Category_Name
                                    res['product_sub_category']=i['product_sub_category_id']
                                    res['product_sub_category_name']=product_sub_category_name
                                    res['sub_category_image']=ps_image
                                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                    # if wishlist:
                                    #     res['wishlist']=True
                                    res['wishlist']=False
                                    # res['wishlist']=i['wishlistss']
                                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                    # res['color_count']=items
                                    res['attribute_option']=[]

                                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                    for k in item:
                                        id=k.id

                                        option=AttributeOptions.objects.filter(attributes_id=id)
                                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                        res['color_count']=option_count
                                        for j in option:

                                            res['attribute_option'].append({
                                            'option_id':j.id,
                                            'option':j.option,

                                            })
                                    Arr.append(res)
                    output = []
                    for x in Arr:
                        if x not in output:
                            output.append(x)
                    return Response(output)
                else:
                    att_op=AttributeOptions.objects.filter(option__in=size)
                    for j in att_op:
                        att=Attributes.objects.get(id=j.attributes_id)
                        pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id))
                        if pro:
                            for i in pro:
                                qs = Product.objects.filter(id=i.id).values()
                                # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)&Q(id=i.id) ).values()
                            # return Response(qs)
                                for i in qs:
                                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                    if rating_count>0:
                                        for k in rating:
                                            if k.star_rating!='':

                                                total_rating=total_rating+int(k.star_rating)
                                            else:
                                                total_rating=0
                                        avg=int(total_rating)/int(rating_count)
                                    else:
                                        avg=0
                                    total_rating=0
                                    rating_count=0


                                    brand=Brand.objects.filter(id=i['brand_id'])
                                    for k in brand:
                                        brand_name=k.brand_name
                                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                    for l in p_category:
                                        Product_Category_Name=l.Product_Category_Name
                                        image=str(l.image)

                                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                    for m in ps_category:
                                        product_sub_category_name=m.product_sub_category_name
                                        ps_image=str(m.image)

                                    res={}
                                    res['rating']=avg
                                    res['id']=i['id']
                                    res['brand_name']=brand_name
                                    res['brand_id']=i['brand_id']
                                    res['Product_Name']=i['Product_Name']
                                    res['Product_Description']=i['Product_Description']
                                    res['Product_Image']=i['Product_Image']
                                    res['Product_Video']=i['Product_Video']
                                    res['Product_Selling_Price']=i['Product_Selling_Price']
                                    res['Gst']=i['Gst']
                                    res['Product_Listed_Price']=i['Product_Listed_Price']
                                    res['Product_Details']=i['Product_Details']
                                    res['Status']=i['Status']
                                    res['Create_TimeStamp']=i['Create_TimeStamp']
                                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                    res['Wash_instructions']=i['Wash_instructions']
                                    res['Product_Category']=i['Product_Category_id']
                                    res['category_image']=image
                                    res['Product_Category_Name']=Product_Category_Name
                                    res['product_sub_category']=i['product_sub_category_id']
                                    res['product_sub_category_name']=product_sub_category_name
                                    res['sub_category_image']=ps_image
                                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                    # if wishlist:
                                    #     res['wishlist']=True
                                    res['wishlist']=False
                                    # res['wishlist']=i['wishlistss']
                                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                    # res['color_count']=items
                                    res['attribute_option']=[]

                                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                    for k in item:
                                        id=k.id

                                        option=AttributeOptions.objects.filter(attributes_id=id)
                                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                        res['color_count']=option_count
                                        for j in option:

                                            res['attribute_option'].append({
                                            'option_id':j.id,
                                            'option':j.option,

                                            })
                                    Arr.append(res)
                    output = []
                    for x in Arr:
                        if x not in output:
                            output.append(x)
                    return Response(output)

        if color:
            if brand_id:
                if price:
                    today = datetime.date.today()
                    discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    if discount:
                        att_op=AttributeOptions.objects.filter(option__in=color)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                # return Response(qs)
                                    for i in qs:
                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0
                                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                        for b in dis:
                                            dis_percent=dis_percent+int(b.Discount_Percentage)
                                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                        f_price=float(i['Product_Selling_Price'])-after_discount
                                        dis_percent=0

                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg
                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=f_price
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                    else:
                        att_op=AttributeOptions.objects.filter(option__in=color)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)& Q(Product_Selling_Price__range=pricess) )
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(brand_id__in=brand_id)&Q(id=i.id) & Q(Product_Selling_Price__range=pricess) ).values()
                                # return Response(qs)
                                    for i in qs:
                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0


                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg
                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=i['Product_Selling_Price']
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                        # else:
                        #     qs = Product.objects.filter( Q(brand_id__in=brand_id) & Q(Product_Selling_Price__range=pricess) ).values()
                        #     return Response(qs)
                else:

                    today = datetime.date.today()
                    discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                    if discount:
                        att_op=AttributeOptions.objects.filter(option__in=color)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(brand_id__in=brand_id)&Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id))
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(id=i.id) ).values()
                                # return Response(qs)
                                    for i in qs:
                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0
                                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                        for b in dis:
                                            dis_percent=dis_percent+int(b.Discount_Percentage)
                                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                        f_price=float(i['Product_Selling_Price'])-after_discount
                                        dis_percent=0

                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg
                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=f_price
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)
                    else:
                        att_op=AttributeOptions.objects.filter(option__in=color)
                        for j in att_op:
                            att=Attributes.objects.get(id=j.attributes_id)
                            pro=Product.objects.filter(Q(brand_id__in=brand_id)&Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id))
                            if pro:
                                for i in pro:
                                    qs = Product.objects.filter(id=i.id).values()
                                    # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)& Q(id=i.id) ).values()
                                # return Response(qs)
                                    for i in qs:
                                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                        if rating_count>0:
                                            for k in rating:
                                                if k.star_rating!='':

                                                    total_rating=total_rating+int(k.star_rating)
                                                else:
                                                    total_rating=0
                                            avg=int(total_rating)/int(rating_count)
                                        else:
                                            avg=0
                                        total_rating=0
                                        rating_count=0

                                        brand=Brand.objects.filter(id=i['brand_id'])
                                        for k in brand:
                                            brand_name=k.brand_name
                                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                        for l in p_category:
                                            Product_Category_Name=l.Product_Category_Name
                                            image=str(l.image)

                                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                        for m in ps_category:
                                            product_sub_category_name=m.product_sub_category_name
                                            ps_image=str(m.image)

                                        res={}
                                        res['rating']=avg
                                        res['id']=i['id']
                                        res['brand_name']=brand_name
                                        res['brand_id']=i['brand_id']
                                        res['Product_Name']=i['Product_Name']
                                        res['Product_Description']=i['Product_Description']
                                        res['Product_Image']=i['Product_Image']
                                        res['Product_Video']=i['Product_Video']
                                        res['Product_Selling_Price']=i['Product_Selling_Price']
                                        res['Gst']=i['Gst']
                                        res['Product_Listed_Price']=i['Product_Listed_Price']
                                        res['Product_Details']=i['Product_Details']
                                        res['Status']=i['Status']
                                        res['Create_TimeStamp']=i['Create_TimeStamp']
                                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                        res['Wash_instructions']=i['Wash_instructions']
                                        res['Product_Category']=i['Product_Category_id']
                                        res['category_image']=image
                                        res['Product_Category_Name']=Product_Category_Name
                                        res['product_sub_category']=i['product_sub_category_id']
                                        res['product_sub_category_name']=product_sub_category_name
                                        res['sub_category_image']=ps_image
                                        # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                        # if wishlist:
                                        #     res['wishlist']=True
                                        res['wishlist']=False
                                        # res['wishlist']=i['wishlistss']
                                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                        # res['color_count']=items
                                        res['attribute_option']=[]

                                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                        for k in item:
                                            id=k.id

                                            option=AttributeOptions.objects.filter(attributes_id=id)
                                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                            res['color_count']=option_count
                                            for j in option:

                                                res['attribute_option'].append({
                                                'option_id':j.id,
                                                'option':j.option,

                                                })
                                        Arr.append(res)
                        output = []
                        for x in Arr:
                            if x not in output:
                                output.append(x)
                        return Response(output)

                        # else:
                        #     qs = Product.objects.filter( Q(brand_id__in=brand_id)).values()
                        #     return Response(qs)

            else:
                today = datetime.date.today()
                discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                if discount:
                    att_op=AttributeOptions.objects.filter(option__in=color)
                    for j in att_op:
                        att=Attributes.objects.get(id=j.attributes_id)
                        pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id))
                        if pro:
                            for i in pro:
                                qs = Product.objects.filter(id=i.id).values()
                                # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)&Q(id=i.id) ).values()
                            # return Response(qs)
                                for i in qs:
                                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                    if rating_count>0:
                                        for k in rating:
                                            if k.star_rating!='':

                                                total_rating=total_rating+int(k.star_rating)
                                            else:
                                                total_rating=0
                                        avg=int(total_rating)/int(rating_count)
                                    else:
                                        avg=0
                                    total_rating=0
                                    rating_count=0
                                    dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                                    for b in dis:
                                        dis_percent=dis_percent+int(b.Discount_Percentage)
                                    after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                                    f_price=float(i['Product_Selling_Price'])-after_discount
                                    dis_percent=0

                                    brand=Brand.objects.filter(id=i['brand_id'])
                                    for k in brand:
                                        brand_name=k.brand_name
                                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                    for l in p_category:
                                        Product_Category_Name=l.Product_Category_Name
                                        image=str(l.image)

                                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                    for m in ps_category:
                                        product_sub_category_name=m.product_sub_category_name
                                        ps_image=str(m.image)

                                    res={}
                                    res['rating']=avg
                                    res['id']=i['id']
                                    res['brand_name']=brand_name
                                    res['brand_id']=i['brand_id']
                                    res['Product_Name']=i['Product_Name']
                                    res['Product_Description']=i['Product_Description']
                                    res['Product_Image']=i['Product_Image']
                                    res['Product_Video']=i['Product_Video']
                                    res['Product_Selling_Price']=f_price
                                    res['Gst']=i['Gst']
                                    res['Product_Listed_Price']=i['Product_Listed_Price']
                                    res['Product_Details']=i['Product_Details']
                                    res['Status']=i['Status']
                                    res['Create_TimeStamp']=i['Create_TimeStamp']
                                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                    res['Wash_instructions']=i['Wash_instructions']
                                    res['Product_Category']=i['Product_Category_id']
                                    res['category_image']=image
                                    res['Product_Category_Name']=Product_Category_Name
                                    res['product_sub_category']=i['product_sub_category_id']
                                    res['product_sub_category_name']=product_sub_category_name
                                    res['sub_category_image']=ps_image
                                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                    # if wishlist:
                                    #     res['wishlist']=True
                                    res['wishlist']=False
                                    # res['wishlist']=i['wishlistss']
                                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                    # res['color_count']=items
                                    res['attribute_option']=[]

                                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                    for k in item:
                                        id=k.id

                                        option=AttributeOptions.objects.filter(attributes_id=id)
                                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                        res['color_count']=option_count
                                        for j in option:

                                            res['attribute_option'].append({
                                            'option_id':j.id,
                                            'option':j.option,

                                            })
                                    Arr.append(res)
                    output = []
                    for x in Arr:
                        if x not in output:
                            output.append(x)
                    return Response(output)
                else:
                    att_op=AttributeOptions.objects.filter(option__in=color)
                    for j in att_op:
                        att=Attributes.objects.get(id=j.attributes_id)
                        pro=Product.objects.filter(Q(id=att.Product_ID_id)&Q(product_sub_category_id=product_sub_category_id))
                        if pro:
                            for i in pro:
                                qs = Product.objects.filter(id=i.id).values()
                                # qs = Product.objects.filter(Q(product_sub_category_id=product_sub_category_id)&Q(id=i.id) ).values()
                            # return Response(qs)
                                for i in qs:
                                    rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                                    rating =Reviews.objects.filter(Product_ID_id=i['id'])
                                    if rating_count>0:
                                        for k in rating:
                                            if k.star_rating!='':

                                                total_rating=total_rating+int(k.star_rating)
                                            else:
                                                total_rating=0
                                        avg=int(total_rating)/int(rating_count)
                                    else:
                                        avg=0
                                    total_rating=0
                                    rating_count=0

                                    brand=Brand.objects.filter(id=i['brand_id'])
                                    for k in brand:
                                        brand_name=k.brand_name
                                    p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                                    for l in p_category:
                                        Product_Category_Name=l.Product_Category_Name
                                        image=str(l.image)

                                    ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                                    for m in ps_category:
                                        product_sub_category_name=m.product_sub_category_name
                                        ps_image=str(m.image)

                                    res={}
                                    res['rating']=avg
                                    res['id']=i['id']
                                    res['brand_name']=brand_name
                                    res['brand_id']=i['brand_id']
                                    res['Product_Name']=i['Product_Name']
                                    res['Product_Description']=i['Product_Description']
                                    res['Product_Image']=i['Product_Image']
                                    res['Product_Video']=i['Product_Video']
                                    res['Product_Selling_Price']=i['Product_Selling_Price']
                                    res['Gst']=i['Gst']
                                    res['Product_Listed_Price']=i['Product_Listed_Price']
                                    res['Product_Details']=i['Product_Details']
                                    res['Status']=i['Status']
                                    res['Create_TimeStamp']=i['Create_TimeStamp']
                                    res['HSN_SAC_Code']=i['HSN_SAC_Code']
                                    res['Wash_instructions']=i['Wash_instructions']
                                    res['Product_Category']=i['Product_Category_id']
                                    res['category_image']=image
                                    res['Product_Category_Name']=Product_Category_Name
                                    res['product_sub_category']=i['product_sub_category_id']
                                    res['product_sub_category_name']=product_sub_category_name
                                    res['sub_category_image']=ps_image
                                    # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                                    # if wishlist:
                                    #     res['wishlist']=True
                                    res['wishlist']=False
                                    # res['wishlist']=i['wishlistss']
                                    # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                                    # res['color_count']=items
                                    res['attribute_option']=[]

                                    item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                                    for k in item:
                                        id=k.id

                                        option=AttributeOptions.objects.filter(attributes_id=id)
                                        option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                                        res['color_count']=option_count
                                        for j in option:

                                            res['attribute_option'].append({
                                            'option_id':j.id,
                                            'option':j.option,

                                            })
                                    Arr.append(res)
                    output = []
                    for x in Arr:
                        if x not in output:
                            output.append(x)
                    return Response(output)





class Product_by_sub_categoryApiView(APIView):
    # queryset = Product.objects.all().values()
    def get(self,request):
        product_id =self.request.query_params.get('product_id')
        user_id =self.request.query_params.get('user_id')
        Arr=[]
        dis_percent=0
        avg=0
        total_rating=0

        if user_id != 'null':

            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:

                all_values = Product.objects.filter(id=product_id)
                for j in all_values:


                    id=j.product_sub_category_id
                    data=Product.objects.filter(product_sub_category_id=id).values()
                    for i in data:
                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        for b in dis:
                            dis_percent=dis_percent+int(b.Discount_Percentage)
                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                        f_price=float(i['Product_Selling_Price'])-after_discount
                        dis_percent=0
                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg
                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=f_price
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                        if wishlist:
                            res['wishlist']=True
                        else:
                            res['wishlist']=False



                        # res['wishlist']=i['wishlistss']
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                return Response(Arr)
            else:
                # wish=Wishlist.objects.filter(user_id=user_id)
                # for l in wish:
                #     product_idss=l.product_id
                all_values = Product.objects.filter(id=product_id)
                for j in all_values:
                    id=j.product_sub_category_id
                    data=Product.objects.filter(product_sub_category_id=id).values()
                    for i in data:
                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg
                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=i['Product_Selling_Price']
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                        if wishlist:
                            res['wishlist']=True
                        else:
                            res['wishlist']=False



                        # res['wishlist']=i['wishlistss']
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                return Response(Arr)

        else:
            print('eeeelse')
            today = datetime.date.today()
            discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
            if discount:
                all_values = Product.objects.filter(id=product_id)
                for j in all_values:

                    id=j.product_sub_category_id
                    data=Product.objects.filter(product_sub_category_id=id).values()
                    for i in data:
                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        for b in dis:
                            dis_percent=dis_percent+int(b.Discount_Percentage)
                        after_discount=float(i['Product_Selling_Price'])*dis_percent/100
                        f_price=float(i['Product_Selling_Price'])-after_discount
                        dis_percent=0
                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg
                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=f_price
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        res['wishlist']=False
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                return Response(Arr)
            else:
                all_values = Product.objects.filter(id=product_id)
                for j in all_values:
                    id=j.product_sub_category_id
                    data=Product.objects.filter(product_sub_category_id=id).values()
                    for i in data:
                        rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                        rating =Reviews.objects.filter(Product_ID_id=i['id'])
                        if rating_count>0:
                            for k in rating:
                                if k.star_rating!='':

                                    total_rating=total_rating+int(k.star_rating)
                                else:
                                    total_rating=0
                            avg=int(total_rating)/int(rating_count)
                        else:
                            avg=0
                        total_rating=0
                        rating_count=0
                        brand=Brand.objects.filter(id=i['brand_id'])
                        for k in brand:
                            brand_name=k.brand_name
                        p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                        for l in p_category:
                            Product_Category_Name=l.Product_Category_Name
                            image=str(l.image)

                        ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                        for m in ps_category:
                            product_sub_category_name=m.product_sub_category_name
                            ps_image=str(m.image)

                        res={}
                        res['rating']=avg
                        res['id']=i['id']
                        res['brand_name']=brand_name
                        res['brand_id']=i['brand_id']
                        res['Product_Name']=i['Product_Name']
                        res['Product_Description']=i['Product_Description']
                        res['Product_Image']=i['Product_Image']
                        res['Product_Video']=i['Product_Video']
                        res['Product_Selling_Price']=i['Product_Selling_Price']
                        res['Gst']=i['Gst']
                        res['Product_Listed_Price']=i['Product_Listed_Price']
                        res['Product_Details']=i['Product_Details']
                        res['Status']=i['Status']
                        res['Create_TimeStamp']=i['Create_TimeStamp']
                        res['HSN_SAC_Code']=i['HSN_SAC_Code']
                        res['Wash_instructions']=i['Wash_instructions']
                        res['Product_Category']=i['Product_Category_id']
                        res['category_image']=image
                        res['Product_Category_Name']=Product_Category_Name
                        res['product_sub_category']=i['product_sub_category_id']
                        res['product_sub_category_name']=product_sub_category_name
                        res['sub_category_image']=ps_image
                        res['wishlist']=False
                        # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                        # res['color_count']=items
                        res['attribute_option']=[]

                        item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                        for k in item:
                            id=k.id

                            option=AttributeOptions.objects.filter(attributes_id=id)
                            option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                            res['color_count']=option_count
                            for j in option:

                                res['attribute_option'].append({
                                'option_id':j.id,
                                'option':j.option,

                                })
                        Arr.append(res)
                return Response(Arr)


# shoppingsession=ShoppingSession.objects.filter(user_id=user_id)
#
# if shoppingsession:
#     for k in shoppingsession:
#         ids=k.id
#
#     test1 =CartItem.objects.filter(ShoppingSession_id=ids)
#     count=0
#     count1=0
#     for i in test1:
#         print(i.Product_ID_id,'llll')
#         att=ProductAttributes.objects.filter(user_id=user_id,Product_ID_id=i.Product_ID_id)
#         for k in att:
#             # Arr1.append(k.attributes.name)
#             Arr2.append(k.selectedoptions)
#         if len(Arr2)>1:
#             data.append({
#             'size':Arr2[1],
#             'color':Arr2[0],
#             'id':i.id,
#             })
#             count=count+1
#             count1=count1+1
import datetime as dt

class Purchase_detailsAPIView(APIView):
    def get(self,request):
        # payment_id = request.query_params.get('payment_id')
        user_id = request.query_params.get('user_id')
        Arr=[]
        dis_percent=0



        data= OrderDetails.objects.filter(user_id=user_id).order_by('-id')
        for j in data:

            order= PaymentDetails.objects.filter(orderdetails_id=j.id,status=True).values()
            for i in order:
                delivery_status=OrderDetails.objects.get(id=i['orderdetails_id'])
                address=User_Address.objects.filter(user_id=delivery_status.user_id,delfault_address=True)
                for k in address:
                    pincode=k.Pincode
                arival_day=ShippingCharges.objects.filter(pincode=pincode)
                for l in arival_day:
                    day=l.days


                arival_date=  i['create_timestamp'] + timedelta(days = int(day))

                res={}
                res['payment_id']=i['payment_id']
                res['amount']=int(float(i['amount']))
                res['OrderDetails_id']=i['orderdetails_id']
                res['delivery_status']=delivery_status.delivery_status
                res['date']=i['create_timestamp']
                res['arival_date']=arival_date
                res['details']=[]

                today = datetime.date.today()
                discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                if discount:

                    item=OrderItems.objects.filter(OrderDetails_id=i['orderdetails_id'])
                    for k in item:

                        dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                        for b in dis:
                            dis_percent=dis_percent+int(b.Discount_Percentage)
                        after_discount=float(int(k.Product_ID.Product_Selling_Price))*dis_percent/100
                        f_price=float(int(k.Product_ID.Product_Selling_Price))-after_discount
                        dis_percent=0

                        # data=ProductAttributes.objects.create(user_id=user_id,attributes_id=attributes_id,Product_ID_id=k.Product_ID_id,selectedoptions=option)
                        # attr=
                        res['details'].append({
                        'product_id':k.Product_ID_id,
                        'product_name':k.Product_ID.Product_Name,
                        'brand_name':k.Product_ID.brand.brand_name,
                        'product_image':str(k.Product_ID.Product_Image),
                        'quantity':k.quantity,
                        'Product_Selling_Price':int(int(k.quantity)*f_price),
                        'color':k.color,
                        'size':k.size
                        })
                    Arr.append(res)
                else:
                    item=OrderItems.objects.filter(OrderDetails_id=i['orderdetails_id'])
                    for k in item:
                        # data=ProductAttributes.objects.create(user_id=user_id,attributes_id=attributes_id,Product_ID_id=k.Product_ID_id,selectedoptions=option)
                        # attr=
                        res['details'].append({
                        'product_id':k.Product_ID_id,
                        'product_name':k.Product_ID.Product_Name,
                        'brand_name':k.Product_ID.brand.brand_name,
                        'product_image':str(k.Product_ID.Product_Image),
                        'quantity':k.quantity,
                        'Product_Selling_Price':int(int(k.Product_ID.Product_Selling_Price)*int(k.quantity)),
                        # 'Product_Selling_Price':f_price,
                        'color':k.color,
                        'size':k.size
                        })
                    Arr.append(res)
        return Response(Arr)




class Get_username_mobile(APIView):

    def get(self,request):
        user_id=self.request.query_params.get('user_id')
        if user_id:
            all_values = Custom_User.objects.filter(user_id=user_id).values()
            return Response(all_values)
        else:
            return Response({
            'error':{'message':'User id required!',
            'status_code':status.HTTP_404_NOT_FOUND,
            }},status=status.HTTP_404_NOT_FOUND)



class Purchase_details_by_paymentAPIView(APIView):
    def get(self,request):
        payment_id = request.query_params.get('payment_id')
        # user_id = request.query_params.get('user_id')
        Arr=[]

        # data= OrderDetails.objects.filter(user_id=user_id)
        # for j in data:

        order= PaymentDetails.objects.filter(payment_id=payment_id).values()

        for i in order:
            res={}
            res['payment_id']=i['payment_id']
            res['amount']=i['amount']
            res['OrderDetails_id']=i['orderdetails_id']
            res['date']=i['create_timestamp']
            res['details']=[]
            # Arr.append({
            # 'payment_id':i.payment_id,
            # 'amount':i.amount,
            # 'OrderDetails_id':i.OrderDetails_id,
            # })
            item=OrderItems.objects.filter(OrderDetails_id=i['orderdetails_id'])
            for k in item:
                res['details'].append({
                'product_id':k.Product_ID_id,
                'product_name':k.Product_ID.Product_Name,
                'product_image':str(k.Product_ID.Product_Image),
                'quantity':k.quantity,
                'Product_Selling_Price':int(k.Product_ID.Product_Selling_Price)
                })
            Arr.append(res)
        return Response(Arr)




from django.contrib.auth import authenticate
def otp_send():
    otpsss= random.randint(100000, 999999)
    return otpsss
forgotpass_otps=0

class ForgotPassword_send_otp(APIView):

    def post(self, request):
        data = request.data
        response={}
        username = data.get('username')

        user_check=User.objects.filter(username=username)
        if user_check:
            val=otp_send()
            global forgotpass_otps
            forgotpass_otps=val
            if '@' in username:

                message = inspect.cleandoc('''Hi,\n%s is your OTP to Forgot Password to your Kri8ev account.\nThis OTP is valid for next 10 minutes,
                                      \nWith Warm Regards,\nTeam Kri8eve,
                                       ''' % (val))
                send_mail(
                    'Kri8eve One Time Password (OTP)', message
                    ,
                    'gunjan.kr518@gmail.com',
                    [username],

                )
                data_dict = {}
                data_dict["Otp"] = val
                print(data_dict,'data_dict')
                # return JsonResponse(data_dict, safe=False)
                return Response('OTP send successfully')
            else:
                otpp=str(val)
                data_dict = {}
                data_dict["Otp"] = otpp
                return JsonResponse(data_dict, safe=False)

                # url = "https://api.kaleyra.io/v1/HXIN1712667009IN/messages"
                #
                # payload='to=91 '+username+'&sender=SPTLYT&type=OTP&body=Hi%2C%20'+otpp+'%20is%20your%20OTP%20to%20verify%20Spotlyt%20account%20and%20change%20your%20password.%20This%20OTP%20is%20valid%20for%20next%2010%20minutes.%20Regards%2C%20Team%20Spotlyt%20Academy&template_id=1207163645109721178'
                # headers = {
                #   'Content-Type': 'application/x-www-form-urlencoded',
                #   'api-key': 'Aa2eaa09645326f99dee7d298de3406d1'
                # }
                #
                # response = requests.request("POST", url, headers=headers, data=payload)
                # response="Message Send Successfully"
                # return Response(response, status=status.HTTP_200_OK)
                # return Response('Message Send Successfully')
        else:
            response['error'] = {'error': {
            'detail': 'Invalid Username!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)




class OTP_Verification_forgotpassAPIView(APIView):


    def post(self, request):
        data = request.data
        response={}
        otp = data.get('otp')
        print(forgotpass_otps,'ori')
        print(otp,'ori')
        if otp:
            if int(otp)==int(forgotpass_otps):
                response="OTP matcheds successfully"
                return Response(response, status=status.HTTP_200_OK)
            else:
                response['error'] = {'error': {
                'detail': 'Invalid OTP!', 'status': status.HTTP_401_UNAUTHORIZED}}

                return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)
        else:

            response['error'] = {'error': {
            'detail': 'OTP Required!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordUpdate(APIView):

    def post(self, request):

        data = request.data
        response={}


        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')


        # if password==confirm_password:
        user_check = Custom_User.objects.filter(username= username)

        if user_check:

            user_data = User.objects.get(username= username)
            user_data.set_password(password)
            user_data.save()







            user = auth.authenticate(username=username, password=password)
            custom=''

            custom_user = User.objects.get(id=user.id)

            custom = Custom_User.objects.get(user_id=custom_user.id)
            #     print(custom_user)
            auth_token = jwt.encode(
                {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

            serializer = CustUserSerializer(user)
            authorization = 'Bearer'+' '+auth_token
            response_result = {}
            response_result['result'] = {
                'detail': 'Login successfull',
                'token': authorization,
                'user_id':user.id,
                'username':user.username,
                'id':custom.id,
                'fullname':user.first_name,
                # 'fullname':custom.fullname,
                'email':user.email,
                'mobile_number':custom.Mobile_Number,
                'status': status.HTTP_200_OK}
            response['Authorization'] = authorization
            # response['Token-Type']      =   'Bearer'
            response['status'] = status.HTTP_200_OK

            return Response(response_result, headers=response,status=status.HTTP_200_OK)


                # message= 'Hello!\nYour password has been updated sucessfully. '
                # subject= 'Password Updated Sucessfully '
                # #
                # email = EmailMessage(subject, message, to=[user_data.email])
                # email.send()
            # response="Password Updated Sucessfully"
            # return Response(response, status=status.HTTP_200_OK)
            # else:
            #     user = auth.authenticate(username=username, password=password)
            #     custom=''
            #     # if user:
            #     custom_user = User.objects.get(id=user.id)
            #
            #     custom = Custom_User.objects.get(user_id=custom_user.id)
            #     #     print(custom_user)
            #     auth_token = jwt.encode(
            #         {'user_id': user.id, 'username': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
            #
            #     serializer = CustUserSerializer(user)
            #     authorization = 'Bearer'+' '+auth_token
            #     response_result = {}
            #     response_result['result'] = {
            #         'detail': 'Login successfull',
            #         'token': authorization,
            #         'user_id':user.id,
            #         'username':user.username,
            #         'id':custom.id,
            #         # 'fullname':custom.fullname,
            #         'email':user.email,
            #         'mobile_number':custom.Mobile_Number,
            #         'status': status.HTTP_200_OK}
            #     response['Authorization'] = authorization
            #     # response['Token-Type']      =   'Bearer'
            #     response['status'] = status.HTTP_200_OK
            #
            #     return Response(response_result, headers=response,status=status.HTTP_200_OK)
                # otpp=str(otpsss)
                # url = "https://api.kaleyra.io/v1/HXIN1712667009IN/messages"
                #
                # payload='to=91 '+username+'&sender=SPTLYT&type=OTP&body=%22Hi%20'+fullnames+'%20Thank%20you%20for%20registering%20with%20us.%20The%20Spotlyt%20is%20now%20on%20you!%22&template_id=1207163394382850917'
                # headers = {
                #   'Content-Type': 'application/x-www-form-urlencoded',
                #   'api-key': 'Aa2eaa09645326f99dee7d298de3406d1'
                # }
                #
                # response = requests.request("POST", url, headers=headers, data=payload)
                # response="Password Updated Sucessfully"
                # return Response(response, status=status.HTTP_200_OK)

        else:
            response['error'] = {'error': {
            'detail': 'Invalid Username!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)
        # else:
        #     response['error'] = {'error': {
        #     'detail': 'Password and Confirm password not matched!', 'status': status.HTTP_401_UNAUTHORIZED}}
        #
        #     return Response(response['error'],status= status.HTTP_401_UNAUTHORIZED)


class Product_filterAPI(APIView):

    def get(self,request):

        value = request.query_params.get('value')
        Arr=[]
        Arrs=[]
        opt=[]
        image=''
        dis_percent=0
        total_rating=0
        Product_Category_Name=''
        product_sub_category_name=''
        ps_image=''
        total_rating=0
        avg=0
        brand_name=''
        data= Product.objects.filter(Q(Product_Name=value)|Q(Product_Category__Product_Category_Name=value)|Q(product_sub_category__product_sub_category_name=value)|Q(brand__brand_name=value)).values()
        return Response(data)
        # today = datetime.date.today()
        # discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
        # if discount:
        #     all_values = Product.objects.filter(Q(Product_Name=value)|Q(Product_Category__Product_Category_Name=value)|Q(product_sub_category__product_sub_category_name=value)|Q(brand__brand_name=value)).values()
        #     for i in all_values:
        #         rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
        #         rating =Reviews.objects.filter(Product_ID_id=i['id'])
        #         if rating_count>0:
        #             for k in rating:
        #                 if k.star_rating!='':
        #
        #                     total_rating=total_rating+int(k.star_rating)
        #                 else:
        #                     total_rating=0
        #             avg=int(total_rating)/int(rating_count)
        #         else:
        #             avg=0
        #         total_rating=0
        #         rating_count=0
        #         dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
        #         for b in dis:
        #             dis_percent=dis_percent+int(b.Discount_Percentage)
        #         after_discount=float(i['Product_Selling_Price'])*dis_percent/100
        #         f_price=float(i['Product_Selling_Price'])-after_discount
        #         dis_percent=0
        #         brand=Brand.objects.filter(id=i['brand_id'])
        #         for k in brand:
        #             brand_name=k.brand_name
        #         p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
        #         for l in p_category:
        #             Product_Category_Name=l.Product_Category_Name
        #             image=str(l.image)
        #
        #         ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
        #         for m in ps_category:
        #             product_sub_category_name=m.product_sub_category_name
        #             ps_image=str(m.image)
        #
        #         res={}
        #         res['rating']=avg
        #         res['id']=i['id']
        #         res['brand_name']=brand_name
        #         res['brand_id']=i['brand_id']
        #         res['Product_Name']=i['Product_Name']
        #         res['Product_Description']=i['Product_Description']
        #         res['Product_Image']=i['Product_Image']
        #         res['Product_Video']=i['Product_Video']
        #         res['Product_Selling_Price']=f_price
        #         res['Gst']=i['Gst']
        #         res['Product_Listed_Price']=i['Product_Listed_Price']
        #         res['Product_Details']=i['Product_Details']
        #         res['Status']=i['Status']
        #         res['Create_TimeStamp']=i['Create_TimeStamp']
        #         res['HSN_SAC_Code']=i['HSN_SAC_Code']
        #         res['Wash_instructions']=i['Wash_instructions']
        #         res['Product_Category']=i['Product_Category_id']
        #         res['category_image']=image
        #         res['Product_Category_Name']=Product_Category_Name
        #         res['product_sub_category']=i['product_sub_category_id']
        #         res['product_sub_category_name']=product_sub_category_name
        #         res['sub_category_image']=ps_image
        #         # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
        #         # if wishlist:
        #         #     res['wishlist']=True
        #         res['wishlist']=False
        #         # res['wishlist']=i['wishlistss']
        #         # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
        #         # res['color_count']=items
        #         res['attribute_option']=[]
        #
        #         item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
        #         for k in item:
        #             id=k.id
        #
        #             option=AttributeOptions.objects.filter(attributes_id=id)
        #             option_count=AttributeOptions.objects.filter(attributes_id=id).count()
        #             res['color_count']=option_count
        #             for j in option:
        #
        #                 res['attribute_option'].append({
        #                 'option_id':j.id,
        #                 'option':j.option,
        #
        #                 })
        #         Arr.append(res)
        #
        #
        #     return Response(Arr)
        # else:
        #     all_values = Product.objects.filter(Q(Product_Name=value)|Q(Product_Category__Product_Category_Name=value)|Q(product_sub_category__product_sub_category_name=value)|Q(brand__brand_name=value)).values()
        #
        #     for i in all_values:
        #         rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
        #         rating =Reviews.objects.filter(Product_ID_id=i['id'])
        #         if rating_count>0:
        #             for k in rating:
        #                 if k.star_rating!='':
        #
        #                     total_rating=total_rating+int(k.star_rating)
        #                 else:
        #                     total_rating=0
        #             avg=int(total_rating)/int(rating_count)
        #         else:
        #             avg=0
        #         total_rating=0
        #         rating_count=0
        #         brand=Brand.objects.filter(id=i['brand_id'])
        #         for k in brand:
        #             brand_name=k.brand_name
        #         p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
        #         for l in p_category:
        #             Product_Category_Name=l.Product_Category_Name
        #             image=str(l.image)
        #
        #         ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
        #         for m in ps_category:
        #             product_sub_category_name=m.product_sub_category_name
        #             ps_image=str(m.image)
        #
        #         res={}
        #         res['rating']=avg
        #         res['id']=i['id']
        #         res['brand_name']=brand_name
        #         res['brand_id']=i['brand_id']
        #         res['Product_Name']=i['Product_Name']
        #         res['Product_Description']=i['Product_Description']
        #         res['Product_Image']=i['Product_Image']
        #         res['Product_Video']=i['Product_Video']
        #         res['Product_Selling_Price']=i['Product_Selling_Price']
        #         res['Gst']=i['Gst']
        #         res['Product_Listed_Price']=i['Product_Listed_Price']
        #         res['Product_Details']=i['Product_Details']
        #         res['Status']=i['Status']
        #         res['Create_TimeStamp']=i['Create_TimeStamp']
        #         res['HSN_SAC_Code']=i['HSN_SAC_Code']
        #         res['Wash_instructions']=i['Wash_instructions']
        #         res['Product_Category']=i['Product_Category_id']
        #         res['category_image']=image
        #         res['Product_Category_Name']=Product_Category_Name
        #         res['product_sub_category']=i['product_sub_category_id']
        #         res['product_sub_category_name']=product_sub_category_name
        #         res['sub_category_image']=ps_image
        #         # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
        #         # if wishlist:
        #         #     res['wishlist']=True
        #         res['wishlist']=False
        #         # res['wishlist']=i['wishlistss']
        #         # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
        #         # res['color_count']=items
        #         res['attribute_option']=[]
        #
        #         item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
        #         for k in item:
        #             id=k.id
        #
        #             option=AttributeOptions.objects.filter(attributes_id=id)
        #             option_count=AttributeOptions.objects.filter(attributes_id=id).count()
        #             res['color_count']=option_count
        #             for j in option:
        #
        #                 res['attribute_option'].append({
        #                 'option_id':j.id,
        #                 'option':j.option,
        #
        #                 })
        #         Arr.append(res)
        #     return Response(Arr)


#############################User_under_marketerAPIView###########################################

class User_under_marketerAPIView(APIView):
    def get(self, request):
        marketer_id =self.request.query_params.get('marketer_id')
        Arr=[]
        codes=''
        senior_name=''
        role_name=''

        team= Team_Code.objects.filter(team_id=marketer_id)
        for k in team:
            codes=k.ref_code
        userRole_data = Custom_User.objects.filter(referral_code=codes).values()
        for i in userRole_data:
            # if i['referral_code'][-2:-1]=='M':
            code=Team_Code.objects.filter(ref_code=i['referral_code'])
            for j in code:
                senior_name=j.team.name
                # senior_role=j.team.role.user_role_name
            role=UserRoleRef.objects.filter(id=i['role_id'])
            for k in role:
                role_name=k.user_role_name
            res={}
            res['id']=i['id']
            res['user_id']=i['user_id']
            res['username']=i['username']
            res['email']=i['Email_ID']
            res['mobile_number']=i['Mobile_Number']
            res['fullname']=i['Full_Name']
            res['date_of_birth']=i['Date_Of_Birth']
            # res['role_id']=i['role_id']
            # res['role_name']=role_name
            res['location']=i['location']
            res['gender']=i['gender']
            res['alt_number']=i['alt_number']
            res['referral_code']=i['referral_code']
            # res['senior_name']=senior_name
            # res['senior_role']=senior_role
            res['leader']=''
            res['marketer']=senior_name
            res['address']=[]
            # res['city']=[]
            # res['state']=[]
            # res['pincode']=[]
            address1 = User_Address.objects.filter(user_id=i['user_id'])
            for j in address1:
                res['address'].append({
                'address':j.Address,
                'city':j.City,
                'state':j.State,
                'pincode':j.Pincode,
                })
            Arr.append(res)

        return Response(Arr)
    # return Response(userRole_data)


#############################User_under_LeaderAPIView###########################################

class User_under_LeaderAPIView(APIView):
    def get(self, request):
        leader_id =self.request.query_params.get('leader_id')
        Arr=[]
        codes=''
        senior_name=''
        role_name=''
        team= Team_Code.objects.filter(team_id=leader_id)
        for k in team:
            codes=k.ref_code

        userRole_data = Custom_User.objects.filter(referral_code=codes).values()
        for i in userRole_data:
            # if i['referral_code'][-2:-1]=='M':
            code=Team_Code.objects.filter(ref_code=i['referral_code'])
            for j in code:
                senior_name=j.team.name
                # senior_role=j.team.role.user_role_name
            role=UserRoleRef.objects.filter(id=i['role_id'])
            for k in role:
                role_name=k.user_role_name
            res={}
            res['id']=i['id']
            res['user_id']=i['user_id']
            res['username']=i['username']
            res['email']=i['Email_ID']
            res['mobile_number']=i['Mobile_Number']
            res['fullname']=i['Full_Name']
            res['date_of_birth']=i['Date_Of_Birth']
            # res['role_id']=i['role_id']
            # res['role_name']=role_name
            res['location']=i['location']
            res['gender']=i['gender']
            res['alt_number']=i['alt_number']
            res['referral_code']=i['referral_code']
            res['leader']=senior_name
            res['marketer']=''
            # res['senior_role']=senior_role
            res['address']=[]
            # res['city']=[]
            # res['state']=[]
            # res['pincode']=[]
            address1 = User_Address.objects.filter(user_id=i['user_id'])
            for j in address1:
                res['address'].append({
                'address':j.Address,
                'city':j.City,
                'state':j.State,
                'pincode':j.Pincode,
                })
            Arr.append(res)

        return Response(Arr)
    # return Response(userRole_data)
#
# class Team_ConfigAPIView(APIView):
#     def get(self, request):
#         id =self.request.query_params.get('id')
#         Arr=[]
#         if id:
#             enq_data = Team_Config.objects.filter(id=id)
#             for j in enq_data:
#                 Arr.append({
#                 'id':j.id,
#                 'role_id':j.role_id,
#                 'role_name':j.role.user_role_name,
#                 'salary':j.salary,
#                 'bonus':j.bonus,
#                 'incentives':j.incentives,
#
#                 })
#
#             return Response(Arr)
#         else:
#             enq_data = Team_Config.objects.all()
#             for j in enq_data:
#                 Arr.append({
#                 'id':j.id,
#                 'role_id':j.role_id,
#                 'role_name':j.role.user_role_name,
#                 'salary':j.salary,
#                 'bonus':j.bonus,
#                 'incentives':j.incentives,
#
#                 })
#             return Response(Arr)
#
#
#     def post(self,request):
#         data = request.data
#         role_id = data.get('role_id')
#         salary= data.get('salary')
#         bonus= data.get('bonus')
#         incentives= data.get('incentives')
#
#
#
#
#
#         data_create=Team_Config.objects.create(role_id=role_id,
#                                 salary=salary,
#                                 bonus=bonus,
#                                 incentives=incentives)
#
#
#
#         return Response({'result':'Created'})
#
#     def put(self,request,pk):
#         data=request.data
#         role_id = data.get('role_id')
#         salary= data.get('salary')
#         bonus= data.get('bonus')
#         incentives= data.get('incentives')
#
#
#
#         data=Team_Config.objects.filter(id=pk).update(role_id=role_id,
#                                 salary=salary,
#                                 bonus=bonus,
#                                 incentives=incentives)
#
#         return Response({'result':'Updated'})
#
#
#     def delete(self,request,pk):
#         all_values = Team_Config.objects.filter(id=pk).delete()
#         return Response({'result':'Deleted'})
#
#
#

class Get_product_colorApiView(APIView):
    def get(self,request):
        Arr=[]
        new=[]

        all_valuess = Attributes.objects.filter(name="Color")
        for k in all_valuess:
            # att=k.attribute
        # attr=eval(att)
            all_valuesq = AttributeOptions.objects.filter(attributes_id=k.id)
            for i in all_valuesq:
                print(i.id,'iddd')
                print(i.option,'oooooopptionnn')
                Arr.append(
                i.option

                )
            output = []
            for x in Arr:
                if x not in output:
                    output.append(x)

        return Response(output)


class Get_product_sizeApiView(APIView):
    def get(self,request):
        Arr=[]
        new=[]

        all_valuess = Attributes.objects.filter(name="Size")
        for k in all_valuess:
            # att=k.attribute
        # attr=eval(att)
            all_valuesq = AttributeOptions.objects.filter(attributes_id=k.id)
            for i in all_valuesq:
                Arr.append(
                i.option

                )
            output = []
            for x in Arr:
                if x not in output:
                    output.append(x)

        return Response(output)




#############################User_under_LeaderAPIView###########################################

class Marketer_salary_bonous_incentiveAPIView(APIView):
    def get(self, request):
        marketer_id =self.request.query_params.get('marketer_id')
        Arr=[]
        amt=0
        sal=0
        bon=0
        incen=0
        codes=''
        team= Team_Code.objects.filter(team_id=marketer_id)
        for k in team:
            codes=k.ref_code
        userRole_data = Custom_User.objects.filter(referral_code=codes)
        for i in userRole_data:
            id=i.user_id
            print(id,'id')
            order=OrderDetails.objects.filter(user_id=id)
            for k in order:
                ids=k.id
                payment=PaymentDetails.objects.filter(orderdetails_id=ids,status=True)
                for j in payment:
                    amt=amt+int(j.amount)
                    print(amt,'amt')
        role=UserRoleRef.objects.filter(user_role_name="Marketer")
        for k in role:
            sal=int(k.salary)
            bon=int(k.bonus)
            incen=int(k.incentives)

        if amt:
            return Response({'total_sale':amt,
                            '2%of_sale':amt*2/100,
                            'marketer_salary':sal,
                            'marketer_salary_two_perc_commision':sal+(amt*2/100),
                            'marketer_bonus':bon,
                            'marketer_bonus_two_perc_commision':bon+(amt*2/100),
                            'marketer_incentives':incen,
                            'marketer_incentives_two_perc_commision':incen+(amt*2/100)})
        else:
            return Response({'total_sale':amt,
                            '2%of_sale':0,
                            'marketer_salary':sal,
                            'marketer_salary_two_perc_commision':0,
                            'marketer_bonus':bon,
                            'marketer_bonus_two_perc_commision':0,
                            'marketer_incentives':incen,
                            'marketer_incentives_two_perc_commision':0})



class Leader_salary_bonous_incentiveAPIView(APIView):
    def get(self, request):
        leader_id =self.request.query_params.get('leader_id')
        Arr=[]
        amt=0
        sal=0
        bon=0
        incen=0
        codes=''
        team= Team_Code.objects.filter(team_id=leader_id)
        for k in team:
            codes=k.ref_code
        userRole_data = Custom_User.objects.filter(referral_code=codes)
        for i in userRole_data:
            id=i.user_id
            print(id,'id')
            order=OrderDetails.objects.filter(user_id=id)
            for k in order:
                ids=k.id
                payment=PaymentDetails.objects.filter(orderdetails_id=ids,status=True)
                for j in payment:
                    amt=amt+int(j.amount)
                    print(amt,'amt')
        role=UserRoleRef.objects.filter(user_role_name="Leader")
        for k in role:
            sal=int(k.salary)
            bon=int(k.bonus)
            incen=int(k.incentives)
        if amt:
            return Response({'total_sale':amt,
                            '2%of_sale':amt*2/100,
                            'leader_salary':sal,
                            'leader_salary_two_perc_commision':sal+(amt*2/100),
                            'leader_bonus':bon,
                            'leader_bonus_two_perc_commision':bon+(amt*2/100),
                            'leader_incentives':incen,
                            'leader_incentives_two_perc_commision':incen+(amt*2/100)})
        else:
            return Response({'total_sale':amt,
                            '2%of_sale':0,
                            'leader_salary':sal,
                            'leader_salary_two_perc_commision':0,
                            'leader_bonus':bon,
                            'leader_bonus_two_perc_commision':0,
                            'leader_incentives':incen,
                            'leader_incentives_two_perc_commision':0})



class Profile_imgAPIView(APIView):
    def get(self,request):
        user_id =self.request.query_params.get('user_id')
        if user_id:
            all_values = Custom_user_profile.objects.filter(user_id=user_id).values()
            return Response(all_values)


    def post(self,request):
        data = request.data
        user_id = data.get('user_id')
        profile_img=data.get('profile_img')

        profile=Custom_user_profile.objects.filter(user_id=user_id)
        if profile:
            create_create=Custom_user_profile.objects.filter(user_id=user_id).delete()
            count=str(random.randint(100,9999999))
            split_base_url_data = profile_img.split(';base64,')[1]
            imgdata1 = base64.b64decode(split_base_url_data)
            filename1 = '/kri8eve/site/public/media/profile_img/'+count+'.png'
            fname1 = '/media/profile_img/'+count+'.png'
            ss=  open(filename1, 'wb')
            ss.write(imgdata1)
            ss.close()



            create_create=Custom_user_profile.objects.create(user_id=user_id,profile_img=fname1)

            return JsonResponse({'result':'Created'})

        else:
            count=str(random.randint(100,9999999))
            split_base_url_data = profile_img.split(';base64,')[1]
            imgdata1 = base64.b64decode(split_base_url_data)
            filename1 = '/kri8eve/site/public/media/profile_img/'+count+'.png'
            fname1 = '/media/profile_img/'+count+'.png'
            ss=  open(filename1, 'wb')
            ss.write(imgdata1)
            ss.close()



            create_create=Custom_user_profile.objects.create(user_id=user_id,profile_img=fname1)

            return JsonResponse({'result':'Created'})



class Unique_Attribute_NameApi(APIView):
    def get(self,request):
        Arr=[]
        test1 = Master_Attributes.objects.all()
        for i in test1:
            Arr.append({
            'name':i.name,
            })
        output = []
        for x in Arr:
            if x not in output:
                output.append(x)

        return Response(output)


class Name_wise_attribute_optionApi(APIView):
    def get(self,request):
        name =self.request.query_params.get('name')
        Arr=[]
        test1 = Master_Attributes.objects.filter(name=name)
        for i in test1:
            options=Master_AttributeOptions.objects.filter(attributes_id=i.id)
            for k in options:
                Arr.append({
                'option':k.option,
                })
        output = []
        for x in Arr:
            if x not in output:
                output.append(x)

        return Response(output)


class Newly_added_productApi(APIView):
    def get(self,request):
        Arr=[]

        dis_percent=0

        today = datetime.date.today()
        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
        if discount:
            all_values = Product.objects.all().order_by('-id')[:6]
            for i in all_values:

                dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                for b in dis:
                    dis_percent=dis_percent+int(b.Discount_Percentage)
                after_discount=float(i.Product_Selling_Price)*dis_percent/100
                f_price=float(i.Product_Selling_Price)-after_discount
                dis_percent=0
                Arr.append({
                 'id':i.id,
                'Product_Name':i.Product_Name,
                'Product_Description':i.Product_Description,
                'Product_Selling_Price':f_price,
                'Product_Image':str(i.Product_Image)

                    })
            return Response(Arr)
                # brand=Brand.objects.filter(id=i['brand_id'])
                # for k in brand:
                #     brand_name=k.brand_name
                # p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                # for l in p_category:
                #     Product_Category_Name=l.Product_Category_Name
                #     image=str(l.image)
                #
                # ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                # for m in ps_category:
                #     product_sub_category_name=m.product_sub_category_name
                #     ps_image=str(m.image)

                # res={}
                # res['rating']=avg
                # res['id']=i['id']
                # res['brand_name']=brand_name
                # res['brand_id']=i['brand_id']
                # res['Product_Name']=i['Product_Name']
                # res['Product_Description']=i['Product_Description']
                # res['Product_Image']=i['Product_Image']
                # res['Product_Video']=i['Product_Video']
                # res['Product_Selling_Price']=f_price
                # res['Gst']=i['Gst']
                # res['Product_Listed_Price']=i['Product_Listed_Price']
                # res['Product_Details']=i['Product_Details']
                # res['Status']=i['Status']
                # res['Create_TimeStamp']=i['Create_TimeStamp']
                # res['HSN_SAC_Code']=i['HSN_SAC_Code']
                # res['Wash_instructions']=i['Wash_instructions']
                # res['Product_Category']=i['Product_Category_id']
                # res['category_image']=image
                # res['Product_Category_Name']=Product_Category_Name
                # res['product_sub_category']=i['product_sub_category_id']
                # res['product_sub_category_name']=product_sub_category_name
                # res['sub_category_image']=ps_image
                # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                # if wishlist:
                #     res['wishlist']=True
                # res['wishlist']=False
                # res['wishlist']=i['wishlistss']
                # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                # res['color_count']=items
                # res['attribute_option']=[]

                # item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                # for k in item:
                #     id=k.id
                #
                #     option=AttributeOptions.objects.filter(attributes_id=id)
                #     option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                #     res['color_count']=option_count
                #     for j in option:
                #
                #         res['attribute_option'].append({
                #         'option_id':j.id,
                #         'option':j.option,
                #
                #         })
                # Arr.append(res)
                #

            # return Response(res)
        else:
            all_values = Product.objects.all().order_by('-id')[:6]
            for i in all_values:
                 Arr.append({
                 'id':i.id,
                'Product_Name':i.Product_Name,
                'Product_Description':i.Product_Description,
                'Product_Selling_Price':i.Product_Selling_Price,
                'Product_Image':str(i.Product_Image)

                    })
            return Response(Arr)
                # rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                # rating =Reviews.objects.filter(Product_ID_id=i['id'])
                # if rating_count>0:
                #     for k in rating:
                #         if k.star_rating!='':
                #
                #             total_rating=total_rating+int(k.star_rating)
                #         else:
                #             total_rating=0
                #     avg=int(total_rating)/int(rating_count)
                # else:
                #     avg=0
                # total_rating=0
                # rating_count=0
                # brand=Brand.objects.filter(id=i['brand_id'])
                # for k in brand:
                #     brand_name=k.brand_name
                # p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                # for l in p_category:
                #     Product_Category_Name=l.Product_Category_Name
                #     image=str(l.image)
                #
                # ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                # for m in ps_category:
                #     product_sub_category_name=m.product_sub_category_name
                #     ps_image=str(m.image)

                # res={}
                # res['rating']=avg
                # res['id']=i['id']
                # res['brand_name']=brand_name
                # res['brand_id']=i['brand_id']
                # res['Product_Name']=i['Product_Name']
                # res['Product_Description']=i['Product_Description']
                # res['Product_Image']=i['Product_Image']
                # res['Product_Video']=i['Product_Video']
                # res['Product_Selling_Price']=i['Product_Selling_Price']
                # res['Gst']=i['Gst']
                # res['Product_Listed_Price']=i['Product_Listed_Price']
                # res['Product_Details']=i['Product_Details']
                # res['Status']=i['Status']
                # res['Create_TimeStamp']=i['Create_TimeStamp']
                # res['HSN_SAC_Code']=i['HSN_SAC_Code']
                # res['Wash_instructions']=i['Wash_instructions']
                # res['Product_Category']=i['Product_Category_id']
                # res['category_image']=image
                # res['Product_Category_Name']=Product_Category_Name
                # res['product_sub_category']=i['product_sub_category_id']
                # res['product_sub_category_name']=product_sub_category_name
                # res['sub_category_image']=ps_image
                # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                # if wishlist:
                #     res['wishlist']=True
                # res['wishlist']=False
                # res['wishlist']=i['wishlistss']
                # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                # res['color_count']=items
                # res['attribute_option']=[]
                #
                # item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                # for k in item:
                #     id=k.id
                #
                #     option=AttributeOptions.objects.filter(attributes_id=id)
                #     option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                #     res['color_count']=option_count
                #     for j in option:
                #
                #         res['attribute_option'].append({
                #         'option_id':j.id,
                #         'option':j.option,
                #
                #         })
                # Arr.append(res)
            # return Response(res)


class Trending_productApi(APIView):
    def get(self,request):
        Arr=[]
        # Arrs=[]
        # opt=[]
        # image=''
        dis_percent=0
        # Product_Category_Name=''
        # product_sub_category_name=''
        # ps_image=''
        today = datetime.date.today()
        discount=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
        if discount:
            all_values = Product.objects.all().order_by('-count_sold')[:6]
            for i in all_values:
                # rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                # rating =Reviews.objects.filter(Product_ID_id=i['id'])
                # if rating_count>0:
                #     for k in rating:
                #         if k.star_rating!='':
                #
                #             total_rating=total_rating+int(k.star_rating)
                #         else:
                #             total_rating=0
                #     avg=int(total_rating)/int(rating_count)
                # else:
                #     avg=0
                # total_rating=0
                # rating_count=0
                dis=Discount.objects.filter(Q(start_date__lte=today)&Q(end_date__gte=today)&Q(Status='Active'))
                for b in dis:
                    dis_percent=dis_percent+int(b.Discount_Percentage)
                after_discount=float(i.Product_Selling_Price)*dis_percent/100
                f_price=float(i.Product_Selling_Price)-after_discount
                dis_percent=0
                Arr.append({
                 'id':i.id,
                'Product_Name':i.Product_Name,
                'Product_Description':i.Product_Description,
                'Product_Selling_Price':f_price,
                'Product_Image':str(i.Product_Image),
                'count_sold':i.count_sold,
                # 'brand_name':i.brand.brand_name


                    })
            return Response(Arr)
                # brand=Brand.objects.filter(id=i['brand_id'])
                # for k in brand:
                #     brand_name=k.brand_name
                # p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                # for l in p_category:
                #     Product_Category_Name=l.Product_Category_Name
                #     image=str(l.image)
                #
                # ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                # for m in ps_category:
                #     product_sub_category_name=m.product_sub_category_name
                #     ps_image=str(m.image)

                # res={}
                # res['rating']=avg
                # res['id']=i['id']
                # res['brand_name']=brand_name
                # res['brand_id']=i['brand_id']
                # res['Product_Name']=i['Product_Name']
                # res['Product_Description']=i['Product_Description']
                # res['Product_Image']=i['Product_Image']
                # res['Product_Video']=i['Product_Video']
                # res['Product_Selling_Price']=f_price
                # res['Gst']=i['Gst']
                # res['Product_Listed_Price']=i['Product_Listed_Price']
                # res['Product_Details']=i['Product_Details']
                # res['Status']=i['Status']
                # res['Create_TimeStamp']=i['Create_TimeStamp']
                # res['HSN_SAC_Code']=i['HSN_SAC_Code']
                # res['Wash_instructions']=i['Wash_instructions']
                # res['Product_Category']=i['Product_Category_id']
                # res['category_image']=image
                # res['Product_Category_Name']=Product_Category_Name
                # res['product_sub_category']=i['product_sub_category_id']
                # res['product_sub_category_name']=product_sub_category_name
                # res['sub_category_image']=ps_image
                # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                # if wishlist:
                #     res['wishlist']=True
                # res['wishlist']=False
                # res['wishlist']=i['wishlistss']
                # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                # res['color_count']=items
                # res['attribute_option']=[]

                # item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                # for k in item:
                #     id=k.id
                #
                #     option=AttributeOptions.objects.filter(attributes_id=id)
                #     option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                #     res['color_count']=option_count
                #     for j in option:
                #
                #         res['attribute_option'].append({
                #         'option_id':j.id,
                #         'option':j.option,
                #
                #         })
                # Arr.append(res)
                #

            # return Response(res)
        else:
            all_values = Product.objects.all().order_by('-count_sold')[:6]
            for i in all_values:
                 Arr.append({
                 'id':i.id,
                'Product_Name':i.Product_Name,
                'Product_Description':i.Product_Description,
                'Product_Selling_Price':i.Product_Selling_Price,
                'Product_Image':str(i.Product_Image),
                'count_sold':i.count_sold,
                'brand_name':i.brand.brand_name



                    })
            return Response(Arr)
                # rating_count =Reviews.objects.filter(Product_ID_id=i['id']).count()
                # rating =Reviews.objects.filter(Product_ID_id=i['id'])
                # if rating_count>0:
                #     for k in rating:
                #         if k.star_rating!='':
                #
                #             total_rating=total_rating+int(k.star_rating)
                #         else:
                #             total_rating=0
                #     avg=int(total_rating)/int(rating_count)
                # else:
                #     avg=0
                # total_rating=0
                # rating_count=0
                # brand=Brand.objects.filter(id=i['brand_id'])
                # for k in brand:
                #     brand_name=k.brand_name
                # p_category=Product_Category.objects.filter(id=i['Product_Category_id'])
                # for l in p_category:
                #     Product_Category_Name=l.Product_Category_Name
                #     image=str(l.image)
                #
                # ps_category=Product_Sub_Category.objects.filter(id=i['product_sub_category_id'])
                # for m in ps_category:
                #     product_sub_category_name=m.product_sub_category_name
                #     ps_image=str(m.image)

                # res={}
                # res['rating']=avg
                # res['id']=i['id']
                # res['brand_name']=brand_name
                # res['brand_id']=i['brand_id']
                # res['Product_Name']=i['Product_Name']
                # res['Product_Description']=i['Product_Description']
                # res['Product_Image']=i['Product_Image']
                # res['Product_Video']=i['Product_Video']
                # res['Product_Selling_Price']=i['Product_Selling_Price']
                # res['Gst']=i['Gst']
                # res['Product_Listed_Price']=i['Product_Listed_Price']
                # res['Product_Details']=i['Product_Details']
                # res['Status']=i['Status']
                # res['Create_TimeStamp']=i['Create_TimeStamp']
                # res['HSN_SAC_Code']=i['HSN_SAC_Code']
                # res['Wash_instructions']=i['Wash_instructions']
                # res['Product_Category']=i['Product_Category_id']
                # res['category_image']=image
                # res['Product_Category_Name']=Product_Category_Name
                # res['product_sub_category']=i['product_sub_category_id']
                # res['product_sub_category_name']=product_sub_category_name
                # res['sub_category_image']=ps_image
                # wishlist=Wishlist.objects.filter(user_id=user_id,product_id=i['id'])
                # if wishlist:
                #     res['wishlist']=True
                # res['wishlist']=False
                # res['wishlist']=i['wishlistss']
                # items=Attributes.objects.filter(Product_ID_id=i['id'],name='Color').count()
                # res['color_count']=items
                # res['attribute_option']=[]
                #
                # item=Attributes.objects.filter(Product_ID_id=i['id'],name='Color')
                # for k in item:
                #     id=k.id
                #
                #     option=AttributeOptions.objects.filter(attributes_id=id)
                #     option_count=AttributeOptions.objects.filter(attributes_id=id).count()
                #     res['color_count']=option_count
                #     for j in option:
                #
                #         res['attribute_option'].append({
                #         'option_id':j.id,
                #         'option':j.option,
                #
                #         })
                # Arr.append(res)
            # return Response(res)



class Get_Assign_product_for_delivery_boyApis(APIView):
    def get(self,request):
        delivery_boy_id =self.request.query_params.get('delivery_boy_id')
        Arr=[]
        address=''
        city=''
        state=''
        street=''
        locationname=''
        pincode=''
        delivery_charges=''

        option=[]
        id=kri8evTeam.objects.get(user_id=delivery_boy_id)
        tests = OrderDetails.objects.filter(delivery_boy_id=id.id).values()
        for i in tests:
            payment=PaymentDetails.objects.filter(orderdetails_id=i['id'],status=True)
            if payment:
                username=User.objects.get(id=i['user_id'])
                c_user=Custom_User.objects.get(user_id=i['user_id'])


                shipping=ShippingCharges.objects.filter(id=i['shippingcharges_id'])
                for k in shipping:
                    locationname=k.locationname
                    pincode=k.pincode
                    delivery_charges  =k.amount

                address=User_Address.objects.filter(user_id=i['user_id'],delfault_address=True)
                for j in address:
                    address=j.Address
                    city=j.City
                    state=j.State
                    street=j.street
                res={}
                res['id']=i['id']
                res['user_id']=i['user_id']
                res['delivery_status']=i['delivery_status']
                res['username']=username.username
                res['fullname']=username.first_name
                res['mobile_number']=c_user.Mobile_Number
                res['alt_number']=c_user.alt_number
                res['total']=int(float(i['total']))
                res['locationname']=locationname
                res['pincode']=pincode
                res['delivery_charges']=delivery_charges
                res['address']=address
                res['city']=city
                res['state']=state
                res['street']=street
                res['product_details']=[]
                item=OrderItems.objects.filter(OrderDetails_id=i['id'])

                for l in item:

                    res['product_details'].append({
                    'product_name':l.Product_ID.Product_Name,
                    'quantity':l.quantity,
                    'product_image':str(l.Product_ID.Product_Image),
                    'size':l.size,
                    'color':l.color
                    })
                Arr.append(res)
        return Response(Arr)


class Get_SalesAPIView(APIView):
    def get(self, request):
        category_id =self.request.query_params.get('category_id')

        Arr=[]
        quant=[]
        amt=0
        new_count=0
        tests = OrderDetails.objects.all()
        for i in tests:
            payment=PaymentDetails.objects.filter(orderdetails_id=i.id,status=True)
            if payment:
                amt=amt+int(float(i.total))

        pro_cate=Product_Category.objects.filter(id=category_id).values()
        for j in pro_cate:
            res={}
            res['category_id']=j['id']
            res['category_name']=j['Product_Category_Name']
            res['details']=[]

            pro=Product.objects.filter(Product_Category_id=j['id'])
            for k in pro:

                item_data = OrderItems.objects.filter(Product_ID_id=k.id)
                if item_data:
                    quant=0
                    for i in item_data:
                        quant=quant+int(i.quantity)
                        product_id=i.Product_ID.id
                        product_name=i.Product_ID.Product_Name
                        product_image=str(i.Product_ID.Product_Image)
                        product_selling_price=i.Product_ID.Product_Selling_Price
                    res['details'].append({
                    'product_id':product_id,
                    'product_name':product_name,
                    'product_image':product_image,
                    'product_selling_price':product_selling_price,
                    'sale_qty':quant

                    })
                    new_count=new_count+quant

                else:
                    continue
            res['total_sale_qty']=new_count
            Arr.append(res)
        return Response({'data':Arr,'total_sale':amt})



class Get_Marketer_sales_DetailsApis(APIView):
    def get(self,request):
        marketer_id =self.request.query_params.get('marketer_id')
        Arr=[]
        value=0
        amt=0

        tests = OrderDetails.objects.all()
        for i in tests:
            payment=PaymentDetails.objects.filter(orderdetails_id=i.id,status=True)
            if payment:
                amt=amt+int(float(i.total))
        if marketer_id:
            details=User.objects.get(id=marketer_id)
            team=kri8evTeam.objects.get(user_id=marketer_id)
            res={}
            value=0
            res['marketer_id']=details.id
            res['marketer_username']=details.username
            res['marketer_name']=details.first_name
            res['marketer_email']=team.email
            res['marketer_mobile_no']=team.mobile_number
            res['details']=[]
            saless=Marketer_sales.objects.filter(marketer_id=marketer_id)
            for r in saless:
                value=value+int(float(r.orders.total))
            res['marketer_sales_amt']=value
            sales=Marketer_sales.objects.filter(marketer_id=marketer_id)
            for i in sales:
                value=value+int(float(i.orders.total))
                res['details'].append({

                'order_id':i.orders_id,
                'code':i.code,
                'sales':int(float(i.orders.total)),
                'date':i.create_timestamp
                })
            Arr.append(res)
            return Response({'total_sale_amount':amt,'data':Arr})
        else:
            username=''
            marketer_name=''

            details=kri8evTeam.objects.filter(role__user_role_name='Marketer').values()
            print(details,'ddddd')
            for j in details:
                user=User.objects.filter(id=j['user_id'])
                for k in user:
                    team=kri8evTeam.objects.get(user_id=k.id)
                    marketer_email=team.email
                    marketer_mobile_no=team.mobile_number

                    username=k.username
                    marketer_name=k.first_name
                res={}
                value=0
                res['marketer_id']=j['user_id']
                res['marketer_username']=username
                res['marketer_name']=marketer_name
                res['marketer_email']=marketer_email
                res['marketer_mobile_no']=marketer_mobile_no
                res['details']=[]
                saless=Marketer_sales.objects.filter(marketer_id=j['user_id'])
                for r in saless:
                    value=value+int(float(r.orders.total))
                res['marketer_sales_amt']=value

                sales=Marketer_sales.objects.filter(marketer_id=j['user_id'])
                for i in sales:
                    value=value+int(float(i.orders.total))
                    res['details'].append({

                    'order_id':i.orders_id,
                    'code':i.code,
                    'sales':int(float(i.orders.total)),
                    'date':i.create_timestamp
                    })
                Arr.append(res)
            return Response({'total_sale_amount':amt,'data':Arr})



class Get_date_wise_marketer_sales_detailsApis(APIView):
    def get(self,request):
        marketer_id =self.request.query_params.get('marketer_id')
        sales_date =self.request.query_params.get('sales_date')
        Arr=[]
        value=0
        salary=0

        details=User.objects.get(id=marketer_id)
        res={}
        res['marketer_id']=details.id
        res['marketer_username']=details.username
        res['marketer_name']=details.first_name
        res['details']=[]

        sales=Marketer_sales.objects.filter(Q(marketer_id=marketer_id)&Q(create_timestamp=sales_date))
        for i in sales:
            value=value+int(float(i.orders.total))
            res['details'].append({
            'marketer_id':details.id,
            'marketer_username':details.username,
            'marketer_name':details.first_name,
            'order_id':i.orders_id,
            'code':i.code,
            'sales':int(float(i.orders.total)),
            'date':i.create_timestamp
            })
        Arr.append(res)

        if value<5000:
            salary=value*5/100
        elif value==5000:
            salary=value*10/100
        elif value>=5001 and value<=10000:
            salary=5000*10/100
            new_value=value-5000
            amt=new_value*2/100
            salary=salary+amt

        elif value>=10001 and value<=15000:
            salary=5000*10/100
            salary=salary+5000*2/100
            new_value=value-5000
            new_value1=new_value-5000
            amt=new_value1*3/100
            salary=salary+amt

        elif value>=15001 and value<=20000:
            salary=5000*10/100
            salary=salary+5000*2/100
            salary=salary+5000*3/100
            new_value=value-15000
            salary=salary+new_value*4/100

        elif value>=20001:
            salary=5000*10/100
            salary=salary+5000*2/100
            salary=salary+5000*3/100
            salary=salary+5000*4/100
            new_value=value-20000
            salary=salary+new_value*5/100

        # if salary_update=Marketer_salary.objects.filter(marketer_id=marketer_id).exists():
        #     salary_update=Marketer_salary.objects.filter(marketer_id=marketer_id).update(salary=salary)
        # else:

        return Response({'date':sales_date,'total_sale_amount':value,'salary':salary,'data':Arr})



class Get_month_wise_marketer_sales_detailsApis(APIView):
    def post(self,request):
        data = request.data
        marketer_id = data.get('marketer_id')
        fdate=data.get('fdate')
        tdate=data.get('tdate')


        Arr=[]
        value=0
        salary=0

        details=User.objects.get(id=marketer_id)
        res={}
        res['marketer_id']=details.id
        res['marketer_username']=details.username
        res['marketer_name']=details.first_name
        res['details']=[]

        sales=Marketer_sales.objects.filter(Q(marketer_id=marketer_id)&Q(create_timestamp__gte=fdate,create_timestamp__lte=tdate))
        for i in sales:
            value=value+int(float(i.orders.total))
            res['details'].append({
            'marketer_id':details.id,
            'marketer_username':details.username,
            'marketer_name':details.first_name,
            'order_id':i.orders_id,
            'code':i.code,
            'sales':int(float(i.orders.total)),
            'date':i.create_timestamp
            })
        Arr.append(res)

        if value<5000:
            salary=value*5/100
        elif value==5000:
            salary=value*10/100
        elif value>=5001 and value<=10000:
            salary=5000*10/100
            new_value=value-5000
            amt=new_value*2/100
            salary=salary+amt

        elif value>=10001 and value<=15000:
            salary=5000*10/100
            salary=salary+5000*2/100
            new_value=value-5000
            new_value1=new_value-5000
            amt=new_value1*3/100
            salary=salary+amt

        elif value>=15001 and value<=20000:
            salary=5000*10/100
            salary=salary+5000*2/100
            salary=salary+5000*3/100
            new_value=value-15000
            salary=salary+new_value*4/100

        elif value>=20001:
            salary=5000*10/100
            salary=salary+5000*2/100
            salary=salary+5000*3/100
            salary=salary+5000*4/100
            new_value=value-20000
            salary=salary+new_value*5/100

        # if salary_update=Marketer_salary.objects.filter(marketer_id=marketer_id).exists():
        #     salary_update=Marketer_salary.objects.filter(marketer_id=marketer_id).update(salary=salary)
        # else:
        # return Response({'date':sales_date,'total_sale_amount':value,'salary':salary,'data':Arr})
        return Response({'total_sale_amount':value,'salary':salary,'data':Arr,'fdate':str(fdate) ,'tdate':str(tdate)})


class get_Product_wise_category(APIView):
    def get(self,request):
        category_id =self.request.query_params.get('category_id')
        Arr=[]
        product=Product.objects.filter(Product_Category_id=category_id)
        for i in product:
            Arr.append({
            'id':i.id,
            'product_name':i.Product_Name
            })
        return Response(Arr)


class get_all_Delivery_boy(APIView):
    def get(self,request):
        Arr=[]
        product=kri8evTeam.objects.filter(role__user_role_name='Delivery Boy')
        for i in product:
            Arr.append({
            'id':i.id,
            'delivery_boy_name':i.name,
            'user_id':i.user_id
            })
        return Response(Arr)



class DashboardAPIView(APIView):
    def get(self,request):
        amt=0
        total_no_reg_user=Custom_User.objects.all().count()
        total_no_of_order=PaymentDetails.objects.filter(status=True).count()

        tests = OrderDetails.objects.all()
        for i in tests:
            payment=PaymentDetails.objects.filter(orderdetails_id=i.id,status=True)
            if payment:
                amt=amt+int(float(i.total))


        return Response({'total_no_reg_user':total_no_reg_user,'total_no_of_order':total_no_of_order,'total_sale_amt':amt})



class Validate_mobileAPIView(APIView):
    def post(self,request):
        data=request.data
        mobile_number=data.get('mobile_number')

        user=User.objects.filter(last_name=mobile_number)
        c_user=Custom_User.objects.filter(Mobile_Number=mobile_number)
        if user and c_user:
            header_response = {}
            response['error'] = {'error': {
                'detail': 'Mobile number already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)


class Validate_emailAPIView(APIView):
    def post(self,request):
        data=request.data
        email=data.get('email')

        user=User.objects.filter(email=email)
        c_user=Custom_User.objects.filter(Email_ID=email)
        if user and c_user:
            header_response = {}
            response['error'] = {'error': {
                'detail': 'Email already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)


def reg_otp_send():
    otpsss= random.randint(100000, 999999)
    return otpsss
forgotpass_otps=0


class Reg_otp(APIView):

    def post(self, request):
        data = request.data
        response = {}

        username = data.get('username')
        Mobile_Number = data.get('Mobile_Number')

        if User.objects.filter(Q(username=username) | Q(email=username)|Q(last_name=Mobile_Number)).exists():
            header_response = {}
            response['error'] = {'error': {
                'detail': 'Email or Mobile number already exist!', 'status': status.HTTP_401_UNAUTHORIZED}}

            return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)

        else:
            val=otp_send()
            global forgotpass_otps
            forgotpass_otps=val
            if username:

                message = inspect.cleandoc('''Hi,\n%s is your OTP to register your Kri8ev account.\nThis OTP is valid for next 10 minutes,
                                      \nWith Warm Regards,\nTeam Kri8ev,
                                       ''' % (val))
                send_mail(
                    'Kri8ev One Time Password (OTP) to Register', message
                    ,
                    'info.aceventures18@gmail.com',
                    [username],

                )
                data_dict = {}
                data_dict["Otp"] = val
                return JsonResponse(data_dict, safe=False)
            else:
                # otpp=str(otp)
                # url = "https://api.kaleyra.io/v1/HXIN1712667009IN/messages"
                #
                # # payload='to='+username+'&sender=SPTLYT&type=OTP&body=%22Hi%2C%20%7B%23var%23%7D%20is%20your%20OTP%20to%20login%20to%20your%20Spotlyt%20account.%20This%20OTP%20is%20valid%20for%20next%20%7B%23var%23%7D%20minutes.%20Regards%2C%20Team%20Spotlyt%20Academy%22&template_id=1207163394371203510'
                # payload='to=91 '+username+'&sender=SPTLYT&type=OTP&body=%22Hi%2C%20'+otpp+'%20is%20your%20OTP%20to%20login%20to%20your%20Spotlyt%20account.%20This%20OTP%20is%20valid%20for%20next%2010%20minutes.%20Regards%2C%20Team%20Spotlyt%20Academy%22'
                # headers = {
                #   'Content-Type': 'application/x-www-form-urlencoded',
                #   'api-key': 'Aa2eaa09645326f99dee7d298de3406d1'
                # }

                # response = requests.request("POST", url, headers=headers, data=payload)
                response="Message Send Successfully"
                return Response(response, status=status.HTTP_200_OK)
                # return Response('Message Send Successfully')

###############################OTP VERIFICATION_signup###################################

class OTP_Verification_signupAPIView(APIView):


    def post(self, request):
        data = request.data
        otp = data.get('otp')
        # print(new_otp,'ori')
        if otp:
            if int(otp)==int(forgotpass_otps):
                response="OTP matcheds successfully"
                return Response(response, status=status.HTTP_200_OK)
                # return JsonResponse({'message': 'OTP matcheds successfully'})
            else:
                response="Invalid OTP"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
                # return JsonResponse({'message': 'Invalid OTP'})
        else:
            response=" OTP required"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class Get_Marketer_sale_graph(APIView):
    def get(self,request):
        user_id = self.request.query_params.get('user_id')
        search=self.request.query_params.get('search')
        Arr=[]
        jan_sale_amt=0
        feb_sale_amt=0
        mar_sale_amt=0
        apr_sale_amt=0
        may_sale_amt=0
        jun_sale_amt=0
        jul_sale_amt=0
        aug_sale_amt=0
        sep_sale_amt=0
        oct_sale_amt=0
        nov_sale_amt=0
        dec_sale_amt=0

        day1_sale_amt=0
        day2_sale_amt=0
        day3_sale_amt=0
        day4_sale_amt=0
        day5_sale_amt=0
        day6_sale_amt=0

        day7_sale_amt=0
        day8_sale_amt=0
        day9_sale_amt=0
        day10_sale_amt=0
        day11_sale_amt=0
        day12_sale_amt=0

        day13_sale_amt=0
        day14_sale_amt=0
        day15_sale_amt=0
        day16_sale_amt=0
        day17_sale_amt=0
        day18_sale_amt=0

        day19_sale_amt=0
        day20_sale_amt=0
        day21_sale_amt=0
        day22_sale_amt=0
        day23_sale_amt=0
        day24_sale_amt=0

        day25_sale_amt=0
        day26_sale_amt=0
        day27_sale_amt=0
        day28_sale_amt=0
        day29_sale_amt=0
        day30_sale_amt=0
        day31_sale_amt=0
        if user_id:
            current_month=date.today().month
            current_year=date.today().year


            if search=='year_wise':
                sale_amt1=0
                sale_amt2=0
                sale_amt3=0
                kri8evTeam_data = kri8evTeam.objects.filter(created_by=user_id)
                for j in kri8evTeam_data:



                    order_details=Marketer_sales.objects.filter(marketer_id=j.user_id,create_timestamp__year=current_year-2)
                    for i in order_details:
                        sale_amt1=sale_amt1+int(float(i.sale_amt))
                    order_details=Marketer_sales.objects.filter(marketer_id=j.user_id,create_timestamp__year=current_year-1)
                    for i in order_details:
                        sale_amt2=sale_amt2+int(float(i.sale_amt))
                    order_details=Marketer_sales.objects.filter(marketer_id=j.user_id,create_timestamp__year=current_year)
                    for i in order_details:
                        sale_amt3=sale_amt3+int(float(i.sale_amt))
                return Response({'data':{'2020 Sales':sale_amt1,
                '2021 Sales':sale_amt2,
                '2022 Sales':sale_amt3,},'name':'Yearly Sales'})


            if search=='month_wise':

                kri8evTeam_data = kri8evTeam.objects.filter(created_by=user_id)
                for i in kri8evTeam_data:
                    print(i.user_id,'ussss')
                    if current_month==1:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))





                    if current_month==2:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))



                    if current_month==3:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))


                    if current_month==4:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))




                    if current_month==5:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))



                    if current_month==6:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                    if current_month==7:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                        jul_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=7,create_timestamp__year=current_year)
                        for jul in jul_order_details:
                            jul_sale_amt=jul_sale_amt+int(float(jul.sale_amt))




                    if current_month==8:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                        jul_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=7,create_timestamp__year=current_year)
                        for jul in jul_order_details:
                            jul_sale_amt=jul_sale_amt+int(float(jul.sale_amt))

                        aug_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=8,create_timestamp__year=current_year)
                        for aug in aug_order_details:
                            aug_sale_amt=aug_sale_amt+int(float(aug.sale_amt))



                    if current_month==9:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                        jul_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=7,create_timestamp__year=current_year)
                        for jul in jul_order_details:
                            jul_sale_amt=jul_sale_amt+int(float(jul.sale_amt))

                        aug_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=8,create_timestamp__year=current_year)
                        for aug in aug_order_details:
                            aug_sale_amt=aug_sale_amt+int(float(aug.sale_amt))

                        sep_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=9,create_timestamp__year=current_year)
                        for sep in sep_order_details:
                            sep_sale_amt=sep_sale_amt+int(float(sep.sale_amt))




                    if current_month==10:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                        jul_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=7,create_timestamp__year=current_year)
                        for jul in jul_order_details:
                            jul_sale_amt=jul_sale_amt+int(float(jul.sale_amt))

                        aug_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=8,create_timestamp__year=current_year)
                        for aug in aug_order_details:
                            aug_sale_amt=aug_sale_amt+int(float(aug.sale_amt))

                        sep_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=9,create_timestamp__year=current_year)
                        for sep in sep_order_details:
                            sep_sale_amt=sep_sale_amt+int(float(sep.sale_amt))

                        oct_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=10,create_timestamp__year=current_year)
                        for oct in oct_order_details:
                            oct_sale_amt=oct_sale_amt+int(float(oct.sale_amt))




                    if current_month==11:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                        jul_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=7,create_timestamp__year=current_year)
                        for jul in jul_order_details:
                            jul_sale_amt=jul_sale_amt+int(float(jul.sale_amt))

                        aug_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=8,create_timestamp__year=current_year)
                        for aug in aug_order_details:
                            aug_sale_amt=aug_sale_amt+int(float(aug.sale_amt))

                        sep_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=9,create_timestamp__year=current_year)
                        for sep in sep_order_details:
                            sep_sale_amt=sep_sale_amt+int(float(sep.sale_amt))

                        oct_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=10,create_timestamp__year=current_year)
                        for oct in oct_order_details:
                            oct_sale_amt=oct_sale_amt+int(float(oct.sale_amt))

                        nov_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=11,create_timestamp__year=current_year)
                        for nov in nov_order_details:
                            nov_sale_amt=nov_sale_amt+int(float(nov.sale_amt))




                    if current_month==12:
                        jan_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=1,create_timestamp__year=current_year)
                        for jan in jan_order_details:
                            jan_sale_amt=jan_sale_amt+int(float(jan.sale_amt))

                        feb_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=2,create_timestamp__year=current_year)
                        for feb in feb_order_details:
                            feb_sale_amt=feb_sale_amt+int(float(feb.sale_amt))

                        mar_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=3,create_timestamp__year=current_year)
                        for mar in mar_order_details:
                            mar_sale_amt=mar_sale_amt+int(float(mar.sale_amt))

                        apr_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=4,create_timestamp__year=current_year)
                        for apr in apr_order_details:
                            apr_sale_amt=apr_sale_amt+int(float(apr.sale_amt))

                        may_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=5,create_timestamp__year=current_year)
                        for may in may_order_details:
                            may_sale_amt=may_sale_amt+int(float(may.sale_amt))

                        jun_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=6,create_timestamp__year=current_year)
                        for jun in jun_order_details:
                            jun_sale_amt=jun_sale_amt+int(float(jun.sale_amt))

                        jul_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=7,create_timestamp__year=current_year)
                        for jul in jul_order_details:
                            jul_sale_amt=jul_sale_amt+int(float(jul.sale_amt))

                        aug_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=8,create_timestamp__year=current_year)
                        for aug in aug_order_details:
                            aug_sale_amt=aug_sale_amt+int(float(aug.sale_amt))

                        sep_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=9,create_timestamp__year=current_year)
                        for sep in sep_order_details:
                            sep_sale_amt=sep_sale_amt+int(float(sep.sale_amt))

                        oct_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=10,create_timestamp__year=current_year)
                        for oct in oct_order_details:
                            oct_sale_amt=oct_sale_amt+int(float(oct.sale_amt))

                        nov_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=11,create_timestamp__year=current_year)
                        for nov in nov_order_details:
                            nov_sale_amt=nov_sale_amt+int(float(nov.sale_amt))

                        dec_order_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=12,create_timestamp__year=current_year)
                        for dec in dec_order_details:
                            dec_sale_amt=dec_sale_amt+int(float(dec.sale_amt))


                return Response({'data':{'Jan':jan_sale_amt,
                'Feb':feb_sale_amt,
                'Mar':mar_sale_amt,
                'Apr':apr_sale_amt,
                'May':may_sale_amt,
                'Jun':jun_sale_amt,
                'Jul':jul_sale_amt,
                'Aug':aug_sale_amt,
                'Sep':sep_sale_amt,
                'Oct':oct_sale_amt,
                'Nov':nov_sale_amt,
                'Dec':dec_sale_amt,},'name':'Monthly Sales'})

            else:
                current_month=date.today().month
                current_year=date.today().year

                l = len(search)

                if search[l - 2:]=='01':
                    month_no=1

                if search[l - 2:]=='02':
                    month_no=2

                if search[l - 2:]=='03':
                    month_no=3
                if search[l - 2:]=='04':
                    month_no=4
                if search[l - 2:]=='05':
                    month_no=5
                if search[l - 2:]=='06':
                    month_no=6

                if search[l - 2:]=='07':
                    month_no=7
                if search[l - 2:]=='08':
                    month_no=8
                if search[l - 2:]=='09':
                    month_no=9

                if search[l - 2:]=='10':
                    month_no=10
                if search[l - 2:]=='11':
                    month_no=11
                if search[l - 2:]=='12':
                    month_no=12

                kri8evTeam_data = kri8evTeam.objects.filter(created_by=user_id)
                for i in kri8evTeam_data:
                    day1_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=1,create_timestamp__year=current_year)
                    for day1 in day1_details:
                        day1_sale_amt=day1_sale_amt+int(float(day1.total))

                    day2_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=2,create_timestamp__year=current_year)
                    for day2 in day2_details:
                        day2_sale_amt=day2_sale_amt+int(float(day2.total))

                    day3_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=3,create_timestamp__year=current_year)
                    for day3 in day3_details:
                        day3_sale_amt=day3_sale_amt+int(float(day3.total))

                    day4_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=4,create_timestamp__year=current_year)
                    for day4 in day4_details:
                        day4_sale_amt=day4_sale_amt+int(float(day4.total))

                    day5_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=5,create_timestamp__year=current_year)
                    for day5 in day5_details:
                        day5_sale_amt=day5_sale_amt+int(float(day5.total))


                    day6_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=6,create_timestamp__year=current_year)
                    for day6 in day6_details:
                        day6_sale_amt=day6_sale_amt+int(float(day6.total))

                    day7_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=7,create_timestamp__year=current_year)
                    for day7 in day7_details:
                        day7_sale_amt=day7_sale_amt+int(float(day7.total))


                    day8_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=8,create_timestamp__year=current_year)
                    for day8 in day8_details:
                        day8_sale_amt=day8_sale_amt+int(float(day8.total))

                    day9_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=9,create_timestamp__year=current_year)
                    for day9 in day9_details:
                        day9_sale_amt=day9_sale_amt+int(float(day9.total))

                    day10_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=10,create_timestamp__year=current_year)
                    for day10 in day10_details:
                        day10_sale_amt=day10_sale_amt+int(float(day10.total))

                    day11_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=11,create_timestamp__year=current_year)
                    for day11 in day11_details:
                        day11_sale_amt=day11_sale_amt+int(float(day11.total))

                    day12_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=12,create_timestamp__year=current_year)
                    for day12 in day12_details:
                        day12_sale_amt=day12_sale_amt+int(float(day12.total))


                    day13_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=13,create_timestamp__year=current_year)
                    for day13 in day13_details:
                        day13_sale_amt=day13_sale_amt+int(float(day13.total))

                    day14_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=14,create_timestamp__year=current_year)
                    for day14 in day14_details:
                        day14_sale_amt=day14_sale_amt+int(float(day14.total))


                    day15_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=15,create_timestamp__year=current_year)
                    for day15 in day15_details:
                        day15_sale_amt=day15_sale_amt+int(float(day15.total))

                    day16_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=16,create_timestamp__year=current_year)
                    for day16 in day16_details:
                        day16_sale_amt=day16_sale_amt+int(float(day16.total))

                    day17_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=17,create_timestamp__year=current_year)
                    for day17 in day17_details:
                        day17_sale_amt=day17_sale_amt+int(float(day17.total))

                    day18_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=18,create_timestamp__year=current_year)
                    for day18 in day18_details:
                        day18_sale_amt=day18_sale_amt+int(float(day18.total))

                    day19_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=19,create_timestamp__year=current_year)
                    for day19 in day19_details:
                        day19_sale_amt=day19_sale_amt+int(float(day19.total))


                    day20_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=20,create_timestamp__year=current_year)
                    for day20 in day20_details:
                        day20_sale_amt=day20_sale_amt+int(float(day20.total))

                    day21_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=21,create_timestamp__year=current_year)
                    for day21 in day21_details:
                        day21_sale_amt=day21_sale_amt+int(float(day21.total))


                    day22_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=22,create_timestamp__year=current_year)
                    for day22 in day22_details:
                        day22_sale_amt=day22_sale_amt+int(float(day22.total))

                    day23_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=23,create_timestamp__year=current_year)
                    for day23 in day23_details:
                        day23_sale_amt=day23_sale_amt+int(float(day23.total))

                    day24_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=24,create_timestamp__year=current_year)
                    for day24 in day24_details:
                        day24_sale_amt=day24_sale_amt+int(float(day24.total))

                    day25_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=25,create_timestamp__year=current_year)
                    for day25 in day25_details:
                        day25_sale_amt=day25_sale_amt+int(float(day25.total))

                    day26_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=26,create_timestamp__year=current_year)
                    for day26 in day26_details:
                        day26_sale_amt=day26_sale_amt+int(float(day26.total))


                    day27_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=27,create_timestamp__year=current_year)
                    for day27 in day27_details:
                        day27_sale_amt=day27_sale_amt+int(float(day27.total))

                    day28_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=28,create_timestamp__year=current_year)
                    for day28 in day28_details:
                        day28_sale_amt=day28_sale_amt+int(float(day28.total))

                    day29_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=29,create_timestamp__year=current_year)
                    for day29 in day29_details:
                        day29_sale_amt=day29_sale_amt+int(float(day29.total))

                    day30_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=30,create_timestamp__year=current_year)
                    for day30 in day30_details:
                        day30_sale_amt=day30_sale_amt+int(float(day30.total))

                    day31_details=Marketer_sales.objects.filter(marketer_id=i.user_id,create_timestamp__month=month_no,create_timestamp__day=31,create_timestamp__year=current_year)
                    for day31 in day31_details:
                        day31_sale_amt=day31_sale_amt+int(float(day31.total))


                if search=='feb':
                    return Response({'data':{'day1_sale_amt':day1_sale_amt,
                    'day2_sale_amt':day2_sale_amt,
                    'day3_sale_amt':day3_sale_amt,
                    'day4_sale_amt':day4_sale_amt,
                    'day5_sale_amt':day5_sale_amt,
                    'day6_sale_amt':day6_sale_amt,

                    'day7_sale_amt':day7_sale_amt,
                    'day8_sale_amt':day8_sale_amt,
                    'day9_sale_amt':day9_sale_amt,
                    'day10_sale_amt':day10_sale_amt,
                    'day11_sale_amt':day11_sale_amt,

                    'day12_sale_amt':day12_sale_amt,
                    'day13_sale_amt':day13_sale_amt,
                    'day14_sale_amt':day14_sale_amt,
                    'day15_sale_amt':day15_sale_amt,
                    'day16_sale_amt':day16_sale_amt,

                    'day17_sale_amt':day17_sale_amt,
                    'day18_sale_amt':day18_sale_amt,
                    'day19_sale_amt':day19_sale_amt,
                    'day20_sale_amt':day20_sale_amt,
                    'day21_sale_amt':day21_sale_amt,

                    'day22_sale_amt':day22_sale_amt,
                    'day23_sale_amt':day23_sale_amt,
                    'day24_sale_amt':day24_sale_amt,
                    'day25_sale_amt':day25_sale_amt,
                    'day26_sale_amt':day26_sale_amt,

                    'day27_sale_amt':day27_sale_amt,
                    'day28_sale_amt':day28_sale_amt,
                    'day29_sale_amt':day29_sale_amt,


                    },'name':'Day Wise Sale'})
                else:
                    return Response({'data':{'day1_sale_amt':day1_sale_amt,
                    'day2_sale_amt':day2_sale_amt,
                    'day3_sale_amt':day3_sale_amt,
                    'day4_sale_amt':day4_sale_amt,
                    'day5_sale_amt':day5_sale_amt,
                    'day6_sale_amt':day6_sale_amt,

                    'day7_sale_amt':day7_sale_amt,
                    'day8_sale_amt':day8_sale_amt,
                    'day9_sale_amt':day9_sale_amt,
                    'day10_sale_amt':day10_sale_amt,
                    'day11_sale_amt':day11_sale_amt,

                    'day12_sale_amt':day12_sale_amt,
                    'day13_sale_amt':day13_sale_amt,
                    'day14_sale_amt':day14_sale_amt,
                    'day15_sale_amt':day15_sale_amt,
                    'day16_sale_amt':day16_sale_amt,

                    'day17_sale_amt':day17_sale_amt,
                    'day18_sale_amt':day18_sale_amt,
                    'day19_sale_amt':day19_sale_amt,
                    'day20_sale_amt':day20_sale_amt,
                    'day21_sale_amt':day21_sale_amt,

                    'day22_sale_amt':day22_sale_amt,
                    'day23_sale_amt':day23_sale_amt,
                    'day24_sale_amt':day24_sale_amt,
                    'day25_sale_amt':day25_sale_amt,
                    'day26_sale_amt':day26_sale_amt,

                    'day27_sale_amt':day27_sale_amt,
                    'day28_sale_amt':day28_sale_amt,
                    'day29_sale_amt':day29_sale_amt,
                    'day30_sale_amt':day30_sale_amt,
                    'day31_sale_amt':day31_sale_amt,


                    },'name':'Day Wise Sale'})

from datetime import date

class Sales_filterAPI(APIView):
    def get(self,request):
        search=self.request.query_params.get('search')
        arr=[]
        jan_sale_amt=0
        feb_sale_amt=0
        mar_sale_amt=0
        apr_sale_amt=0
        may_sale_amt=0
        jun_sale_amt=0
        jul_sale_amt=0
        aug_sale_amt=0
        sep_sale_amt=0
        oct_sale_amt=0
        nov_sale_amt=0
        dec_sale_amt=0
        day1_sale_amt=0
        day2_sale_amt=0
        day3_sale_amt=0
        day4_sale_amt=0
        day5_sale_amt=0
        day6_sale_amt=0

        day7_sale_amt=0
        day8_sale_amt=0
        day9_sale_amt=0
        day10_sale_amt=0
        day11_sale_amt=0
        day12_sale_amt=0

        day13_sale_amt=0
        day14_sale_amt=0
        day15_sale_amt=0
        day16_sale_amt=0
        day17_sale_amt=0
        day18_sale_amt=0

        day19_sale_amt=0
        day20_sale_amt=0
        day21_sale_amt=0
        day22_sale_amt=0
        day23_sale_amt=0
        day24_sale_amt=0

        day25_sale_amt=0
        day26_sale_amt=0
        day27_sale_amt=0
        day28_sale_amt=0
        day29_sale_amt=0
        day30_sale_amt=0
        day31_sale_amt=0




        if search=='month_wise':
            current_month=date.today().month
            current_year=date.today().year
            if current_month==1:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))



                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                },'name':'Monthly Sales'})
            if current_month==2:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))



                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                },'name':'Monthly Sales'})
            if current_month==3:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))



                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                },'name':'Monthly Sales'})
            if current_month==4:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))



                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                },'name':'Monthly Sales'})
            if current_month==5:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))



                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                },'name':'Monthly Sales'})

            if current_month==6:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))


                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'Jan':jan_sale_amt,
                'Feb':feb_sale_amt,
                'Mar':mar_sale_amt,
                'Apr':apr_sale_amt,
                'May':may_sale_amt,
                'Jun':jun_sale_amt},'name':'Monthly Sales'})

            if current_month==7:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))

                jul_order_details=OrderDetails.objects.filter(create_timestamp__month=7,create_timestamp__year=current_year)
                for jul in jul_order_details:
                    jul_sale_amt=jul_sale_amt+int(float(jul.total))


                # return Response({'month':'Jan','jan_sale_amt':jan_sale_amt,
                # 'month':'Jan','feb_sale_amt':feb_sale_amt,
                # 'month':'Mar','mar_sale_amt':mar_sale_amt,
                # 'month':'Apr','apr_sale_amt':apr_sale_amt,
                # 'month':'May','may_sale_amt':may_sale_amt,
                # 'month':'Jun','jun_sale_amt':jun_sale_amt})
                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                'jun_sale_amt':jun_sale_amt,
                'jul_sale_amt':jul_sale_amt},'name':'Monthly Sales'})

            if current_month==8:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))

                jul_order_details=OrderDetails.objects.filter(create_timestamp__month=7,create_timestamp__year=current_year)
                for jul in jul_order_details:
                    jul_sale_amt=jul_sale_amt+int(float(jul.total))

                aug_order_details=OrderDetails.objects.filter(create_timestamp__month=8,create_timestamp__year=current_year)
                for aug in aug_order_details:
                    aug_sale_amt=aug_sale_amt+int(float(aug.total))



                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                'jun_sale_amt':jun_sale_amt,
                'jul_sale_amt':jul_sale_amt,
                'aug_sale_amt':aug_sale_amt,
                },'name':'Monthly Sales'})

            if current_month==9:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))

                jul_order_details=OrderDetails.objects.filter(create_timestamp__month=7,create_timestamp__year=current_year)
                for jul in jul_order_details:
                    jul_sale_amt=jul_sale_amt+int(float(jul.total))

                aug_order_details=OrderDetails.objects.filter(create_timestamp__month=8,create_timestamp__year=current_year)
                for aug in aug_order_details:
                    aug_sale_amt=aug_sale_amt+int(float(aug.total))

                sep_order_details=OrderDetails.objects.filter(create_timestamp__month=9,create_timestamp__year=current_year)
                for sep in sep_order_details:
                    sep_sale_amt=sep_sale_amt+int(float(sep.total))





                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                'jun_sale_amt':jun_sale_amt,
                'jul_sale_amt':jul_sale_amt,
                'aug_sale_amt':aug_sale_amt,
                'sep_sale_amt':sep_sale_amt,
                },'name':'Monthly Sales'})

            if current_month==10:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))

                jul_order_details=OrderDetails.objects.filter(create_timestamp__month=7,create_timestamp__year=current_year)
                for jul in jul_order_details:
                    jul_sale_amt=jul_sale_amt+int(float(jul.total))

                aug_order_details=OrderDetails.objects.filter(create_timestamp__month=8,create_timestamp__year=current_year)
                for aug in aug_order_details:
                    aug_sale_amt=aug_sale_amt+int(float(aug.total))

                sep_order_details=OrderDetails.objects.filter(create_timestamp__month=9,create_timestamp__year=current_year)
                for sep in sep_order_details:
                    sep_sale_amt=sep_sale_amt+int(float(sep.total))

                oct_order_details=OrderDetails.objects.filter(create_timestamp__month=10,create_timestamp__year=current_year)
                for oct in oct_order_details:
                    oct_sale_amt=oct_sale_amt+int(float(oct.total))



                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                'jun_sale_amt':jun_sale_amt,
                'jul_sale_amt':jul_sale_amt,
                'aug_sale_amt':aug_sale_amt,
                'sep_sale_amt':sep_sale_amt,
                'oct_sale_amt':oct_sale_amt,
                },'name':'Monthly Sales'})

            if current_month==11:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))

                jul_order_details=OrderDetails.objects.filter(create_timestamp__month=7,create_timestamp__year=current_year)
                for jul in jul_order_details:
                    jul_sale_amt=jul_sale_amt+int(float(jul.total))

                aug_order_details=OrderDetails.objects.filter(create_timestamp__month=8,create_timestamp__year=current_year)
                for aug in aug_order_details:
                    aug_sale_amt=aug_sale_amt+int(float(aug.total))

                sep_order_details=OrderDetails.objects.filter(create_timestamp__month=9,create_timestamp__year=current_year)
                for sep in sep_order_details:
                    sep_sale_amt=sep_sale_amt+int(float(sep.total))

                oct_order_details=OrderDetails.objects.filter(create_timestamp__month=10,create_timestamp__year=current_year)
                for oct in oct_order_details:
                    oct_sale_amt=oct_sale_amt+int(float(oct.total))

                nov_order_details=OrderDetails.objects.filter(create_timestamp__month=11,create_timestamp__year=current_year)
                for nov in nov_order_details:
                    nov_sale_amt=nov_sale_amt+int(float(nov.total))



                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                'jun_sale_amt':jun_sale_amt,
                'jul_sale_amt':jul_sale_amt,
                'aug_sale_amt':aug_sale_amt,
                'sep_sale_amt':sep_sale_amt,
                'oct_sale_amt':oct_sale_amt,
                'nov_sale_amt':nov_sale_amt,
                },'name':'Monthly Sales'})

            if current_month==12:
                jan_order_details=OrderDetails.objects.filter(create_timestamp__month=1,create_timestamp__year=current_year)
                for jan in jan_order_details:
                    jan_sale_amt=jan_sale_amt+int(float(jan.total))

                feb_order_details=OrderDetails.objects.filter(create_timestamp__month=2,create_timestamp__year=current_year)
                for feb in feb_order_details:
                    feb_sale_amt=feb_sale_amt+int(float(feb.total))

                mar_order_details=OrderDetails.objects.filter(create_timestamp__month=3,create_timestamp__year=current_year)
                for mar in mar_order_details:
                    mar_sale_amt=mar_sale_amt+int(float(mar.total))

                apr_order_details=OrderDetails.objects.filter(create_timestamp__month=4,create_timestamp__year=current_year)
                for apr in apr_order_details:
                    apr_sale_amt=apr_sale_amt+int(float(apr.total))

                may_order_details=OrderDetails.objects.filter(create_timestamp__month=5,create_timestamp__year=current_year)
                for may in may_order_details:
                    may_sale_amt=may_sale_amt+int(float(may.total))

                jun_order_details=OrderDetails.objects.filter(create_timestamp__month=6,create_timestamp__year=current_year)
                for jun in jun_order_details:
                    jun_sale_amt=jun_sale_amt+int(float(jun.total))

                jul_order_details=OrderDetails.objects.filter(create_timestamp__month=7,create_timestamp__year=current_year)
                for jul in jul_order_details:
                    jul_sale_amt=jul_sale_amt+int(float(jul.total))

                aug_order_details=OrderDetails.objects.filter(create_timestamp__month=8,create_timestamp__year=current_year)
                for aug in aug_order_details:
                    aug_sale_amt=aug_sale_amt+int(float(aug.total))

                sep_order_details=OrderDetails.objects.filter(create_timestamp__month=9,create_timestamp__year=current_year)
                for sep in sep_order_details:
                    sep_sale_amt=sep_sale_amt+int(float(sep.total))

                oct_order_details=OrderDetails.objects.filter(create_timestamp__month=10,create_timestamp__year=current_year)
                for oct in oct_order_details:
                    oct_sale_amt=oct_sale_amt+int(float(oct.total))

                nov_order_details=OrderDetails.objects.filter(create_timestamp__month=11,create_timestamp__year=current_year)
                for nov in nov_order_details:
                    nov_sale_amt=nov_sale_amt+int(float(nov.total))

                dec_order_details=OrderDetails.objects.filter(create_timestamp__month=12,create_timestamp__year=current_year)
                for dec in dec_order_details:
                    dec_sale_amt=dec_sale_amt+int(float(dec.total))



                return Response({'data':{'jan_sale_amt':jan_sale_amt,
                'feb_sale_amt':feb_sale_amt,
                'mar_sale_amt':mar_sale_amt,
                'apr_sale_amt':apr_sale_amt,
                'may_sale_amt':may_sale_amt,
                'jun_sale_amt':jun_sale_amt,
                'jul_sale_amt':jul_sale_amt,
                'aug_sale_amt':aug_sale_amt,
                'sep_sale_amt':sep_sale_amt,
                'oct_sale_amt':oct_sale_amt,
                'nov_sale_amt':nov_sale_amt,
                'dec_sale_amt':dec_sale_amt,},'name':'Monthly Sales'})

        if search=='year_wise':
            sale_amt1=0
            sale_amt2=0
            sale_amt3=0
            current_year=date.today().year
            order_details=OrderDetails.objects.filter(create_timestamp__year=current_year-2)
            for i in order_details:
                sale_amt1=sale_amt1+int(float(i.total))
            order_details=OrderDetails.objects.filter(create_timestamp__year=current_year-1)
            for i in order_details:
                sale_amt2=sale_amt2+int(float(i.total))
            order_details=OrderDetails.objects.filter(create_timestamp__year=current_year)
            for i in order_details:
                sale_amt3=sale_amt3+int(float(i.total))
            return Response({'data':{'2020 Sales':sale_amt1,
            '2021 Sales':sale_amt2,
            '2022 Sales':sale_amt3,},'name':'Yearly Sales'})
        else:
            current_month=date.today().month
            current_year=date.today().year
            l = len(search)
            # print(search[l - 2:])

            if search[l - 2:]=='01':
                month_no=1

            if search[l - 2:]=='02':
                month_no=2

            if search[l - 2:]=='03':
                month_no=3
            if search[l - 2:]=='04':
                month_no=4
            if search[l - 2:]=='05':
                month_no=5
            if search[l - 2:]=='06':
                month_no=6

            if search[l - 2:]=='07':
                month_no=7
            if search[l - 2:]=='08':
                month_no=8
            if search[l - 2:]=='09':
                month_no=9

            if search[l - 2:]=='10':
                month_no=10
            if search[l - 2:]=='11':
                month_no=11
            if search[l - 2:]=='12':
                month_no=12
            day1_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=1,create_timestamp__year=current_year)
            for day1 in day1_details:
                day1_sale_amt=day1_sale_amt+int(float(day1.total))

            day2_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=2,create_timestamp__year=current_year)
            for day2 in day2_details:
                day2_sale_amt=day2_sale_amt+int(float(day2.total))

            day3_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=3,create_timestamp__year=current_year)
            for day3 in day3_details:
                day3_sale_amt=day3_sale_amt+int(float(day3.total))

            day4_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=4,create_timestamp__year=current_year)
            for day4 in day4_details:
                day4_sale_amt=day4_sale_amt+int(float(day4.total))

            day5_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=5,create_timestamp__year=current_year)
            for day5 in day5_details:
                day5_sale_amt=day5_sale_amt+int(float(day5.total))


            day6_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=6,create_timestamp__year=current_year)
            for day6 in day6_details:
                day6_sale_amt=day6_sale_amt+int(float(day6.total))

            day7_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=7,create_timestamp__year=current_year)
            for day7 in day7_details:
                day7_sale_amt=day7_sale_amt+int(float(day7.total))


            day8_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=8,create_timestamp__year=current_year)
            for day8 in day8_details:
                day8_sale_amt=day8_sale_amt+int(float(day8.total))

            day9_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=9,create_timestamp__year=current_year)
            for day9 in day9_details:
                day9_sale_amt=day9_sale_amt+int(float(day9.total))

            day10_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=10,create_timestamp__year=current_year)
            for day10 in day10_details:
                day10_sale_amt=day10_sale_amt+int(float(day10.total))

            day11_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=11,create_timestamp__year=current_year)
            for day11 in day11_details:
                day11_sale_amt=day11_sale_amt+int(float(day11.total))

            day12_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=12,create_timestamp__year=current_year)
            for day12 in day12_details:
                day12_sale_amt=day12_sale_amt+int(float(day12.total))


            day13_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=13,create_timestamp__year=current_year)
            for day13 in day13_details:
                day13_sale_amt=day13_sale_amt+int(float(day13.total))

            day14_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=14,create_timestamp__year=current_year)
            for day14 in day14_details:
                day14_sale_amt=day14_sale_amt+int(float(day14.total))


            day15_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=15,create_timestamp__year=current_year)
            for day15 in day15_details:
                day15_sale_amt=day15_sale_amt+int(float(day15.total))

            day16_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=16,create_timestamp__year=current_year)
            for day16 in day16_details:
                day16_sale_amt=day16_sale_amt+int(float(day16.total))

            day17_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=17,create_timestamp__year=current_year)
            for day17 in day17_details:
                day17_sale_amt=day17_sale_amt+int(float(day17.total))

            day18_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=18,create_timestamp__year=current_year)
            for day18 in day18_details:
                day18_sale_amt=day18_sale_amt+int(float(day18.total))

            day19_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=19,create_timestamp__year=current_year)
            for day19 in day19_details:
                day19_sale_amt=day19_sale_amt+int(float(day19.total))


            day20_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=20,create_timestamp__year=current_year)
            for day20 in day20_details:
                day20_sale_amt=day20_sale_amt+int(float(day20.total))

            day21_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=21,create_timestamp__year=current_year)
            for day21 in day21_details:
                day21_sale_amt=day21_sale_amt+int(float(day21.total))


            day22_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=22,create_timestamp__year=current_year)
            for day22 in day22_details:
                day22_sale_amt=day22_sale_amt+int(float(day22.total))

            day23_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=23,create_timestamp__year=current_year)
            for day23 in day23_details:
                day23_sale_amt=day23_sale_amt+int(float(day23.total))

            day24_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=24,create_timestamp__year=current_year)
            for day24 in day24_details:
                day24_sale_amt=day24_sale_amt+int(float(day24.total))

            day25_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=25,create_timestamp__year=current_year)
            for day25 in day25_details:
                day25_sale_amt=day25_sale_amt+int(float(day25.total))

            day26_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=26,create_timestamp__year=current_year)
            for day26 in day26_details:
                day26_sale_amt=day26_sale_amt+int(float(day26.total))


            day27_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=27,create_timestamp__year=current_year)
            for day27 in day27_details:
                day27_sale_amt=day27_sale_amt+int(float(day27.total))

            day28_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=28,create_timestamp__year=current_year)
            for day28 in day28_details:
                day28_sale_amt=day28_sale_amt+int(float(day28.total))

            day29_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=29,create_timestamp__year=current_year)
            for day29 in day29_details:
                day29_sale_amt=day29_sale_amt+int(float(day29.total))

            day30_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=30,create_timestamp__year=current_year)
            for day30 in day30_details:
                day30_sale_amt=day30_sale_amt+int(float(day30.total))

            day31_details=OrderDetails.objects.filter(create_timestamp__month=month_no,create_timestamp__day=31,create_timestamp__year=current_year)
            for day31 in day31_details:
                day31_sale_amt=day31_sale_amt+int(float(day31.total))


            if search=='feb':
                return Response({'data':{'day1_sale_amt':day1_sale_amt,
                'day2_sale_amt':day2_sale_amt,
                'day3_sale_amt':day3_sale_amt,
                'day4_sale_amt':day4_sale_amt,
                'day5_sale_amt':day5_sale_amt,
                'day6_sale_amt':day6_sale_amt,

                'day7_sale_amt':day7_sale_amt,
                'day8_sale_amt':day8_sale_amt,
                'day9_sale_amt':day9_sale_amt,
                'day10_sale_amt':day10_sale_amt,
                'day11_sale_amt':day11_sale_amt,

                'day12_sale_amt':day12_sale_amt,
                'day13_sale_amt':day13_sale_amt,
                'day14_sale_amt':day14_sale_amt,
                'day15_sale_amt':day15_sale_amt,
                'day16_sale_amt':day16_sale_amt,

                'day17_sale_amt':day17_sale_amt,
                'day18_sale_amt':day18_sale_amt,
                'day19_sale_amt':day19_sale_amt,
                'day20_sale_amt':day20_sale_amt,
                'day21_sale_amt':day21_sale_amt,

                'day22_sale_amt':day22_sale_amt,
                'day23_sale_amt':day23_sale_amt,
                'day24_sale_amt':day24_sale_amt,
                'day25_sale_amt':day25_sale_amt,
                'day26_sale_amt':day26_sale_amt,

                'day27_sale_amt':day27_sale_amt,
                'day28_sale_amt':day28_sale_amt,
                'day29_sale_amt':day29_sale_amt,


                },'name':'Day Wise Sale'})
            else:
                return Response({'data':{'day1_sale_amt':day1_sale_amt,
                'day2_sale_amt':day2_sale_amt,
                'day3_sale_amt':day3_sale_amt,
                'day4_sale_amt':day4_sale_amt,
                'day5_sale_amt':day5_sale_amt,
                'day6_sale_amt':day6_sale_amt,

                'day7_sale_amt':day7_sale_amt,
                'day8_sale_amt':day8_sale_amt,
                'day9_sale_amt':day9_sale_amt,
                'day10_sale_amt':day10_sale_amt,
                'day11_sale_amt':day11_sale_amt,

                'day12_sale_amt':day12_sale_amt,
                'day13_sale_amt':day13_sale_amt,
                'day14_sale_amt':day14_sale_amt,
                'day15_sale_amt':day15_sale_amt,
                'day16_sale_amt':day16_sale_amt,

                'day17_sale_amt':day17_sale_amt,
                'day18_sale_amt':day18_sale_amt,
                'day19_sale_amt':day19_sale_amt,
                'day20_sale_amt':day20_sale_amt,
                'day21_sale_amt':day21_sale_amt,

                'day22_sale_amt':day22_sale_amt,
                'day23_sale_amt':day23_sale_amt,
                'day24_sale_amt':day24_sale_amt,
                'day25_sale_amt':day25_sale_amt,
                'day26_sale_amt':day26_sale_amt,

                'day27_sale_amt':day27_sale_amt,
                'day28_sale_amt':day28_sale_amt,
                'day29_sale_amt':day29_sale_amt,
                'day30_sale_amt':day30_sale_amt,
                'day31_sale_amt':day31_sale_amt,


                },'name':'Day Wise Sale'})
