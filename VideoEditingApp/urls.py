from django.urls import path
from VideoEditingApp .views import *
from VideoEditingApp import views  

urlpatterns = [
    path('thumbnailapi/',ThumbnailView.as_view(),name='thumbnail'),
    path('renamethumbnail_title/',RenameTitleThumbnail.as_view(),name='thumbnail_title'),
    path('upload_video/',VideoView.as_view(),name='thumbnail_title'),
    path('audio/',VideoToAudioView.as_view(),name='thumbnail_title'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email_otp/', SendOtpEmail.as_view()),
    path('email_verify/', VerifyEmailView.as_view()),
    path('index/', views.index),  
    path('productlist/', views.product_list),  
    path('person/<int:pk>/', PersonDetailView.as_view()),
    path('email_testing/', EmailView.as_view(), name='email'),
    path('json/', ConvertJson.as_view(), name='email'),
   
]