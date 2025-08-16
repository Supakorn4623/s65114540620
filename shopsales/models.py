from django.db import models
from django.utils.timezone import now


class Product(models.Model):
    id = models.AutoField(primary_key=True)  
    product_code = models.CharField(max_length=100, unique=True)  
    product_name = models.CharField(max_length=255)  
    price = models.PositiveIntegerField()  
    stock = models.PositiveIntegerField (default=0,blank=True, null=True)  

    def __str__(self):
        return f"{self.product_name} ({self.product_code})"
    
class Shelf(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # เชื่อมกับ Product
    shelf_quantity = models.PositiveIntegerField(default=0)  # จำนวนที่ขึ้นชั้นวาง
    created_date = models.DateTimeField(default=now)  # วันที่เพิ่มสินค้าขึ้นชั้นวาง

    def __str__(self):
        return f"{self.product.product_name} - {self.shelf_quantity} ชิ้น"
