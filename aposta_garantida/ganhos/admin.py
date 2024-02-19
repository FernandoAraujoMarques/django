from django.contrib import admin
from .models import Member, Saldo, Aposta, Contas

# Register your models here.
admin.site.register(Member)
admin.site.register(Saldo)
admin.site.register(Aposta)
admin.site.register(Contas)
