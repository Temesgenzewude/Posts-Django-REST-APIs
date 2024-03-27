from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from .serializers import UserSignUpSerializer

# Create your views here.

class UserSignUpAPIView(generics.GenericAPIView):

    serializer_class = UserSignUpSerializer

    def post(self, request:Request):
        data= request.data
        serializer = self.serializer_class(data= data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'You have successfully signed up!',
                'data': serializer.data
            }
            return Response(data= response, status=status.HTTP_201_CREATED)
        else:
            return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginAPIView(generics.GenericAPIView):

    def post(self, request:Request):
        email= request.data.get('email')
        password= request.data.get('password')

        user= authenticate(request, email= email, password= password)

        if user is not None:
            response= {
                'message': 'You have successfully logged in!',
                'data': {
                    'email': user.email,
                    'username': user.username,
                    'date_of_birth': user.date_of_birth,
                    'auth_token': user.auth_token.key,
                }
            }
            return Response(data= response, status=status.HTTP_200_OK)
        
        else:
            return Response(data= {'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request:Request):

        contents={
            "user": str(request.user),
            "auth_token": str(request.auth)

        }

        return Response(data= contents, status=status.HTTP_200_OK)
        
    
