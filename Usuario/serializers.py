from rest_framework import serializers
from .models import Usuario




class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields=('first_name','last_name','email','empresa','password')