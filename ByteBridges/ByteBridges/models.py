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
    idclient = models.AutoField(primary_key=True) 
    email = models.EmailField(max_length=70, unique=True)
    individual = models.BooleanField(default=False)
    zipCode = models.CharField(max_length=8)
    address = models.CharField(max_length=120)
    nif = models.CharField(max_length=9,unique=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    city = models.CharField(max_length=80)
    eletronicinvoice = models.BooleanField(default=False)
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
    name = models.CharField(max_length=70)
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
        
class ComponentListFamily(models.Model):
    at_id = models.IntegerField(primary_key=True)  
    at_name = models.CharField(max_length=80)

    def __str__(self):
        return self.at_name

    class Meta:
        # Specify the table name
        db_table = 'fn_components_list_family'  
        
class ArticleType(models.Model):
    idarticletype = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    idfamily = models.IntegerField()  # Assuming the data type for the family field
    idcategory = models.IntegerField()  # Assuming the data type for the family field
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1024)
    profitmargin = models.FloatField()
    barcode = models.CharField(max_length=13)
    reference = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        # Specify the table name
        db_table = 'articletypes'


class Equipment(models.Model):
    idEquipment = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    family = models.CharField(max_length=120)  # Assuming the data type for the family field
    warehouse = models.CharField(max_length=80)  # Assuming the data type for the warehouse field
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1024)
    cost = models.IntegerField()
    profitmargin = models.FloatField()
    barcode = models.CharField(max_length=13)
    serialnumber = models.CharField(max_length=100)
    reference = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        # Specify the table name
        db_table = 'view_equipments_list'


