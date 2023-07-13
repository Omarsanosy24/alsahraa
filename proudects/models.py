from django.db import models

# Create your models here.
class Category(models.Model):
    mainCategory = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        )
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    def __str__(self):
        return self.name_ar

class Product(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description_ar = models.TextField()
    description_en = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        limit_choices_to={"mainCategory__isnull":False}
        )
    def __str__(self):
        return self.name_ar


class Image(models.Model):
    image = models.ImageField(upload_to='products/', default='products/face2028-eb00-4b01-be75-a4fc537a10dc.jpeg')
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return self.product.name_ar
class Banners(models.Model):
    image = models.ImageField(upload_to='banners')

    def __str__(self) -> str:
        return self.image



