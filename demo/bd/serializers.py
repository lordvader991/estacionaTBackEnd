from rest_framework.serializers import ModelSerializer
from bd.models import PersonModel, User

class PersonSerializer(ModelSerializer):
    class Meta:
        model = PersonModel
        fields = ['id', 'name', 'address', 'phone']
        #fields = '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'email','password', 'phone']
        #fields = '__all__'