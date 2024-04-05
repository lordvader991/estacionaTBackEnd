from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'email', 'password', 'phone', 'rol_usuario', 'correo_auth']
    extra_kwargs = {
        'password': {'write_only': True},
        'email': {'required': True},
    }
    def update(self,instance, validated_data):
        if 'passowrd' in validated_data:
            password = validated_data.pop('password')
        return super().update(instance, validated_data)
