from rest_framework import serializers, status
from rest_framework.response import Response

from .models import UserInfo, UserProfile

class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True, 
                                            style = {'input_type': 'password', 'placeholder': 'Confirm Password'})

    class Meta:

        model = UserInfo
        fields = ['id','email','password','confirm_password']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type': 'password', 'placeholder': 'Password'}
            },
            'confirm_password':{
                'write_only':True
            }
        }

    def validate(self,data):

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password_error':"Password Does not Match"})
        return data
    
    def create(self, validated_data):
    
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        user = UserInfo(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'firstname',
            'lastname',
            'city',
            'country',
            'phone_number',
            'date_of_birth',
            'email',
            'gender',
            'describe_about_yourself'
        ]