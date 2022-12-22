from django.db import models

# # Create your models here.
# class Invoice(models.Model):
#     InvoiceNo = models.CharField(max_length=50, primary_key=True)
#     InvoiceDate = models.DateTimeField()
#     CustomerID = models.CharField(max_length=50)
#     Country = models.CharField(max_length=50)

# class Stock(models.Model):
#     StockCode = models.CharField(max_length=50, primary_key=True)
#     Description = models.CharField(max_length=50)
#     UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)

# class Compose(models.Model):
#     Quantity = models.IntegerField()
#     InvoiceNo = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     StockCode = models.ForeignKey(Stock, on_delete=models.CASCADE)

# class Meta:
#     unique_together = ('InvoiceNo','StockCode')
