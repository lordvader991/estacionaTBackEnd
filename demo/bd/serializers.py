from rest_framework.serializers import ModelSerializer
from bd.models import PersonModel

class PersonSerializer(ModelSerializer):
    class Meta:
        model = PersonModel
        fields = ['id', 'name', 'address', 'phone']
        #fields = '__all__'
        