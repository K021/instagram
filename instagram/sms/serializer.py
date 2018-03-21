from rest_framework import serializers


class SendSMSSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=13)
    message = serializers.CharField(max_length=90)

    def validate(self, data):
        cellphone = ['010', '011', '016', '017', '019']

        receiver = data['receiver'].replace('-', '')
        message = data['message']

        if len(receiver) not in [10, 11]:
            raise serializers.ValidationError('전화번호 형식이 올바르지 않습니다. 국내 핸드폰 번호만 가능합니다')
        elif receiver[:3] not in cellphone:
            raise serializers.ValidationError('전화번호 형식이 올바르지 않습니다. 국내 핸드폰 번호만 가능합니다')

        if len(message.encode('cp949')) > 90:
            raise serializers.ValidationError('90 byte 까지만 전송할 수 있습니다')

        return data
