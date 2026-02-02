from rest_framework import serializers
from .models import (
    User, Teacher, Student, Class, ClassStudent, GameSession, GameResult,
    Achievement, StudentAchievement, TeacherNote, StudentMetrics, ClassMetrics, TeacherMetrics
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassStudent
        fields = '__all__'

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = '__all__'

class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class StudentAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAchievement
        fields = '__all__'

class TeacherNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherNote
        fields = '__all__'

class StudentMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMetrics
        fields = '__all__'

class ClassMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMetrics
        fields = '__all__'

class TeacherMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherMetrics
        fields = '__all__'
