from rest_framework import serializers
from .models import (
    User, Class, ClassStudent, Avatar,
    KindlewickGameProgress, KindlewickGameSession,
    TeachingResource, School
)

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'slug', 'logo', 'subscription_tier', 'description']
        read_only_fields = ['id', 'slug']


class UserSerializer(serializers.ModelSerializer):
    school_detail = serializers.SerializerMethodField()

    def get_school_detail(self, obj):
        if not obj.school:
            return None
        return {'name': obj.school}
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'school', 'school_detail', 'display_name', 'bio']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'user', 'avatar_config', 'created_at', 'updated_at']
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


class TeachingResourceSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    visibility_display = serializers.CharField(source='get_visibility_display', read_only=True)
    
    class Meta:
        model = TeachingResource
        fields = ['id', 'title', 'slug', 'author', 'author_name', 'content', 'excerpt', 'image', 'file', 'resource_type', 'key_stage', 'subject', 'status', 'visibility', 'visibility_display', 'featured', 'created_at', 'updated_at', 'published_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']