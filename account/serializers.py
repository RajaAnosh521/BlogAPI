from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.authentication import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, data):
        # Check if the passwords match
        if data['password1'] != data['password2']:
            raise ValidationError({"message": "Passwords do not match!"}) # type: ignore
        
        # Validate the password strength using Django's validate_password function
        validate_password(data['password1'])
        
        return data

    def create(self, validated_data):
        # Remove password1 and password2 from validated_data
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        # Create the user with the rest of the data
        user = User(**validated_data)
        
        # Set the password (this hashes it before saving)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ['username', 'password'] 

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data