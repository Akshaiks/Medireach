"""
URL configuration for smartcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",login_p,name="login_p"),
    path("login_p/",login_p,name="login_p"),
    path("index/",index,name='index'),
    path('index_d/',index_d,name='index_d'),
    path('video_consultation_user/',video_consultation_user,name='video_consultation_user'),
    path('medical_history/',medical_history,name='medical_history'),
    path('sign_up/',sign_up,name='sign_up'),
    path('login_view',login_view,name='login_view'),
    path('medical_history_d.html',medical_history_d,name='medical_history_d'),
    path('request_send',request_send,name='request_send'),
    path('video_consultation_requests/',video_consultation_requests,name='video_consultation_requests'),
    path('send_link/<int:request_id>/', send_link, name='send_link'),
    path('reject_request/<int:request_id>/',reject_request, name='reject_request'),
    path('video_consultation_user/',video_consultation_user,name='video_consultation_user'),
    path('signout/',signout,name='signout'),
    path('prescription_d/',prescription_d,name='prescription_d'),
    path('upload_prescription/',upload_prescription,name='upload_prescription'),
    path('prescription_view',prescription_view,name='prescription_view'),
    path('profile_view/',profile_view,name='profile_view'),
    path('get_sensor_data/',get_sensor_data,name='get_sensor_data'),
    path('medical_history/live_sensor_data/',live_sensor_data,name='live_sensor_data'),
    path('medical_history/get_history_data/',get_history_data,name='get_history_data'),
    path('live_sensor_data_d/<str:username>/', live_sensor_data_d, name='live_sensor_data_d'),
    path('get_history_data_d/<str:username>/', get_history_data_d, name='get_history_data_d'),
    path('get_users/', get_users, name='get_users'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('update_password/', update_password, name='update_password'),

]
