from django.contrib import admin
# Register your models here.
from .models import Publisher, Author, Edition, ISBN, Title, Student, Transaction 

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Title)
admin.site.register(Edition)
admin.site.register(ISBN)
# admin.site.register(Student)
# admin.site.register(Transaction)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site) -> None:
        self.list_display = [str(field.name) for field in Transaction._meta.fields]
        super().__init__(model, admin_site)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site) -> None:
        self.list_display = [str(field.name) for field in Student._meta.fields]
        super().__init__(model, admin_site)