from .models import Empresa

def generic_get_empresa_rz(rz):
    empresa = Empresa.objects.get(razao_social=rz)
    return empresa
def generic_get_empresa_id(id):
    empresa = Empresa.objects.get(id=id)
    return empresa