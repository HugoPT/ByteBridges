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
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'families'


class Category(models.Model):
    idcategory = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'categories'


class Labor(models.Model):
    idlabor = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=80)
    hourrate = models.FloatField()

    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'labors'


class Article(models.Model):
    idarticle = models.AutoField(primary_key=True, unique=True)
    idfamily = models.IntegerField()
    idwarehouse = models.IntegerField()
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1024)
    cost = models.FloatField()
    profitmargin = models.FloatField()
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
    equipment = models.CharField(max_length=80)
    idequipment = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=500)
    cost = models.IntegerField()
    serialnumber = models.CharField(max_length=100)
    image = models.CharField(max_length=1024)
    profitmargin = models.FloatField()
    barcode = models.CharField(max_length=13)
    reference = models.CharField(max_length=30)
    category = models.CharField(max_length=80)  # Assuming the data type for the family field
    warehouse = models.CharField(max_length=80)  # Assuming the data type for the warehouse field


    def __str__(self):
        return self.equipment

    class Meta:
        # Specify the table name
        db_table = 'equipments'


class User(models.Model):
    iduser = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=100)
    role = models.IntegerField()
    labor = models.IntegerField()


    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'users'