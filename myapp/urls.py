from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.Home),
    path('Contact/', views.Contact),
    path('About/', views.About),
    path('Services/', views.Services),
    path('Register/', views.Register),
    path('checkEmailAJAX/', views.checkEmailAJAX),
    path('verify/', views.verify),
    path('Login/', views.Login),
    path('ajaxresponse/', views.ajaxresponse),
    path('myadmin/',include('myadmin.urls') ),
    path('user/',include('user.urls'))    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
