from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from utils.coolsms import coolsms
from utils.serializer import SendSMSSerializer


class SendSMS(APIView):
    def post(self, request):
        serializer = SendSMSSerializer(data=request.data)
        if serializer.is_valid():
            coolsms(**serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


