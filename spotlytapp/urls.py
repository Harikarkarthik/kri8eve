from django.urls import path, include
from spotlytapp.views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_swagger.views import get_swagger_view


app_name = 'spotlytapp'


router = routers.DefaultRouter()
# router.register(r'announcements' , AnnouncementView ,basename="announcements")
schema_view = get_swagger_view(title='Api Documentation')

urlpatterns = [
    path('', include(router.urls)),
    path('api_documentation/', schema_view),
    # path('email_verfication/', EmailVerification.as_view()),
    path('signup/', SignupApi.as_view()),
    path('login/', LoginView.as_view(), name="JWT-LOGIN"),
    # path('api-token-auth/', CustomAuthToken.as_view(), name="LOGIN"),
    # path('logout/', Logout.as_view()),
    # path('forgotpassword/', ForgotPassword.as_view()),
    # path('change-password/', ChangePassword.as_view()),
    # path('course/', CourseAPIView.as_view()),
    # path('get_course/', Get_CourseAPIView.as_view()),
    # path('lesson/', LessonAPIView.as_view()),
    # path('faqs/', FAQsAPIView.as_view()),
    # path('get_faqs/', Get_FaqsAPIView.as_view()),
    # path('post/', PostAPIView.as_view()),
    # path('get_post/', Get_PostAPIView.as_view()),
    # path('registeration_code/', RegisterationCodeAPIView.as_view()),
    # path('comments/', CommentsAPIView.as_view()),
    # path('reviews/', ReviewsAPIView.as_view()),
    # path('orders/', OrdersAPIView.as_view()),
    # path('get_orders/', Get_OrdersAPIView.as_view()),

    # path('user_course/', UserCourseAPIView.as_view()),
    # path('testimonials/', TestimonialsAPIView.as_view()),
    # path('download/', InvoicePDF),
    # path('dashboard/', DashboardAPIView.as_view()),
    # path('reg_user/', RegisterUserAPIView.as_view()),
    # path('get_reg_user/', Get_Reg_UserAPIView.as_view()),
    # path('enquiry/', EnquiryAPIView.as_view()),
    # path('get_enq/', Get_EnquiryAPIView.as_view()),
    # path('get_announcement/', Get_AnnouncementAPIView.as_view()),
    # path('announcement/', AnnouncementAPIView.as_view()),
    # path('spotlyt_team/', SpotlytTeamApiView.as_view()),
    # path('course_survey/', Course_surveyAPIView.as_view()),
    # path('survey_question/', Survey_questionAPIView.as_view()),
    # path('question_choice/', Question_choiceAPIView.as_view()),
    # path('new_lesson/', New_lesson_APIView.as_view()),
    # path('leaderboard/', LeaderboardAPIView.as_view()),
    # path('notification/', NotificationAPIView.as_view()),
    # path('promo_code/', PromoCodeAPIView.as_view()),
    # path('student_update/', Student_updateAPIView.as_view()),
    # path('active_course/', Active_courseAPIView.as_view()),
    # path('faqs_query/', FAQsQueryAPIView.as_view()),
    # path('student_result/', Student_resultAPIView.as_view()),
    # path('payment/',PaymentAPIView.as_view()),
    # path('access_key_validations_dashboard/',Access_key_validations_dashboardAPIView.as_view()),
    # path('access_key_validations/',Access_key_validationsAPIView.as_view()),
    # path('course_finish/',Course_finishAPIView.as_view()),

    # path('subscribe/',SubscribeAPIView.as_view()),
    # path('otp/',Send_otp.as_view()),
    # path('login_otp/',login_otp.as_view()),
    # path('reg_otp/',Reg_otp.as_view()),
    # path('otp_Verification_signup/',OTP_Verification_signupAPIView.as_view()),
    # path('otp_Verification_login/',OTP_Verification_signupAPIView.as_view()),
    # path('certificate/',views.Certificate , name='home'),

    # path('forgot_password_otp/',ForgotPassword_send_otp.as_view()),
    # path('otp_Verification_forgot/',OTP_Verification_forgotpassAPIView.as_view()),
    # path('forgot_password_update/', ForgotPasswordUpdate.as_view()),



    # path('upload_student_data/', Upload_student_data.as_view()),
    # path('upload_enquiry_data/', Upload_enquiry_data.as_view()),
    # path('upload_orders_data/', Upload_orders_data.as_view()),
    # path('upload_course_data/', Upload_course_data.as_view()),


    # path('download_student_data/', Download_student_data.as_view()),
    # path('download_course_data/', Download_course_data.as_view()),
    # path('download_enquiry_data/', Download_enquiry_data.as_view()),
    # path('download_orders_data/', Download_orders_data.as_view()),
    # path('download_student_activity_data/', Download_student_activity_data.as_view()),
    # path('download_student_access_code/', Download_access_code.as_view()),



    path('product/', ProductApiView.as_view()),
    path('product/<int:pk>/', ProductApiView.as_view()),
    path('edit_product/', Edit_productApiView.as_view()),

    path('edit_product/<int:pk>/', Edit_productApiView.as_view()),

    path('productcategory/', ProductCategoryView.as_view(),name='productcategory'),
    path('productcategory/<int:pk>/', ProductCategoryView.as_view()),

    path('sub_category/', Product_Sub_CategoryAPIView.as_view(),name='productcategory'),
    path('sub_category/<int:pk>/', Product_Sub_CategoryAPIView.as_view()),

    path('productinventory/', ProductInventorApi.as_view()),
    path('productinventory/<int:pk>/', ProductInventorApi.as_view()),

    path('discount/', DiscountApi.as_view()),
    path('discount/<int:pk>/', DiscountApi.as_view()),


    path('custom/', Custom_Userapi.as_view()),
    path('custom/<int:pk>/', Custom_Userapi.as_view()),

    # path('userauthentication/', UserAuthenticationApi.as_view()),
    # path('userauthentication/<int:pk>/', UserAuthenticationApi.as_view()),

    path('useraddress/', UserAddressApi.as_view()),
    path('useraddress/<int:pk>/', UserAddressApi.as_view()),

    path('userpayment/', UserPaymentApi.as_view()),
    path('userpayment/<int:pk>/', UserPaymentApi.as_view()),


    path('user_role/', UserRoleRefAPIView.as_view()),
    path('user_role/<int:pk>/', UserRoleRefAPIView.as_view()),

    path('faqapi/', FAQAPIVIEW.as_view()),
    path('faqapi/<int:pk>/', FAQAPIVIEW.as_view()),


    path('reviews/', ReviewApiViews.as_view()),
    path('reviews/<int:pk>/', ReviewApiViews.as_view()),



    path('testimonials/', TestimonialsAPIView.as_view()),
    path('testimonials/<int:pk>/', TestimonialsAPIView.as_view()),

    path('orderdetails/', OrderDetailsApis.as_view()),
    path('orderdetails/<int:pk>/', OrderDetailsApis.as_view()),


    path('paymentetails', PaymentDetailsApi.as_view()),
    path('paymentetails/<int:pk>/', PaymentDetailsApi.as_view()),

    path('orderitems/', OrderItemsApi.as_view()),
    path('orderitems/<int:pk>/', OrderItemsApi.as_view()),

    path('shoppingsession/', ShoppingSessionApi.as_view()),
    path('shoppingsession/<int:pk>/', ShoppingSessionApi.as_view()),

    path('cartitem/', CartItemApi.as_view()),
    path('cartitem/<int:pk>/', CartItemApi.as_view()),
    path('get_cartitem/', Get_CartItemApi.as_view()),

    path('buy_now_cartitem/', Buy_NowCartItemApi.as_view()),


    path('leaderboard/', LeaderBoardOneApi.as_view()),


    path('alldetails', OrderDetailItemApi.as_view()),


    path('promocode/', PromoCodeApi.as_view()),
    path('promocode/<int:pk>/', PromoCodeApi.as_view()),

    path('shippingcharges/', ShippingChargesApi.as_view()),
    path('shippingcharges/<int:pk>/', ShippingChargesApi.as_view()),

    path('attributes/', AttributesApi.as_view()),
    path('attributes/<int:pk>/', AttributesApi.as_view()),

    # path('attributeoptions', AttributeOptionsApi.as_view()),
    # path('attributeoptions/<int:pk>/', AttributeOptionsApi.as_view()),

    # path('productattribute/', ProductsAttributeApi.as_view()),
    # path('productattribute/<int:pk>/', ProductsAttributeApi.as_view()),



    path('startpayment/', views.start_payment),
    path('handle_payment_success/',views.handle_payment_success),

#########################Gunjan############################
    path('menu_category/', Menu_CategoryAPIView.as_view()),
    path('get_product_wise_sub_category/', Get_Product_Wise_Sub_CategoryAPIView.as_view()),
    path('wishlist/', WishlistApi.as_view()),

    path('promo_code_validations/',Promo_code_validationsAPIView.as_view()),
    path('social-login/', SocialMdGmailSignupApi.as_view()),
    path('deal_of_the_day/', Deal_of_the_dayAPIView.as_view()),
    path('deal_of_the_day/<int:pk>/', Deal_of_the_dayAPIView.as_view()),

    path('shipping_validation/', Shipping_validationApi.as_view()),
    path('final_amount/', Final_amountApi.as_view()),
    path('enquiry/', EnquiryAPIView.as_view()),

    path('enquiry/<int:pk>/', EnquiryAPIView.as_view()),
    path('team/', kri8evTeamApiView.as_view()),
    path('team/<int:pk>/', kri8evTeamApiView.as_view()),

    path('get_leader_role/', Get_leader_roleapi.as_view()),
    path('get_leader_role/<int:pk>/', Get_leader_roleapi.as_view()),

    path('get_marketer_role/', Get_marketer_roleapi.as_view()),
    path('get_marketer_role/<int:pk>/', Get_marketer_roleapi.as_view()),

    path('brand/', BrandAPIView.as_view()),
    path('brand/<int:pk>/', BrandAPIView.as_view()),

    path('get_category_wise_brand/', Get_category_wise_brandAPIView.as_view()),
    path('get_brand_wise_prduct/', Get_brand_wise_prductAPIView.as_view()),
    path('product_by_sub_category/', Product_by_sub_categoryApiView.as_view()),
    path('purchase_details/', Purchase_detailsAPIView.as_view()),
    path('get_username_mobile/', Get_username_mobile.as_view()),
    path('update_default_address/<int:pk>/', Update_default_addressApi.as_view()),
    path('get_attribute/', Get_attributeAPIView.as_view()),
    path('get_color_attribute/', Get_color_attributeAPIView.as_view()),
    path('get_size_attribute/', Get_size_attributeAPIView.as_view()),
    path('purchase_details_by_payment/', Purchase_details_by_paymentAPIView.as_view()),
    path('quantity_update/<int:pk>/', Quantity_update_CartItemApi.as_view()),
    path('forgot_password_otp/',ForgotPassword_send_otp.as_view()),#
    path('otp_Verification_forgot/',OTP_Verification_forgotpassAPIView.as_view()),#
    path('forgot_password_update/', ForgotPasswordUpdate.as_view()),#
    path('product_filter/', Product_filterAPI.as_view()),#
    path('user_under_marketer/', User_under_marketerAPIView.as_view()),#

    path('user_under_leader/', User_under_LeaderAPIView.as_view()),#
    # path('team_config/', Team_ConfigAPIView.as_view()),#
    # path('team_config/<int:pk>/', Team_ConfigAPIView.as_view()),

    path('get_product_color/', Get_product_colorApiView.as_view()),
    path('get_product_size/', Get_product_sizeApiView.as_view()),
    path('marketer_salary_bonous_incentive/', Marketer_salary_bonous_incentiveAPIView.as_view()),
    path('leader_salary_bonous_incentive/', Leader_salary_bonous_incentiveAPIView.as_view()),
    path('profile_img/', Profile_imgAPIView.as_view()),

    path('get_unique_attribute_name/', Unique_Attribute_NameApi.as_view()),
    path('get_name_wise_attribute_option/', Name_wise_attribute_optionApi.as_view()),
    path('del_wishlist_pro/', Delete_wishlist_based_on_product_idAPIView.as_view()),
    path('delete_slide_image/<int:pk>/', Delete_slideImageApiView.as_view()),
    path('delete_attribute/<int:pk>/', Delete_attributeApiView.as_view()),

    path('user_promocode/', User_PromoDetailsApi.as_view()),

    path('newly_added/', Newly_added_productApi.as_view()),
    path('trending_product/', Trending_productApi.as_view()),
    path('get_assign_product_for_delivery_boy/', Get_Assign_product_for_delivery_boyApis.as_view()),
    path('get_marketer_sales_details/', Get_Marketer_sales_DetailsApis.as_view()),
    path('get_date_wise_marketer_sales_details/', Get_date_wise_marketer_sales_detailsApis.as_view()),
    path('get_month_wise_marketer_sales_details/', Get_month_wise_marketer_sales_detailsApis.as_view()),
    path('get_sales_details/', Get_SalesAPIView.as_view()),
    path('get_product_wise_category/', get_Product_wise_category.as_view()),

    path('get_all_delivery_boy/', get_all_Delivery_boy.as_view()),
    path('dashboard/', DashboardAPIView.as_view()),
    path('validate_email/', Validate_emailAPIView.as_view()),
    path('validate_mobile/', Validate_mobileAPIView.as_view()),

    path('reg_otp/',Reg_otp.as_view()),#
    path('otp_Verification_signup/',OTP_Verification_signupAPIView.as_view()),#

    path('sales_filter/',Sales_filterAPI.as_view()),#
    path('get_marketer_sale_graph/',Get_Marketer_sale_graph.as_view()),#




    # path('api-token-auth/', CustomAuthToken.as_view()),





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
