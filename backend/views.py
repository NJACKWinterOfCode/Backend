from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import DB_details
from .serializer import DB_detailsSerializer
from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse("Home")


class DB_detailsAPI(APIView):
    def post(self, request, dbname, format=None):
        dbserializer = DB_detailsSerializer(data=request.data)
        if dbserializer.is_valid():
            dbserializer.save()
            return Response(dbserializer.data, status=status.HTTP_200_OK)
        return Response(dbserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, dbname, format=None):
        try:
            db_data = DB_details.objects.get(name=dbname)
            dbserializer = DB_detailsSerializer(db_data)
            response_data = dbserializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({"success": False, "message": "No details found"}, status=status.HTTP_400_BAD_REQUEST)
