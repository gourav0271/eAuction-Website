from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from . import emailAPI
from . import models
import time


#middleware sessioncheck for mainapp routes:
def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path=='/Home/' or request.path == '/About/' or request.path=='/Services/' or request.path=='/Register/' or request.path=='/Contact/' or request.path=='/Login/':
            request.session['sunm']=None
            request.session['srole']=None
            response=get_response(request)
        else:
            response=get_response(request)
        return response
    return middleware

urlRoute = """<h2>Click below to redirect<h2>
<a href="/">Home Page</a><br/><br/>
<a href="/Contact/">Contact Page</a><br/><br/>
<a href="/Login/">Login Page</a><br/><br/>
<a href="/Services/">Services Page</a><br/><br/>
<a href="/Register/">Register Page</a><br/><br/>
<a href="/About/">About Page</a><br/><br/>
"""

def Home(request):
    return render(request, "index.html")

def About(request):
    return render(request, "about.html")

def Services(request):
    return render(request, "services.html")

def Contact(request):
    return render(request, "contact.html")

def Register(request):
    if request.method == 'GET': 
        return render(request, "register.html",{"Output":""})
    else:
         name=request.POST.get("name")
         mobile=request.POST.get("number")
         email=request.POST.get("email")
         password=request.POST.get("password")
         address=request.POST.get("address")
         city=request.POST.get("city")
         gender=request.POST.get("gender")

         #to send verification email
         emailAPI.sendMail(email,password)
         #insert record in databse tab  le

         p=models.Register(name=name,mobile=mobile,email=email,password=password,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
         p.save()
         return render(request,"register.html",{"Output":"User Register Successfullly.........!"})
    
def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)
    return redirect("/Login/")

def Login(request):
    cunm,cpass="","";
    if request.COOKIES.get("cunm") != None:
     cunm=request.COOKIES.get("cunm")
     cpass=request.COOKIES.get("cpass")
    if request.method=="GET":
        return render(request, "login.html",{"cunm":cunm, "cpass":cpass, "Output":""})
    else:        
        email=request.POST.get("email")
        password=request.POST.get("password")
        chk=request.POST.get("chk")
        userdetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userdetails)>0:
            #set session for the user after login
            #to store user details in session
            request.session["sunm"]=userdetails[0].email
            request.session["srole"]=userdetails[0].role

            if userdetails[0].role=="admin":
                response = redirect("/myadmin/")
            else:
                response = redirect("/user/")

            # to store cookies in response
            if chk != None:
                response.set_cookie("cunm",userdetails[0].email,3600)
                response.set_cookie("cpass",userdetails[0].password,3600)
            return response;zz
        else:
             return render(request, "login.html",{"Output":"Invalid user or verify your account..."})
        
def ajaxresponse(request):
    return HttpResponse("<h1>Ajax is working............</h1>")

def checkEmailAJAX(request):
    email=request.GET.get("email")
    userDetails=models.Register.objects.filter(email__startswith=email)
    flag=0
    if len(userDetails)>0:
        flag=1
    return HttpResponse(flag) 