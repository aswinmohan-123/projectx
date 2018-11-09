from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import LoginSerializer, RegisterSerializer, InboxSerializer
from rest_framework.authtoken.models import Token
from app.models import ProjectxUser, Message
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


class Login(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=200, data=serializer.validated_data,
                            content_type='application/json')
        else:
            return Response(status=404, data={'error': str(serializer.error_messages)}, content_type='application/json')


class Register(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user = ProjectxUser.objects.get(username=serializer.validated_data["username"])
                (token, created) = Token.objects.get_or_create(user=user)
                output = {"token": token.key}
            return Response(status=200, data=output, content_type='application/json')
        else:
            return Response(status=404, data={'error': str(serializer.error_messages)}, content_type='application/json')


class Details(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {"username": request.user.username, "first_name": request.user.first_name, "last_name": request.user.last_name,
                "phone": request.user.phone}
        return Response(status=200, data=data, content_type='application/json')


class Inbox(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.GET:
            try:
                user = ProjectxUser.objects.get(username=request.GET['sender'])
                messages = Message.objects.filter(to_user=request.user, from_user=user).order_by('-created_date')[0:4]
                serializer = InboxSerializer(messages, many=True)
                senders = []
                today = datetime.now().strftime("%Y-%m-%d")
                today = int(today[5:7]+today[8:10])
                for element in serializer.data:
                    date = element['created_date']
                    date = int(date[5:7] + date[8:10])
                    if today-date == 1:
                        senders.append([element['message'], "yesterday"])
                        break
                    if abs(today-date) > 1:
                        senders.append([element['message'], element['created_date'][0:10]])
                        break
                    if int(element['created_date'][11:13]) < 12:
                        senders.append([element['message'], element['created_date'][11:16]+"am"])
                    else:
                        if int(element['created_date'][11:13]) == 12:
                            senders.append([element['message'],
                                            element['created_date'][11:13] + element['created_date'][
                                                                                            13:16] + "pm"])
                        else:
                            senders.append([element['message'],
                                            str(int(element['created_date'][11:13])-12)+element['created_date'][
                                                                                        13:16]+"pm"])
                return Response(status=200, data={"messages": senders}, content_type='application/json')
            except Exception as e:
                return Response(status=404, data={"error": "something went wrong"+str(e)},
                                content_type='application/json')
        else:
            try:
                messages = Message.objects.filter(to_user=request.user).order_by('-created_date')
                serializer = InboxSerializer(messages, many=True)
                senders = []
                for x in serializer.data:
                    username = ProjectxUser.objects.get(id=x['from_user']).username
                    if username not in senders:
                        senders.append(username)
                return Response(status=200, data={"names": senders[0:5]}, content_type='application/json')
            except Exception:
                return Response(status=404, data={"error": "something went wrong"},
                                content_type='application/json')


class Peoples(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            peoples = ProjectxUser.objects.all().values('username')
            return Response(status=200, data=peoples,
                            content_type='application/json')
        except Exception:
            pass
        return Response(status=404, data="hai",
                        content_type='application/json')


class Send(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            print(request.data)
            to_user = ProjectxUser.objects.get(username=request.data['to_user'])
            from_user = request.user
            message = request.data['message']
            mess = Message.objects.create(from_user=from_user, to_user=to_user)
            mess.message = message
            mess.save()
        except Exception:
            return Response(status=404, data="failed",
                            content_type='application/json')

        return Response(status=200, data="Successful",
                        content_type='application/json')




























