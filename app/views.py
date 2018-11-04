from rest_framework.views import APIView
from rest_framework.response import Response

class login(APIView):
    def get(self, request):
        return Response(status=200, data={'first_name': 'aswin', 'last_name': 'mohan'}, content_type='application/json')
