from cProfile import label
from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import Author, Title, Publisher, Edition, ISBN, Student, Transaction


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'
        
        labels = {
            'name': '',
            'address': '',
            'telephone': '',
            'email': '',
            'alternative_telephone': '',
            'alternative_email': '',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Full Name' }),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Office Address' }),
            'telephone': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Telephone' }),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Email address' }),
            'alternative_telephone': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Additional Telephone (Optional))' }),
            'alternative_email': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Additional Email (Optional)' }),
        }
        
        
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        
        labels = {
            'name': '',
            'nationality': '',
            'email': '',
            'date_of_birth': '',
            'details': '',
        }  
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Full Name' }),
            'nationality': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter nationality' }),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter email address' }),
            'date_of_birth': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Date of Birth (Optional)' }),
            'details': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter more deatils (Optional)' }),
        }
        

class TitleForm(ModelForm):
    class Meta:
        model = Title
        fields = '__all__'
        
        labels = {
            'title': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Title of the Book' }),
        }

class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = '__all__'
        
        
        
class ISBNForm(forms.ModelForm):
    class Meta:
        model = ISBN
        fields = '__all__'
        
        
class StudentForm(forms.ModelForm):
    FACULTY_CHOICES = (('BEX','BEX'),('BCT','BCT'),('BCE','BCE'),('BEI','BEI'),)
    class Meta:
        model = Student
        exclude = ('issued_count', 'fine_status')
        
        labels = {
            'year_joined':'',
            'roll_no': '',
            'name': '',
            'phone': '',
            'email': '',
            'address': '',
        }
        widgets = {
            'year_joined': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Joined Year (eg. 078)' }),
            'roll_no': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Roll No. (eg. 004)' }),
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Full Name' }),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Phone Number' }),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter email address' }),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Home address' }),
        }
        
        
class IssueBookForm(forms.Form):
    isbnf = forms.ModelChoiceField(queryset = ISBN.objects.all(), empty_label="Search and Select Barcode", label='ISBN')
    studentf = forms.ModelChoiceField(queryset = Student.objects.all(), empty_label="Search and Select Student", label="Student")
    
    
    

