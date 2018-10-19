from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import DB_details
from .serializer import DB_detailsSerializer
from django.http import HttpResponse, JsonResponse
import MySQLdb
from django.views.decorators.http import require_http_methods


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
        results.append({desc: res[iterator]})
    return results


def home(request):
    return HttpResponse("Home")


class DB_detailsAPI(APIView):
    def post(self, request, dbname, format=None):
        if request.user.is_authenticated():
            request_data = request.data.copy()
            request_data['user'] = request.user
            dbserializer = DB_detailsSerializer(data=request_data)
            if dbserializer.is_valid():
                dbserializer.save()
                return Response(dbserializer.data, status=status.HTTP_200_OK)
            return Response(dbserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "message": "You are not logged in."}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, dbname, format=None):
        if request.user.is_authenticated():
            try:
                db_data = DB_details.objects.get(
                    name=dbname, user=request.user)
                dbserializer = DB_detailsSerializer(db_data)
                response_data = dbserializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            except:
                return Response({"success": False, "message": "No details found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "message": "You are not logged in."}, status=status.HTTP_403_FORBIDDEN)


class MysqlAPI(APIView):
    def get(self, request, column, dbname, tablename):
        if request.user.is_authenticated():
            db_data = DB_details.objects.get(name=dbname, user=request.user)

            conn = MySQLdb.connect(host=db_data.address,
                                   user=db_data.username, passwd=db_data.password)
            cursor = conn.cursor()
            cursor.execute('use ' + db_data.name)
            cursor.execute('select * from ' + tablename)

            results = get_results(cursor, column)

            return Response(results, status=status.HTTP_200_OK)
        return Response({"success": False, "message": "You are not logged in."}, status=status.HTTP_403_FORBIDDEN)
