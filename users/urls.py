from django.urls import path
from .views import*


urlpatterns = [
    path('register/', userRegisteration, name='userRegisteration'),
    path('login/', userLoginByEmail, name='userLogin'),
    path('logout/',userLogout, name="userLogout"),
    path('profile/', userProfile, name="profile"),
    path('changepassword/', changePassword, name="changepassword"),
    path('sendresetpassword/', sendresetPassword, name="sendresetpassword"),
    path('resetpassword/<uid>/<token>/', resetPassword, name="resetpassword"),
    path('imagelogin/', userLoginByImage, name="imagelogin"),
    path('sendloginotp/', UserLoginByContact, name="sendotp"),
    path('verifyloginotp/', verifyOtpForLogin, name="verifyotp"),
    path('addcategories/', addCategories,name="addcategories",),
    path('getcategories/', getCategories,name="getcategories",),
    path('addservice/', addServiceToCategory,name="addservicetocategory",),
    path('getservice/', getServiceOfCategory,name="getServiceOfCategory",),
   
]
