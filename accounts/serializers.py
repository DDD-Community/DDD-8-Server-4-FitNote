from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: profile_image
    fullname = serializers.CharField()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['fullname'] = self.validated_data.get('fullname', '')

        return data
