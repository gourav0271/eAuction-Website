from django.urls import path

from . import views
urlpatterns = [
    path('', views.userhome),
    path('userabout/', views.userabout),
    path('funds/', views.funds),
    path('payment/', views.payment),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('cpuser/', views.cpuser),              #cpuser=change password user
    path('epuser/', views.epuser),              #epuser=edit profile user
    path('searchcat/',views.searchcat),     #searchcat=search category
    path('searchsubcat/',views.searchsubcat), 
    path('searchproduct/',views.searchproduct),
    path('bidstatus/', views.bidstatus),
    path('bidnow/', views.bidnow),
    path('cart/', views.cart),
    path('checkout/', views.checkout),
    path('ordersuccess/', views.ordersuccess),
    path('orderpayment/', views.orderpayment),



]
