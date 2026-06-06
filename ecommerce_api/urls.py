from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import client_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # API per il login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API delle nostre App
    path('api/users/', include('users.urls')),
    path('api/shop/', include('shop.urls')),

    # Pagina web frontend
    path('', client_view, name='client'),
]