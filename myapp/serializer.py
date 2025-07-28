# serializers.py

from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'name', 'mobile_no', 'password', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile_no=validated_data['mobile_no'],
            address=validated_data.get('address', ''),
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
    


class DecorationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Decoration
        fields = '__all__'

class CatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogItem
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


def validate_image(value):
    if value.size > 1024 * 1024:  # 1MB
        raise serializers.ValidationError("Image must be less than 1MB")
    return value

class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validate_image])

    class Meta:
        model = GalleryImage
        fields = ['image']

