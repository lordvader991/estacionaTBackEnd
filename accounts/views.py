from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import  User
from .serializers import  UserSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class LoginAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def post(self,req):
        user = get_object_or_404(User,username = req.data['username'])

        if not user.check_password(req.data['password']):
            return Response({"error":"invalid password"},status = status.HTTP_404_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        return Response({"token":token.key, "user":serializer.data},status = status.HTTP_200_OK)

class SignupAPIView(APIView):
    def post(self, req):
        print(req.data)
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        try:
            user = User.objects.get(email=user_data['email'])
            raise ValidationError("User with this email already exists")
        except ObjectDoesNotExist:
            user = User.objects.create(
                username=user_data['username'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                phone=user_data['phone']
            )
            user.set_password(user_data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user_data}, status=status.HTTP_201_CREATED)
        
class UserDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)
    
