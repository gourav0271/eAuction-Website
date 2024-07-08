from django.db import models

class Payments(models.Model):
     txnid=models.AutoField(primary_key=True)
     uid=models.CharField(max_length=50)
     amt=models.IntegerField()
     info=models.CharField(max_length=50)

class Bidding(models.Model):
     bid_id=models.AutoField(primary_key=True)
     bidder_name=models.CharField(max_length=50)
     product_icon=models.CharField(max_length=500)
     bidder_mobile=models.CharField(max_length=12)
     bidder_email=models.CharField(max_length=50)
     bidd_product_ID=models.CharField(max_length=10)
     bidd_product=models.CharField(max_length=50)
     bidd_price=models.CharField(max_length=10)
     info=models.CharField(max_length=50)

class Cart(models.Model):
     Id=models.AutoField(primary_key=True)
     email=models.CharField(max_length=50)
     bidd_ID=models.CharField(max_length=10)
     product=models.CharField(max_length=50)
     price=models.CharField(max_length=10)