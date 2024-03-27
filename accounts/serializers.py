
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User
from rest_framework.authtoken.models import Token


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=80)
    username = serializers.CharField(required=False, max_length=45)
    date_of_birth = serializers.DateField(required=False)
    password = serializers.CharField(required=True, write_only=True, min_length=8,  style={'input_type': 'password'})


    class Meta:
        model = User
        fields = ['email', 'username', 'date_of_birth', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs.get('email')).exists()
        if email_exists:
            raise ValidationError('Email already exists')
        return super().validate(attrs)
    

    def create(self, validated_data):

        password = validated_data.pop('password')

        user= super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


