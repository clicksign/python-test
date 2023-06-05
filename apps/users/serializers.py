from rest_framework import serializers
from apps.users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_group = serializers.ChoiceField(choices=CustomUser.USER_GROUPS, default=2)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'user_group')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
