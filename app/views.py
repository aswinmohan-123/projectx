from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import LoginSerializer, RegisterSerializer, InboxSerializer, sendSerializer
from rest_framework.authtoken.models import Token
from app.models import ProjectxUser, Message, Config
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.db.models import Q


class Login(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=200, data=serializer.validated_data,
                            content_type='application/json')
        else:
            return Response(status=404, data={'error': "Username or password are incorrect"}, content_type='application/json')


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
            return Response(status=404, data={'error': "username already exist or values are null"}, content_type='application/json')


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
                messages = Message.objects.filter(chat=request.GET['chat'])
                sendto = messages.filter(from_user=request.user).values('to_user')
                if sendto:
                    sendto = ProjectxUser.objects.get(id=sendto[0]['to_user']).username
                messages = messages.order_by('-created_date')[0:4]
                serializer = InboxSerializer(messages, many=True)
                senders = []
                today = datetime.now().strftime("%Y-%m-%d")
                today = int(today[5:7]+today[8:10])
                for element in serializer.data:
                    if request.user.id == element["from_user"]:
                        reply = 0
                    else:
                        reply = 1
                    date = element['created_date']
                    date = int(date[5:7] + date[8:10])
                    if today-date == 1:
                        senders.append([element['message'], "yesterday", reply, sendto])
                        break
                    if abs(today-date) > 1:
                        senders.append([element['message'], element['created_date'][0:10], reply, sendto])
                        break
                    if int(element['created_date'][11:13]) < 12:
                        senders.append([element['message'], element['created_date'][11:16]+"am", reply, sendto])
                    else:
                        if int(element['created_date'][11:13]) == 12:
                            senders.append([element['message'],
                                            element['created_date'][11:13] + element['created_date'][
                                                                                            13:16] + "pm", reply, sendto])
                        else:
                            senders.append([element['message'],
                                            str(int(element['created_date'][11:13])-12)+element['created_date'][
                                                                                        13:16]+"pm", reply, sendto])
                return Response(status=200, data={"messages": senders[::-1]}, content_type='application/json')
            except Exception as e:
                return Response(status=404, data={"error": "something went wrong"+str(e)},
                                content_type='application/json')
        else:
            try:
                messages = Message.objects.filter(to_user=request.user).order_by('-created_date')
                serializer = InboxSerializer(messages, many=True)
                senders = []
                checker = []
                for x in serializer.data:
                    username = ProjectxUser.objects.get(id=x['from_user']).username
                    if senders:
                        if username not in checker:
                            senders.append([username, x['chat']])
                            checker.append(username)
                    else:
                        senders.append([username, x['chat']])
                        checker.append(username)
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
            to_user = ProjectxUser.objects.get(username=request.data['to_user'])
            from_user = request.user
            message = request.data['message']
            if message != '':
                mess = Message.objects.filter(from_user=from_user, to_user=to_user)
                serializer = sendSerializer(mess, many=True)
                if serializer.data:
                    mess = Message.objects.create(from_user=from_user, to_user=to_user, chat=serializer.data[0]['chat'])
                else:
                        mess = Message.objects.filter(from_user=to_user, to_user=from_user)
                        serializer2 = sendSerializer(mess, many=True)
                        if serializer2.data:
                            mess = Message.objects.create(from_user=from_user, to_user=to_user,
                                                          chat=serializer2.data[0]['chat'])
                        else:
                            mess = Message.objects.create(from_user=from_user, to_user=to_user)
                            config = Config.objects.get(id=1)
                            mess.chat = config.chat_max_number
                            config.chat_max_number += 1
                            config.save()
                mess.message = message
                mess.save()
        except Exception:
            return Response(status=404, data="failed",
                            content_type='application/json')

        return Response(status=200, data="Successful",
                        content_type='application/json')




























