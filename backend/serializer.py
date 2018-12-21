from rest_framework import serializers
from .models import DB_details, Charts


class Chart_detailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Charts
        fields = ('connection_name', 'table_name', 'column_name', 'database_id')


class DB_detailsSerializer(serializers.ModelSerializer):
    charts = Chart_detailsSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model = DB_details
        fields = ('connection_name', 'db_type', 'name', 'address', 
                  'password', 'username', 'port', 'user')


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        )