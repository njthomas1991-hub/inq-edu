from rest_framework import serializers
from .models import (
    User, Class, ClassStudent, Avatar,
    KindlewickGameProgress, KindlewickGameSession
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassStudent
        fields = '__all__'


class KindlewickGameProgressSerializer(serializers.ModelSerializer):
    game_type_display = serializers.CharField(source='get_game_type_display', read_only=True)
    
    class Meta:
        model = KindlewickGameProgress
        fields = ['id', 'user', 'game_type', 'game_type_display', 'current_level', 'score', 
                  'tokens_earned', 'total_playtime', 'last_played', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_played']


class KindlewickGameSessionSerializer(serializers.ModelSerializer):
    game_type_display = serializers.CharField(source='get_game_type_display', read_only=True)
    
    class Meta:
        model = KindlewickGameSession
        fields = ['id', 'user', 'game_type', 'game_type_display', 'level', 'score', 
                  'tokens_earned', 'playtime', 'completed', 'session_data', 'created_at', 'finished_at']
        read_only_fields = ['id', 'created_at']


class KindlewickGameProgressAdminSerializer(serializers.ModelSerializer):
    game_type_display = serializers.CharField(source='get_game_type_display', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = KindlewickGameProgress
        fields = ['id', 'user', 'user_detail', 'game_type', 'game_type_display', 'current_level', 'score', 
                  'tokens_earned', 'total_playtime', 'last_played', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_played']


class KindlewickGameSessionAdminSerializer(serializers.ModelSerializer):
    game_type_display = serializers.CharField(source='get_game_type_display', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = KindlewickGameSession
        fields = ['id', 'user', 'user_detail', 'game_type', 'game_type_display', 'level', 'score', 
                  'tokens_earned', 'playtime', 'completed', 'session_data', 'created_at', 'finished_at']
        read_only_fields = ['id', 'created_at']