from django.contrib import admin
from django.urls import path, include
from apps.manager.views import index

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('api/manager/', include('apps.manager.urls')),
    path('docs/', schema_view),
]
