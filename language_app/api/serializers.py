from rest_framework import serializers
from language_app.models import Language, Dictionary, Word, UserProfile
from django.contrib.auth.models import User

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'native_language', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

class DictionarySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    language_id = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), source='language')
    user_id = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all(), source='user')

    class Meta:
        model = Dictionary
        fields = ['id', 'user', 'user_id', 'language', 'language_id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'language']

class WordSerializer(serializers.ModelSerializer):
    dictionary = DictionarySerializer(read_only=True)
    dictionary_id = serializers.PrimaryKeyRelatedField(queryset=Dictionary.objects.all(), source='dictionary')

    class Meta:
        model = Word
        fields = ['id', 'dictionary', 'dictionary_id', 'text', 'translation', 'example_sentence', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'dictionary']