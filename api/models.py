from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


# Create your models here.
class Products(models.Model):

    name=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    image=models.ImageField(null=True,upload_to="images")

    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
            return (sum(ratings)/len(ratings))
        else:
            return 0
    @property
    def total_ratings(self):
        totalrt=self.reviews_set.all().values_list("rating",flat=True)
        if totalrt:
            return (len(totalrt))
        else:
            return 0
    def __str__(self):
        return self.name


#python manage.py shell
#then we have to import

#ORM
#orm query for creating a resource
#modalname.objects.create(field1=value1,field2=value2....)
#produccts.objects.create(name="samsunga72",price=32000,description="mobile",category="electronics")


#ORM query for fetching all records
#qs=modelname.objects.all()


#ORM query for filter queries
#qs=modalname.objects.filter(category="electronics"

#ORM query for exclude
#qs=Products.objects.all().exclude(category="electronics"

#ORM query for fetching a specific record
#qs=modelname.objects.get(id=1)

#ORM query for update
#modelname.objects.filter(id=2).update(price=350)

#price>25000
#qs=Prodcuts.objects.filter(price=__lt=25000)

#Products in range of 20000 to 30000
#Prodcuts.objects.filter(condition1,condition2)

#return all categories
#Prodcuts.objects.values_list('category')

#return category with no duplicates
#Prodcuts.objects.values_list('category').distinct()


class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
        ("order-placed","order-placed"),
        ("in-cart","in-cart"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")



class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.comment



class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("order-placed","order-placed"),
        ("dispatched","dispatched"),
        ("in-transit","in-transit"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)