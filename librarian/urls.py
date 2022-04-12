from django.urls import path
from . import views
from .views import vlogin, viewlogout, vhomepage

urlpatterns = [
    path('', vlogin, name='login-page'),
    path('login', vlogin, name='login-page'),
    path('logout', viewlogout, name='logout-page'),
    
    path('home', vhomepage, name='home-page'),
    
    path('add_author/', views.addauthor, name='aa-page'),
    path('view_authors/', views.viewauthors, name='va-page'),
    path('edit_author/<author_id>/', views.editauthor, name='ea-page'),
    path('delete_author/<author_id>/', views.deleteauthor, name='da-page'),
    
    path('add_publications/', views.addpublisher, name='ap-page'),
    path('view_publications/', views.viewpublishers, name='vp-page'),
    path('edit_publication/<publisher_id>/', views.editpublisher, name='ep-page'),
    path('delete_publication/<publisher_id>/', views.deletepublisher, name='dp-page'),
    
    path('add_title/', views.addtitle, name='at-page'),                                 #Note: add / to end of url if it needs to access another database info
    path('view_titles/', views.viewtitles, name='vt-page'),
    path('edit_title/<title_id>/', views.edittitle, name='et-page'),
    path('delete_title/<title_id>/', views.deletetitle, name='dt-page'),
    
    path('add_edition/', views.addedition, name='ae-page'),
    path('view_edition/', views.vieweditions, name='ve-page'),
    path('edit_edition/<edition_id>/', views.editedition, name='ee-page'),
    path('delete_edition/<edition_id>/', views.deleteedition, name='de-page'),
    
    path('add_isbn/', views.addisbn, name='ai-page'),
    path('view_isbns/', views.viewisbns, name='vi-page'),
    path('edit_isbn/<isbn_id>/', views.editisbn, name='ei-page'),
    path('delete_isbn/<isbn_id>/', views.deleteisbn, name='di-page'),
    
    path('add_student/', views.addstdnt, name='as-page'),
    path('view_students/', views.viewstudents, name='vs-page'),
    path('edit_student/<int:student_id>/', views.editstudent, name='es-page'),
    path("delete_student/<int:student_id>/", views.deletestudent, name="delete_student"),
    
    path('view_issued_books/', views.viewissuedbooks, name='vib-page'),
    path('issue_a_book/', views.issueabook, name='iab-page'),
    path('return_book/<int:transaction_id>/', views.returnabook, name='rab-page'),
    
    path('fine_section/', views.finerecord, name='fs-page'),
    path('clear_fine/<int:transaction_id>/', views.clearfine, name='cf'),
    
]