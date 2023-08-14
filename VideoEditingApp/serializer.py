from rest_framework import serializers
from .models import *

class VideoClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clips
        fields = ('id', 'video','subclips','thumbnail_url','title')

class VideoToAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoToAudio
        fields = ('id', 'video','audio_url','title')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
      password=attrs.get('password')   
      return attrs
    def create(self, validated_data,):
       user=User.objects.create(
       email=validated_data['email'],
       username=validated_data['username'],)
       user.set_password(validated_data['password']) 
       user.save()
       return user
      

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'age', 'address')

class PersonSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Person
        fields = ('id', 'name', 'profile')   