import contextvars
from pdb import post_mortem
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from . import models
from .models import Author, Publisher, Title, Edition, ISBN, Student, Transaction
from .forms import AuthorForm, PublisherForm, TitleForm, EditionForm, ISBNForm, StudentForm, IssueBookForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import date
# from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q

#Librarian

def vlogin(request):    
    if request.method =='POST':
       name = request.POST.get('uname')
       password = request.POST.get('passw')
       user = authenticate(request, username=name, password=password)
       if user is not None and user.is_active:
           login(request, user)
           return redirect('home-page')
       else:
           messages.error(request, 'Invalid username or password')
           return redirect('login-page')
    else:
        return render(request, 'librarian/login.html', {})
       
       
def viewlogout(request):
    logout(request)
    return redirect('login-page')


@login_required
def vhomepage(request):
	book = ISBN.objects.all().count()
	user = Student.objects.all().count()
	context = {'book':book, 'user':user}
	return render(request, 'librarian/index.html', context)





@login_required
def addauthor(request):
    submitted = False
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_author?submitted=True')
    else:
        form = AuthorForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'librarian/addbook/addauthor.html', {'form':form, 'submitted':submitted})

@login_required
def viewauthors(request):
    authors = Author.objects.all()
    return render(request, 'librarian/mngbook/mngauthor.html', {'authors':authors})

@login_required
def editauthor(request, author_id):
    object = Author.objects.get(id = author_id)
    form = AuthorForm(instance=object)
    if request.method == "POST":  
        form = AuthorForm(request.POST, instance=object)  
        if form.is_valid():  
            form.save()
            return redirect('va-page')
    return render(request,'librarian/mngbook/editauthor.html',{'form':form})

@login_required
def deleteauthor(request, author_id):
    obj = Author.objects.filter(id=author_id)
    obj.delete()
    return redirect('va-page')




@login_required
def addpublisher(request):
    submitted = False
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_publications?submitted=True')
    else:
        form = PublisherForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'librarian/addbook/addpublisher.html', {'form':form, 'submitted':submitted})

@login_required
def viewpublishers(request):
    publishers = Publisher.objects.all()
    return render(request, 'librarian/mngbook/mngpublisher.html', {'publishers':publishers})

@login_required
def editpublisher(request, publisher_id):
    object = Publisher.objects.get(id = publisher_id)
    form = PublisherForm(instance=object)
    if request.method == "POST":  
        form = PublisherForm(request.POST, instance=object)  
        if form.is_valid():  
            form.save()
            return redirect('vp-page')
    return render(request,'librarian/mngbook/editpublisher.html',{'form':form})

@login_required
def deletepublisher(request, publisher_id):
    obj = Publisher.objects.filter(id=publisher_id)
    obj.delete()
    return redirect('vp-page')



@login_required
def addtitle(request):
    submitted = False
    if request.method == "POST":
        form = TitleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_title?submitted=True')
    else:
        form = TitleForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'librarian/addbook/addtitle.html', {'form':form, 'submitted':submitted})

@login_required
def viewtitles(request):
    titles = Title.objects.all()
    return render(request, 'librarian/mngbook/mngtitle.html', {'titles':titles})

@login_required
def edittitle(request, title_id):
    object = Title.objects.get(id = title_id)
    form = TitleForm(instance=object)
    if request.method == "POST":  
        form = TitleForm(request.POST, instance=object)  
        if form.is_valid():  
            form.save()
            return redirect('vt-page')
    return render(request,'librarian/mngbook/edittitle.html',{'form':form})

@login_required
def deletetitle(request, title_id):
    obj = Title.objects.filter(id=title_id)
    obj.delete()
    return redirect('vt-page')




@login_required
def addedition(request):
    submitted = False
    if request.method == "POST":
        form = EditionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_edition?submitted=True')
    else:
        form = EditionForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'librarian/addbook/addedition.html', {'form':form, 'submitted':submitted})

@login_required
def vieweditions(request):
    editions = Edition.objects.all()
    return render(request, 'librarian/mngbook/mngedition.html', {'editions':editions})

@login_required
def editedition(request, edition_id):
    object = Edition.objects.get(id = edition_id)
    form = EditionForm(instance=object)
    if request.method == "POST":  
        form = EditionForm(request.POST, instance=object)  
        if form.is_valid():  
            form.save()
            return redirect('ve-page')
    return render(request,'librarian/mngbook/editedition.html',{'form':form})

@login_required
def deleteedition(request, edition_id):
    obj = Edition.objects.filter(id=edition_id)
    obj.delete()
    return redirect('ve-page')




@login_required
def addisbn(request):
    submitted = False
    if request.method == "POST":
        form = ISBNForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_isbn?submitted=True')
    else:
        form = ISBNForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'librarian/addbook/addisbn.html', {'form':form, 'submitted':submitted})

@login_required
def viewisbns(request):
    isbns = ISBN.objects.all()
    return render(request, 'librarian/mngbook/mngisbn.html', {'isbns':isbns})

@login_required
def editisbn(request, isbn_id):
    object = ISBN.objects.get(id = isbn_id)
    form = ISBNForm(instance=object)
    if request.method == "POST":  
        form = ISBNForm(request.POST, instance=object)  
        if form.is_valid():  
            form.save()
            return redirect('vi-page')
    return render(request,'librarian/mngbook/editisbn.html',{'form':form})

@login_required
def deleteisbn(request, isbn_id):
    obj = ISBN.objects.filter(id= isbn_id)
    obj.delete()
    return redirect('vi-page')




@login_required
def addstdnt(request):
    submitted = False
    if request.method == "POST":
        form = StudentForm(request.POST)  
        if form.is_valid():  
            form.save()
            subject = 'Library Membership Alert'
            message = "Hi " +  form.cleaned_data['name'] + ", You're successfully registered as a member in SEC Library. You can now borrow and return book by yourself with certain procedure inside the Library."
            recipient_email = form.cleaned_data['email']
            send_mail( subject, message, 'library.sagarmatha@gmail.com', [recipient_email], fail_silently=False )
            return HttpResponseRedirect('/add_student?submitted=True')   
    else:  
        form = StudentForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,'librarian/addstudent.html',{'form':form, 'submitted':submitted}) 

@login_required
def viewstudents(request):
    students = Student.objects.all()
    return render(request, "librarian/mngstudent/mngstudents.html", {'students':students})

@login_required
def editstudent(request, student_id):
    object = Student.objects.get(id = student_id)
    form = StudentForm(instance=object)
    if request.method == "POST":  
        form = StudentForm(request.POST, instance=object)  
        if form.is_valid():  
            form.save()
            return redirect('vs-page')
    return render(request,'librarian/mngstudent/editstudent.html',{'form':form})

@login_required
def deletestudent(request, student_id):
    obj = Student.objects.filter(id= student_id)
    obj.delete()
    return redirect('vs-page')


@login_required
def issueabook(request):
    form = IssueBookForm()
    if request.method == 'POST': 
        #now this form have data from htmlasasdasd
        form = IssueBookForm(request.POST)
        if form.is_valid():
            obj = Transaction()
            obj.student = form.cleaned_data['studentf']
            obj.isbn = form.cleaned_data['isbnf']
            count1 = obj.student.issued_count
            fine = obj.student.fine_status
            if count1<=2 and fine == False:
                obj.student.issued_count += 1
                print(obj.student.issued_count)           
                obj.save()
                # from gtts import gTTS
                # sound=gTTS('book issued')S
                # sound.save('book.mp3')
                return redirect('vib-page')
            else:
                messages.info(request, "Unable to issue a book. Either this student have already meet max borrowed limit or yet to clear fine.")
    return render(request,'librarian/mnltransaction/issueabook.html',{'form':form})

#           obj2 = Student.objects.filter(id=student_id)
#           if obj2.issued_count <= 2:
#            obj2.issued_count += 1


@login_required
def viewissuedbooks(request):
    try:
     issuedbooks = Transaction.objects.filter(returned_status=False)
    except Transaction.DoesNotExist as e:
        print(e)
    for isb in issuedbooks:
        days = (date.today()-isb.issued_date)   #fine calculation
        d = days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
            isb.fine = fine
            isb.student.fine_status = True
        isb.save()       
    return render(request,'librarian\mnltransaction\issuedbooks.html', {'issuedbooks':issuedbooks})
    
    
@login_required
def returnabook(request, transaction_id):
    obj = Transaction()
    obj = Transaction.objects.get(id= transaction_id)
    obj.student.issued_count -= 1               
    if obj.fine != 0:
        obj.returned_status = True
        obj.returned_date = date.today
    else:
        obj.delete()
    return redirect('vib-page')


@login_required
def finerecord(request):
    objs = Transaction.objects.filter(~Q(fine=None))
    return render(request, 'librarian/finerecord.html', {'objs':objs})


@login_required
def clearfine(request, transaction_id):
    obj = Transaction.objects.filter(id= transaction_id)
    #obj.student.fine_status = False
    obj.delete()
    return redirect('fs-page')


'''
@login_required
def vasearch(request):
    query = request.GET['query']
    print(type(query))
'''