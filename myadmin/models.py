from django.db import models

class Category(models.Model):
     catid=models.AutoField(primary_key=True)
     catname=models.CharField(max_length=50,unique=True)
     caticonname=models.CharField(max_length=100)
     
class SubCategory(models.Model):
     subcatid=models.AutoField(primary_key=True)
     catname=models.CharField(max_length=50)
     subcatname=models.CharField(max_length=50,unique=True)
     subcaticonname=models.CharField(max_length=100)

class Product(models.Model):
     pid=models.AutoField(primary_key=True)
     ptitle=models.CharField(max_length=50)
     subcatname=models.CharField(max_length=50)
     pdescription=models.CharField(max_length=150)
     pbprice=models.IntegerField()
     piconname=models.CharField(max_length=100)
     info=models.IntegerField()

