from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from users.serializers import CourseSerializer, NewRegistrationSerializer
from rest_framework.generics import CreateAPIView
from users.models import NewRegistration


# Create your views here.


class GenerateAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        current_tokens = Token.objects.filter(user=user)

        if current_tokens.exists():
            current_tokens.first().delete()
        if not user.student.account_active:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        token, created = Token.objects.get_or_create(user=user)
        user.student.logged_in = True
        user.student.last_login_time = token.created
        user.student.save()

        course_list = CourseSerializer(user.student.courses.all(), many=True)

        return Response(
            {"token": token.key, "name": user.first_name, "courses": course_list.data}
        )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ConfirmLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        token = request.data.get("token", None)
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        queryset = Token.objects.filter(key=token)

        if not queryset.exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            user_token = queryset.first()
            student = user_token.user.student
            if not student.account_active:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            user_token.user.student.last_login_time = timezone.now()
            user_token.user.student.save()
            course_list = CourseSerializer(
                user_token.user.student.courses.all(), many=True
            )

            return Response(
                {
                    "status": "ok",
                    "name": user_token.user.first_name,
                    "courses": course_list.data,
                }
            )


class NewRegistrationsView(CreateAPIView):
    queryset = NewRegistration.objects.all()
    serializer_class = NewRegistrationSerializer
