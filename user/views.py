from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp import models as myapp_models
from myadmin import models as myadmin_models
from user import models as user_models
from django.db.models import Max
from . import models
import time

#middleware sessioncheck for user routes:
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path == '/user/userabout/' or request.path=='/user/funds/' or request.path=='/user/payment/' or request.path=='/user/success/' or request.path=='/user/cancel/' or request.path == '/user/epuser/' or request.path=='/user/cpuser/':
			if request.session['sunm'] == None or request.session['srole']!="user":
				response = redirect('/Login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)
		return response
	return middleware


def userhome(request):
	clist=myadmin_models.Category.objects.all()
	return render(request,"userhome.html",{"sunm":request.session['sunm'],"clist":clist})

def userabout(request):
	udetails=myapp_models.Register.objects.filter(email=request.session['sunm'])
	return render(request,"userabout.html",{"sunm":request.session['sunm'],"udetails":udetails[0]})

def cpuser(request):
	if request.method=="GET":
		return render(request,"cpuser.html",{"sunm":request.session['sunm']})
	else:
		opassword=request.POST.get("opassword")
		npassword=request.POST.get("npassword")
		cnpassword=request.POST.get("cnpassword")
		sunm=request.session["sunm"]

		userdetails=myapp_models.Register.objects.filter(email=sunm,password=opassword)
		
		if len(userdetails)>0:
			if npassword==cnpassword:
				myapp_models.Register.objects.filter(email=sunm).update(password=cnpassword)
				msg="Password changed successfully...."
			else:
				msg="New & Confirm new password mismatch"
		else:
			msg="Old password not matched"
		return render(request,"cpuser.html",{"sunm":request.session['sunm'],"output":msg})

def epuser(request):
	if request.method=="GET":
		userdetails=myapp_models.Register.objects.filter(email=request.session["sunm"])
		return render(request,"epuser.html",{"sunm":request.session['sunm'],"userdetails":userdetails[0]})
	else:
		name=request.POST.get("name")
		mobile=request.POST.get("number")
		email=request.POST.get("email")
		password=request.POST.get("password")
		address=request.POST.get("address")
		city=request.POST.get("city")
		gender=request.POST.get("gender")
         
	    #update record in databse table
		myapp_models.Register.objects.filter(email=request.session["sunm"]).update(name=name,mobile=mobile,address=address,city=city,gender=gender)
		return redirect("/user/epuser")
    

def funds(request):
	paypalURL="http://www.sandbox.paypal.com/cgi-bin/webscr"
	paypalID="sb-17hjc29126034@business.example.com"
	amt=1000
	# sb-apjnt29770980@personal.example.com 12345678
	return render(request,"funds.html",{"paypalURL":paypalURL, "paypalID":paypalID, "amt":amt, "sunm":request.session['sunm']})

def payment(request):
	uid=request.GET.get("uid")
	amt=request.GET.get("amt")
	p=models.Payment(uid=uid,amt=int(amt),info=time.asctime())
	p.save()
	return redirect("/user/success/")

def success(request):
	return render(request,"success.html",{"sunm":request.session['sunm']})

def cancel(request):
	return render(request,"cancel.html",{"sunm":request.session['sunm']})

def searchcat(request):
	clist=myadmin_models.Category.objects.all()
	return render(request,"searchcat.html",{"sunm":request.session['sunm'],"clist":clist})

def searchsubcat(request):
	catname=request.GET.get("catname")
	sclist=myadmin_models.SubCategory.objects.filter(catname=catname)
	clist=myadmin_models.Category.objects.all()
	return render(request,"searchsubcat.html",{"catname":catname,"sclist":sclist,"clist":clist,"sunm":request.session['sunm']})

def searchproduct(request):
	scname=request.GET.get("scname")
	plist=myadmin_models.Product.objects.filter(subcatname=scname)
	return render(request,"searchproduct.html",{"sunm":request.session['sunm'],"plist":plist})

def bidstatus(request):
	cart=0
	sunm=request.session['sunm']
	pid=int(request.GET.get("pid"))
	pDetails=myadmin_models.Product.objects.filter(pid=pid)
	dtime=time.time()-int(pDetails[0].info)
	hour_diff=divmod(dtime,3600)[0]
	if hour_diff<=48:
		return render(request,"bidnow.html",{"sunm":request.session['sunm'],"pDetails":pDetails[0],"pid":pid})
	else:
		highest_bid = user_models.Bidding.objects.filter(bidd_product_ID=pid).aggregate(max_bid=Max('bidd_price'))['max_bid']
		p_id=user_models.Bidding.objects.filter(bidd_price=highest_bid,bidd_product_ID=pid)
		msg=("Sorry, Bidding time is over!!!!")
		if p_id[0].bidder_email==sunm:
			cart=1
		else:
			cart=0
		# print(p_id[0].bidd_product_ID)
	return render(request,"bidstatus.html",{"sunm":request.session['sunm'],"cart":cart,"p_id":p_id[0],"output":msg})


def bidnow(request):
	pid=int(request.GET.get("pid"))
	bDetails=myadmin_models.Product.objects.filter(pid=pid)	
	if request.method=="GET":
		return render(request,"bidnow.html",{"sunm":request.session['sunm'],"bDetails":bDetails[0]})
	else:
         bidder_name=request.POST.get("bidder_name")
         bidder_mobile=request.POST.get("bidder_mobile")
         bidd_price=request.POST.get("bidd_price")
         bidder_email=request.POST.get("bidder_email")
         #insert record in databse table
         p=models.Bidding(bidder_name=bidder_name,bidder_mobile=bidder_mobile,bidder_email=bidder_email,bidd_product_ID=bDetails[0].pid,bidd_product=bDetails[0].ptitle,bidd_price=bidd_price,product_icon=bDetails[0].piconname,info=time.asctime())
         p.save()
         return render(request,"bidnow.html",{"sunm":request.session['sunm'],"bDetails":bDetails[0],"Output":"User Register Successfullly.........!"})

def cart(request):
	b_id=request.GET.get("b_id")
	details=user_models.Bidding.objects.filter(bid_id=b_id)
	p_title=details[0].bidd_product
	title=myadmin_models.Product.objects.filter(ptitle=p_title)
	if not user_models.Cart.objects.filter(bidd_ID=details[0].bid_id,product=details[0].bidd_product).exists():
		x=models.Cart(email=details[0].bidder_email,bidd_ID=details[0].bid_id,product=details[0].bidd_product,price=details[0].bidd_price)
		x.save()
	return render(request,"cart.html",{"sunm":request.session['sunm'],"details":details[0],"title":title[0]})


def checkout(request):
	ID=request.GET.get("ID")
	z=user_models.Cart.objects.filter(bidd_ID=ID)
	return render(request,"checkout.html",{"sunm":request.session['sunm'],"z":z[0]})

def ordersuccess(request):
	return render(request,"ordersuccess.html",{"sunm":request.session['sunm']})

def orderpayment(request):
	paypalURL="http://www.sandbox.paypal.com/cgi-bin/webscr"
	paypalID="sb-17hjc29126034@business.example.com"
	iD=request.GET.get("ID")
	w=user_models.Cart.objects.filter(bidd_ID=iD)
	return render(request,"orderpayment.html",{"sunm":request.session['sunm'],"w":w[0],"amt":w[0].price,"paypalURL":paypalURL, "paypalID":paypalID})
