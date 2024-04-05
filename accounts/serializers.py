from rest_framework.serializers import ModelSerializer
from accounts.models import  User


class UserSerializer(ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['id','username', 'last_name', 'email','password', 'phone','rol_usuario','correo_auth']
        #fields = '__all__'
