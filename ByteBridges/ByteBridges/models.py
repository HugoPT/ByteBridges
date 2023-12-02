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
    nif = models.CharField(unique=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    city = models.CharField()

    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'Clients'
