from django.urls import path
from faculty import views
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
    # path('faculty/', views.allFaculty, name='allFaculty'),
    path('faculty/<str:user_id>', views.facultyById, name='facultyById'),
]
