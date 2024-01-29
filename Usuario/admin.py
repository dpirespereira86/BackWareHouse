from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Usuario.models import Usuario
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('first_name','last_name','email','empresa')
    model = Usuario
    fieldsets =(
        (None, {'fields':('email','password')}),
        ('Informações Pessoais', {'fields': ('first_name','last_name','empresa')}),
        ('Permissões', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login','date_joined')}),
    )


