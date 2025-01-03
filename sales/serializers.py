
from rest_framework import serializers
from django.contrib.auth.models import User

from sales.models import Telecaller, SalesLead, LeadSourceConfig, Config


class TelecallerSerializer (serializers.ModelSerializer):
    class Meta:
        model = Telecaller
        fields = '__all__'

class LeadSourceConfigSerializer(serializers.ModelSerializer):
    telecallers = TelecallerSerializer(many=True)

    class Meta:
        model = LeadSourceConfig
        fields = '__all__'


# class SalesLeadSerializer(serializers.ModelSerializer):
#     telecaller = TelecallerSerializer()
#     user = serializers.SerializerMethodField()
#
#     class Meta:
#         model = SalesLead
#         fields = ['id', 'telecaller', 'user']


class SalesLeadSerializer(serializers.ModelSerializer):
    telecaller = TelecallerSerializer()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SalesLead
        fields = ['id', 'telecaller', 'user_name']

    def get_user_name(self, obj):
        return obj.user.username

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'