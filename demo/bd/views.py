from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from bd.models import PersonModel
from bd.serializers import PersonSerializer

class PersonApiView(APIView):
    def get(self, request):
        serializer = PersonSerializer(PersonModel.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class PersonDetailApiView(APIView):
    def get_object(self,pk):
        try:
            return PersonModel.objects.get(pk=pk)
        except PersonModel.DoesNotExist:
            return None
    def get(self, request, id):
        person = self.get_object(id)
        serializer = PersonSerializer(person)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def put(self, request, id):
        person = self.get_object(id)
        if(person==None):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    def dekete(self,request,id):
        person = self.get_object(id)
        person.delete()
        Response = {'deleted':True}
        return Response(status=status.HTTP_200_OK, data=Response)