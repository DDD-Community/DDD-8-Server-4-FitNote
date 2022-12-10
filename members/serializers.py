from django.core import serializers



class MemberSerializer(serializers.ModelSerializer):

    test = serializers.SerializerMethodField(method_name='testtest')

    class Meta:
        fields = ('fields')