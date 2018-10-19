from rest_framework import serializers
from .models import DB_details


class DB_detailsSerializer(serializers.ModelSerializer):

        class Meta:
            model = DB_details
            fields = ('name', 'address', 'password', 'username', 'port')
