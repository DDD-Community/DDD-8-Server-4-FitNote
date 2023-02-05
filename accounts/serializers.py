from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):

    fullname = serializers.CharField()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['fullname'] = self.validated_data.get('fullname', '')

        return data
