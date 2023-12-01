from django.db import models


class Supplier(models.Model):
    idsupplier = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    nif = models.TextField()
    email = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    zipcode = models.CharField(max_length=100, unique=True)
    city = models.TextField()
    phone = models.TextField()
    obs = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        # Specify the table name
        db_table = 'suppliers'