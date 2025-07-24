from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.urls import path, include

def home(request):
    return HttpResponse("<h1>Hello from Render Django!</h1>")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),
]
