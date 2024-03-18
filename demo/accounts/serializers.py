from rest_framework.serializers import ModelSerializer
from accounts.models import  User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'last_name', 'email','password', 'phone']
        #fields = '__all__'