from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp import models as myapp_models
from myadmin import models as myadmin_models
from django.core.files.storage import FileSystemStorage
from . import models
import time

#middleware sessioncheck for admin routes:
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path == '/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/'  or request.path=='/myadmin/addsubcategory/' or request.path=='/myadmin/addproduct/':
			if request.session['sunm'] == None or request.session['srole']!="admin":
				response = redirect('/Login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)
		return response
	return middleware


def adminhome(request):
	return render(request,"adminhome.html",{"sunm":request.session['sunm']})

def manageusers(request):
	userdetails=myapp_models.Register.objects.filter(role="user")
	return render(request,"manageusers.html",{"userdetails":userdetails,"sunm":request.session['sunm']})

def manageuserstatus(request):
	regid=int(request.GET.get("regid"))
	status=int(request.GET.get("status"))
	if status==1:
		myapp_models.Register.objects.filter(regid=regid).update(status=status)
	elif status==0:
		myapp_models.Register.objects.filter(regid=regid).update(status=status)
	else:
		myapp_models.Register.objects.filter(regid=regid).delete()
	return redirect("/myadmin/manageusers/")

def addcategory(request):
	if request.method=="GET":
		return render(request,"addcategory.html",{"sunm":request.session['sunm']})
	else:
		catname=request.POST.get("catname")
		caticon=request.FILES["caticon"]
		fs=FileSystemStorage()
		filename=fs.save(caticon.name,caticon)
		p=models.Category(catname=catname,caticonname=filename)
		p.save()
		return render(request,"addcategory.html",{"sunm":request.session['sunm'],"output":"Category Added successfully.."})

def addsubcategory(request):
	clist=models.Category.objects.all()
	if request.method=="GET":
		return render(request,"addsubcategory.html",{"sunm":request.session['sunm'],"output":"","clist":clist})
	else:
		catname=request.POST.get("catname")
		subcatname=request.POST.get("subcatname")
		subcaticon=request.FILES["subcaticon"]
		fs=FileSystemStorage()
		filename=fs.save(subcaticon.name,subcaticon)
		p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticonname=filename)
		p.save()
		return render(request,"addsubcategory.html",{"sunm":request.session['sunm'],"output":"SubCategory Added successfully..","clist":clist})


def addproduct(request):
	sclist=models.SubCategory.objects.all()
	if request.method=="GET":
		return render(request,"addproduct.html",{"sunm":request.session['sunm'],"output":"","sclist":sclist})
	else:
		ptitle=request.POST.get("ptitle")
		subcatname=request.POST.get("subcatname")
		pdescription=request.POST.get("pdescription")
		pbprice=request.POST.get("pbprice")
		picon=request.FILES["picon"]
		ptime=request.POST.get("ptime")
		fs=FileSystemStorage()
		filename=fs.save(picon.name,picon)
		p=models.Product(ptitle=ptitle,subcatname=subcatname,pdescription=pdescription,pbprice=pbprice,piconname=filename,info=time.time())
		p.save()
		return render(request,"addproduct.html",{"sunm":request.session['sunm'],"output":"Product Added Successfully","sclist":sclist})


def seeaddedproducts(request):
	scname=request.GET.get("scname")
	plist=myadmin_models.Product.objects.filter(subcatname=scname)
	return render(request,"seeaddedproducts.html",{"sunm":request.session['sunm'],"plist":plist})

def cpadmin(request):
	if request.method=="GET":
		return render(request,"cpadmin.html",{"sunm":request.session['sunm']})
	else:
		opassword=request.POST.get("opassword")
		npassword=request.POST.get("npassword")
		cnpassword=request.POST.get("cnpassword")
		sunm=request.session["sunm"]
		admindetails=myapp_models.Register.objects.filter(email=sunm,password=opassword)
		
		if len(admindetails)>0:
			if npassword==cnpassword:
				myapp_models.Register.objects.filter(email=sunm).update(password=cnpassword)
				msg="Password changed successfully...."
			else:
				msg="New & Confirm new password mismatch"
		else:
			msg="Old password not matched"
		return render(request,"cpadmin.html",{"sunm":request.session['sunm'],"output":msg})

def epadmin(request):
	if request.method=="GET":
		admindetails=myapp_models.Register.objects.filter(email=request.session["sunm"])
		return render(request,"epadmin.html",{"sunm":request.session['sunm'],"admindetails":admindetails[0]})
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
		return redirect("/myadmin/epadmin")
