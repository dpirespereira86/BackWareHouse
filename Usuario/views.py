
from rest_framework import viewsets, status
from rest_framework.views import APIView
import requests
from .models import Usuario
from .serializers import UserSerializers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema



# Create your views here.
class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        print(request.data)
        user = request.data.copy()
        user.__setitem__('username', request.data['email'])
        print(user)
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ObtainAuthToken(APIView):
    """
    Sobrescrita do metodo original do python para retorno do token a partir do username e password

    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(username=request.data['username'])
        empresa = requests.get(f'http://127.0.0.1:8080/api/v1/empresa/{usuario.empresa}').json()
        """
        Verifica de a empresa está ativa e habilitada para wms
        
        """
        print('Passaei aqui')
        if empresa['wms'] == True and empresa['ativo'] == True :
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
           return Response({'token': 'Acesso não Autorizado'})


obtain_auth_token = ObtainAuthToken.as_view()


