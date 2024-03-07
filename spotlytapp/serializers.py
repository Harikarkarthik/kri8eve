from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User





class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields ="__all__"

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Category
        fields ="__all__"




class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('username', 'email', 'password','last_name')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class CustUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Custom_User
        fields ="__all__"

class CustUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields ="__all__"


class ForgotPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password',)
        #fields = ('password')


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields ="__all__"


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields ="__all__"



class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields ="__all__"


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields ="__all__"




class OrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        fields ="__all__"

class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCode
        fields ="__all__"

class PaymentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentDetails
        fields ="__all__"


class FAQsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQs
        fields ="__all__"

class UserRoleRefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRoleRef
        fields ="__all__"

class TestimonialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimonials
        fields ="__all__"

class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields ="__all__"
