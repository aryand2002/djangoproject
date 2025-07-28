from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.urls import path, include
from myapp.views import *
from rest_framework_simplejwt.views import TokenRefreshView

from django.conf import settings


def home(request):
    return HttpResponse("<h1>Hello from Render Django!</h1>")

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('', home),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('decorations/', DecorationListCreateAPIView.as_view(), name='decoration-list-create'),
    path('decorations/<int:pk>/', DecorationDetailAPIView.as_view(), name='decoration-detail'),
    path('catalog/', CatalogItemAPIView.as_view(), name='catalog-api'),
    path('blog/', BlogPostAPIView.as_view(), name='blog-api'),
    path('upload-gallery/', GalleryUploadView.as_view(), name='upload-gallery'),
]
