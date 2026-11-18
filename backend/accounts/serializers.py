from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "is_active", "must_change_password")
        read_only_fields = ("id", "is_active", "must_change_password")

class TeamCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role", "password")
    def validate_role(self, value):
        if value == User.Role.ADMIN:
            raise serializers.ValidationError("Only the existing workspace owner can grant admin access.")
        return value
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.must_change_password = True
        user.save()
        return user
