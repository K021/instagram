from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from sms.coolsms import coolsms
from sms.serializer import SendSMSSerializer


class SendSMS(APIView):
    def post(self, request):
        serializer = SendSMSSerializer(data=request.data)
        if serializer.is_valid():
            result = coolsms(**serializer.data)
            data = {
                'result': result.data,
                'sms data': serializer.data,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


