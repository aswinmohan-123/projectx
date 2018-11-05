from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from app.models import projectx_user


class Login(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            return Response(status=200, data=serializer.validated_data,
                            content_type='application/json')
        else:
            return Response(status=404, data={'error': 'username or password is wrong'})


class Register(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            if user:
                print(serializer.validated_data["username"])
                user = projectx_user.objects.get(username=serializer.validated_data["username"])
                (token, created) = Token.objects.get_or_create(user=user)
                print(token)
            return Response(status=200, data={"username": user.username, "token": token}, content_type='application/json')
        else:
            return Response(status=404, data={'error': 'username already exist'})

