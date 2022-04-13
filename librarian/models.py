from tkinter import CASCADE
from django.db import models
from datetime import datetime,timedelta
from django.utils import timezone
# from django.contrib.auth.models import User


class Publisher(models.Model):
    #Publisher_id = models.BigAutoField(primary_key=True)  As django create model pk id by default auto increment integer, this code can be used to set manual pk.
    name = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=75, unique=True)
    alternative_telephone = models.CharField(max_length=15, blank=True)
    alternative_email = models.EmailField(max_length=75, blank=True)
    def __str__(self):
        return self.name + ' - ' + self.address

class Author(models.Model):
    name= models.CharField(max_length=30)
    nationality= models.CharField(max_length=30)
    email = models.EmailField(max_length=75, unique=True)
    date_of_birth= models.CharField(max_length=30, blank=True)
    details=models.CharField(max_length=1000, blank=True)
    def __str__(self):
            return self.name + ' , ' + self.nationality

class Title(models.Model):
    name = models.CharField(max_length=100)                                            #use ManyToManyField for many-many relation
    author = models.ManyToManyField(Author)                                            #one author may publish many books and one book may be published by many author, both relation may exists.
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)                 #One publisher may publish many books & one book with same title may be published by many publisher, both relation may exists.
    def __str__(self):                                                                 #Note: use OneToOneField if only single to single link exists      
     return self.name + ' - By ' + str(self.publisher)                                 #Note: use ForeignKey in child class if either one to many or many to one relation exists, not both relation.


class Edition(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    which_edition = models.CharField(max_length=10)
    price_in_Rs = models.IntegerField()
    cover = models.ImageField(upload_to='static/covers', blank=True)
    pdf = models.FileField(upload_to='static/pdfs/', blank=True)
    def __str__(self):
        return self.which_edition + ' edition: ' + str(self.title)

    def delete(self, *args, **kwargs):
        self.cover.delete()
        self.pdf.delete()
        super().delete(*args, **kwargs)

class ISBN(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)       #Many ISBN can have one same edition ->> ForeignKey
    def __str__(self):
        return self.barcode


class Student(models.Model):
    # user = models.OneToOneField(User)
    year_joined = models.CharField(max_length=4)
    FACULTY_CHOICES = (('BEX','BEX'),('BCT','BCT'),('BCE','BCE'),('BEI','BEI'),)
    branch = models.CharField(max_length=6,choices=FACULTY_CHOICES)
    roll_no = models.CharField(max_length=3)
    name= models.CharField(max_length=50)
    GENDER_CHOICES = (("M", "Male"),("F", "Female"),("Other", "Other"))
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=75, unique=True)
    address = models.CharField(max_length=1024)
    issued_count = models.IntegerField(default=0)
    fine_status = models.BooleanField(default=False)
    def __str__(self):
        return 'SEC' + self.year_joined + '' + self.branch + '' + self.roll_no + ' - ' + self.name
    


def get_expiry():
    return datetime.today() + timedelta(days=15)

class Transaction(models.Model):
     student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
     isbn = models.ForeignKey(ISBN, on_delete=models.CASCADE, null=True)                           # OneToOneField !!!!!!!!!
     issued_date = models.DateField(auto_now=True)
     due_date = models.DateField(default=get_expiry)
     returned_status = models.BooleanField(default=False)
     returned_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
     
     fine = models.IntegerField(null=True, default=0)

     def __str__(self):
        return str(self.student)











'''
class Alltransaction(models.Model):
     issued_date = models.DateField(auto_now=True)
     due_date = models.DateField(default=get_expiry)
     fine = models.IntegerField(null=True, blank=True)
     returned_status = models.BooleanField(default=False)
     returned_date = models.DateTimeField(auto_now=True, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    issued_date = models.DateField(default=timezone.now)
    returned_date = models.DateTimeField(default=None, blank=True)
    fine = models.IntegerField(blank=True)
    
    def __str__(self):
        return str(self.student)
        
        if(return_date>due_date):
            temp = return_date - due_date
        else:
         temp = 0
'''
    #use sql or django ORM to get the difference between dates