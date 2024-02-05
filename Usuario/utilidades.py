from .models import Usuario

def generic_get_usuario_email(email):
    usuario = Usuario.objects.get(email=email)
    return usuario
def generic_get_usuario_id(id):
    usuario = Usuario.objects.get(id=id)
    return usuario