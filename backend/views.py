from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import DB_details
from .serializer import DB_detailsSerializer
from django.http import HttpResponse, JsonResponse
import MySQLdb
from django.views.decorators.http import require_http_methods


class dotdict(dict):
   __getattr__ = dict.get
   __setattr__ = dict.__setitem__
   __delattr__ = dict.__delitem__


def get_results(db_cursor, column):
   desc = ""
   results = []
   iterator = 0
   for d in db_cursor.description:
       if d[0].lower() == column.lower():
           desc = d[0]
           break
       iterator = iterator + 1
    for res in db_cursor.fetchall():
       results.append({desc:res[iterator]})
   return results


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

class MysqlAPI(APIView):
    def get(self, request, column, dbname, tablename):
        db_data = DB_details.objects.get(name=dbname)
         conn = MySQLdb.connect(host=db_data.address,
                               user=db_data.username, passwd=db_data.password)
        cursor = conn.cursor()
        cursor.execute('use ' + db_data.name)
        cursor.execute('select * from ' + tablename)
         results = get_results(cursor, column)
         return Response(results, status=status.HTTP_200_OK)
