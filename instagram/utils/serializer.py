from rest_framework import serializers


class SendSMSSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=11)
    message = serializers.CharField(max_length=45)

    def validate(self, data):
        cellphone = ['010', '011', '016', '017', '019']
        receiver = data['receiver']

        if not type(receiver) == str:
            raise serializers.ValidationError('전화번호가 문자열이 아닙니다')
        elif receiver == '':
            raise serializers.ValidationError('전화번호 데이터가 없습니다')
        elif len(receiver) not in [10, 11]:
            raise serializers.ValidationError('전화번호 형식이 올바르지 않습니다. 국내 핸드폰 번호만 가능합니다')
        elif receiver[:3] not in cellphone:
            raise serializers.ValidationError('전화번호 형식이 올바르지 않습니다. 국내 핸드폰 번호만 가능합니다')

        return data
