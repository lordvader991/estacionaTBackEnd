from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import  User
from .serializers import  UserSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

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
                phone=user_data['phone'],
                rol_usuario=user_data.get('rol_usuario', False)
            )
            user.set_password(user_data['password'])
            user.correo_auth = True  #cuando envia el correo ahi se vuelve true
            user.save()

            self.send_confirmation_email(user.email)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user_data}, status=status.HTTP_201_CREATED)

    def send_confirmation_email(self, to_email):
        sender_email = settings.EMAIL_HOST_USER
        sender_password = settings.EMAIL_HOST_PASSWORD
        #mensaje
        subject = "¡Registro exitoso!"
        body = "¡Gracias por registrarte en nuestra aplicación EstacionaT!"
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
class UserDetailApiView(APIView):
    #implementando las validaciones del token
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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