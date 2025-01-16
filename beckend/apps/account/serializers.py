from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token

from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            # Аутентификация пользователя
            user = authenticate(
                request=self.context.get("request"),
                username=username,  # Используем username
                password=password,
            )

            user_data_base = User.objects.filter(username=username)

            if not user:
                if user_data_base and self.access_period:
                    msg = "Срок действия вашей учётной записи истёк. Пожалуйста, оплатите доступ для продолжения."
                    raise PermissionDenied(detail=msg)
                msg = "Неправильный номер телефона или пароль."
                raise serializers.ValidationError(msg, code="error")
            # Проверка срока действия и активности

        else:
            msg = "Обязательно укажите номер телефона и пароль."
            raise serializers.ValidationError(msg, code="authorization")

        # Проверка успешной аутентификации
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """
        Генерация токена после успешной аутентификации.
        """
        user = validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return {"token": token.key}


class CreateEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user


class UpdatePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()