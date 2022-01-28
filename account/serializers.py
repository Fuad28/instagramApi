from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import  get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import  FollowRelations


User= get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators= [UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=32,validators=[UniqueValidator(queryset=User.objects.all())])
    password= serializers.CharField(min_length= 8, max_length=50, required=True, write_only=True, style={'input_type': 'password'})
    password2= serializers.CharField(min_length=8, max_length=50, required=True, write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model= User
        fields =  ["id", "username", "password", "password2","email", "phone", "first_name", "last_name", "bio", "profile_pic", "private", "birth_date"]
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("Those passwords don't match.")
        validate_password(attrs.get('password'), User)
        attrs.pop('password2')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ["id", "username", "first_name", "last_name", "bio", "profile_pic"]

class FollowRelationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= FollowRelations
        fields= ['id', 'user', 'followers', 'following', 'pending', 'blocked']
