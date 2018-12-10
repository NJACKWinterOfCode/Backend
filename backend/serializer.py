from rest_framework import serializers
from .models import DB_details


class DB_detailsSerializer(serializers.ModelSerializer):

        class Meta:
            model = DB_details
            fields = ('connection_name', 'db_type', 'name', 'address', 
                      'password', 'username', 'port', 'user')


class SocialSerializer(serializers.Serializer):
	access_token = serializers.CharField(
		allow_blank=False,
		trim_whitespace=True,
		)
