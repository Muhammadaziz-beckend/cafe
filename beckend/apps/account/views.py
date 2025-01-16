from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *

from apps.account.serializers import *
from utils.permissions import IsAdminOrStaff


class Login(GenericAPIView):

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        if not user:
            return Response(
                {"default": "Неверная имя или пароль!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class CreateEmployee(GenericAPIView):

    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAdminOrStaff]

    def post(self, request, *args, **kwargs):

        serializer: CreateEmployeeSerializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        user_data = {
            "username": user.username,
            "token": str(token),
        }

        return Response(user_data, status=201)


class UpdatePasswordUser(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UpdatePasswordUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get("new_password")
        old_password = serializer.validated_data.get("old_password")

        user = authenticate(username=request.user.username, password=old_password)

        if user:

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Пароль успешно изменён"})

        return Response(
            {"detail": "Неверный старый пароль"}, status=status.HTTP_400_BAD_REQUEST
        )