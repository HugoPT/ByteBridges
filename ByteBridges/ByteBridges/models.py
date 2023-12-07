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
    nif = models.CharField(max_length=9, unique=True)
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
    profitmargin = models.FloatField()
    barcode = models.CharField(max_length=13)
    serialnumber = models.CharField(max_length=100)
    reference = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        # Specify the table name
        db_table = 'articles'


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


class CompanyAPI(models.Model):
    result = models.CharField(max_length=255)
    nif_validation = models.BooleanField()
    is_nif = models.BooleanField()
    records_nif = models.BigIntegerField(primary_key=True)
    records_seo_url = models.CharField(max_length=255)
    records_title = models.CharField(max_length=255)
    records_address = models.TextField()
    records_pc4 = models.CharField(max_length=10)
    records_pc3 = models.CharField(max_length=10)
    records_city = models.CharField(max_length=255)
    records_start_date = models.DateField()
    records_activity = models.TextField()
    records_status = models.CharField(max_length=255)
    records_cae = models.JSONField()
    records_contacts_email = models.EmailField()
    records_contacts_phone = models.CharField(max_length=20)
    records_contacts_website = models.URLField()
    records_contacts_fax = models.CharField(max_length=20)
    records_structure_nature = models.CharField(max_length=255)
    records_structure_capital = models.DecimalField(max_digits=10, decimal_places=2)
    records_structure_capital_currency = models.CharField(max_length=3)
    records_geo_region = models.CharField(max_length=255)
    records_geo_county = models.CharField(max_length=255)
    records_geo_parish = models.CharField(max_length=255)
    records_place_address = models.TextField()
    records_place_pc4 = models.CharField(max_length=10)
    records_place_pc3 = models.CharField(max_length=10)
    records_place_city = models.CharField(max_length=255)
    records_racius = models.URLField()
    records_alias = models.CharField(max_length=255)
    records_portugalio = models.URLField()

    credits_used = models.CharField(max_length=255)
    credits_left = models.JSONField()
