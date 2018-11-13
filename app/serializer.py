from rest_framework import serializers
from app.models import ProjectxUser, Message
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = ProjectxUser
        fields = ('username', 'password')

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user:
            (token, created) = Token.objects.get_or_create(user=user)
            output = {"token": token.key}
            return output
        raise serializers.ValidationError({"error": "username or password is wrong"})


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_repeat = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = ProjectxUser
        fields = ('username', 'password', 'password_repeat', 'first_name', 'last_name', 'phone')

    def validate(self, data):
        try:
            ProjectxUser.objects.get(username=data["username"])
        except:
            if data["password"] == data["password_repeat"]:
                return data
            else:
                raise serializers.ValidationError({"error": "password is not matching"})
        raise serializers.ValidationError({"error": "username already taken"})

    def create(self, validated_data):
        try:
            user = ProjectxUser.objects.create(username=validated_data["username"])
            user.first_name = validated_data["first_name"]
            user.last_name = validated_data["last_name"]
            user.phone = validated_data["phone"]
            user.set_password(validated_data["password"])
            user.save()
            return user
        except Exception:
            try:
                user.delete()
            except Exception as e:
                raise serializers.ValidationError(str(e))


class InboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('from_user', 'to_user', 'message', 'chat', 'created_date')


class sendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('from_user', 'to_user', 'message', 'chat', 'created_date')



