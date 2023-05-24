from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # 默认注册的用户不是active状态，需要超级管理员审批
        user.save()

        # Send email to admins
        send_mail(
            'New user registration',
            f'A new user {user.username} has registered. Please check and activate their account.',
            settings.EMAIL_HOST_USER,
            [admin[1] for admin in settings.ADMINS],
            fail_silently=False,
        )

        return user
