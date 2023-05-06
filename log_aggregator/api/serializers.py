from rest_framework import serializers

from log_access_apache.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
