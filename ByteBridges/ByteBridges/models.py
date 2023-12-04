from django.db import models


class Supplier(models.Model):
    idsupplier = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    nif = models.TextField()
    address = models.TextField()
    zipcode = models.CharField(max_length=100, unique=True)
    city = models.TextField()
    phone = models.TextField()
    email = models.CharField(max_length=100, unique=True)
    obs = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'suppliers'
        
    
class Client(models.Model):
    email = models.EmailField(max_length=70, unique=True)
    zipCode = models.CharField(max_length=8, unique=True)
    address = models.CharField(max_length=120)
    nif = models.CharField(max_length=9,unique=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    city = models.CharField(max_length=80)

    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'clients'
        
class Warehouse(models.Model):
    idwarehouse = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    zipcode = models.CharField(max_length=8)
    phone = models.CharField(max_length=9)
    
    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'warehouse'
              
class Family(models.Model):
    idfamily = models.AutoField(primary_key=True, unique=True)
    namefamily = models.CharField(max_length=70)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.namefamily
    class Meta:
        # Specify the table name
        db_table = 'families'        
        
class Article(models.Model):
    idarticle = models.AutoField(primary_key=True, unique=True)
    idfamily = models.IntegerField()
    idwarehouse = models.IntegerField()
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1024)
    cost = models.FloatField()
    profitmargin =models.FloatField()
    barcode = models.CharField(max_length=13)
    serialnumber = models.CharField(max_length=100)
    reference = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    class Meta:
        # Specify the table name
        db_table = 'articles'