from django.contrib import admin
from django.urls import path, include
from users import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-api'),
    path('test/', views.test, name="Test GET/POST Api"),
    

    # path('guest/', include('faculty.urls'))
    path('users/', include('faculty.urls'))
    
    
]
