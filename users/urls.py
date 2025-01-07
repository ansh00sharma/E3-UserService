from django.urls import path
from .views import*


urlpatterns = [
    path('register/', userRegisteration, name='userRegisteration'),
    path('login/', userLogin, name='userLogin'),
    path('profile/', userProfile, name="profile"),
    path('changepassword/', changePassword, name="changepassword"),
    path('sendresetpassword/', sendresetPassword, name="sendresetpassword"),
    path('resetpassword/<uid>/<token>/', resetPassword, name="resetpassword"),
   
]
