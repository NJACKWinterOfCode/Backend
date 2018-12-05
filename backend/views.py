from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import DB_details
from .serializer import DB_detailsSerializer
from django.http import HttpResponse, JsonResponse
import MySQLdb
import psycopg2
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User


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


def connect_psql(data):
    name = data['name']
    host = data['address']
    password = data['password']
    username = data['username']
    port = data['port']
    s = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(name, username, host, password, port)
    return psycopg2.connect(s)


class DBDetailsView(APIView):
    def get(self, request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user)
            x = DB_details.objects.filter(user=user)
            # x = DB_details.objects.all()
            # print(user)
            s = DB_detailsSerializer(x, many=True)
            return Response(s.data)
            # if s.is_valid():
            #     print(s.data)
            #     return Response({"status": "ok"})
            # else:
            #     print(s.errors)
            #     print("Not Valid")
            #     return Response({"error": "bad"})
            

class New_DB_detailsAPI(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated():
            request_data = request.data.copy()
            request_data['user'] = User.objects.get(username=request.user).id
            # print(request_data)
            dbserializer = DB_detailsSerializer(data=request_data)
            if dbserializer.is_valid():
                # dbserializer.save()
                if request_data['db_type'] == 'psql':
                    try:
                        conn = connect_psql(request_data)
                        cursor = conn.cursor()
                        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                        tables = []
                        for table in cursor.fetchall():
                            tables.append(table[0])
                        details = {}
                        for table in tables:
                            print(table)
                            cursor.execute("select column_name, data_type from information_schema.columns where table_name='{}'".format(table))
                            results = cursor.fetchall()
                            details[table] = results
                        dbserializer.save()
                        print(dbserializer.data)
                        conn.close()
                        return Response({"status": "ok", "connection_name": request_data["connection_name"], "tables": tables, "details": details})
                    except:
                        conn.close()
                        return Response({"error": "Unable to connect to Database. Check if the port is open"})
                if request_data['db_type'] == 'mysql':
                    try:
                        tables = []
                        schema = {}
                        conn = MySQLdb.connect(host=request_data.get('address'),
                                           user=request_data['username'], passwd=request_data['password'])
                        cursor = conn.cursor()
                        cursor.execute('use ' + request_data['name'])
                        cursor.execute('show tables')
                        for data in cursor.fetchall():
                            tables.append(data[0])
                        for table in tables:
                            cursor.execute("describe " + table)
                            schema_data = cursor.fetchall()
                            schema[table] = [schema_data[0][0],schema_data[0][1]]
                        dbserializer.save()
                        conn.close()
                        return Response({"status": "ok","connection_name": request_data["connection_name"], "tables": tables,"details":schema}, status=status.HTTP_200_OK)
                    except:
                        conn.close()
                        return Response({"error": "Unable to connect to Database. Check if the port is open"})
                return Response(dbserializer.data, status=status.HTTP_200_OK)
            return Response(dbserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "message": "You are not logged in."}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, dbname, format=None):
        if request.user.is_authenticated():
            try:
                db_data = DB_details.objects.get(name=dbname,user=request.user)
                dbserializer = DB_detailsSerializer(db_data)
                response_data = dbserializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            except:
                return Response({"success": False, "message": "No details found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "message": "You are not logged in."}, status=status.HTTP_403_FORBIDDEN)


class DB_detailsAPI(APIView):
    def post(self, request, dbname, format=None):
        if request.user.is_authenticated():
            request_data = request.data.copy()
            request_data['user'] = request.user
            dbserializer = DB_detailsSerializer(data=request_data)
            if dbserializer.is_valid():
                dbserializer.save()
                # print(request_data)
                return Response(dbserializer.data, status=status.HTTP_200_OK)
            return Response(dbserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "message": "You are not logged in."}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, dbname, format=None):
        if request.user.is_authenticated():
            try:
                db_data = DB_details.objects.get(name=dbname,user=request.user)
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


class DataFetcher(APIView):
    def post(self, request):
        if request.user.is_authenticated():
            data = request.data.copy()
            connection_name = data['connection_name']
            user_id = User.objects.get(username=request.user).id
            db = DB_details.objects.filter(user=user_id).get(connection_name=connection_name)
            # print(db.name)
            if db.db_type == 'psql':
                x = {
                    'name': db.name,
                    'address': db.address,
                    'password': db.password,
                    'port': db.port,
                    'username': db.username
                }
                conn = connect_psql(x)
                curr = conn.cursor()
                cols = data['col']
                results = [{'status':'ok'}]
                for col in cols:
                    table = col['table']
                    field = col['field']
                    curr.execute("SELECT {} from {}".format(field, table))
                    x = curr.fetchall()
                    z  = []
                    for y in x:
                        z.append(y[0])
                    results.append({ 'table': table, 'field': field, 'data': z })
                conn.close()
                return Response(results)
            return Response("Awesome")
            

class DBSingle(APIView):
    def post(self, request, connection_name):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user)
            x = DB_details.objects.filter(user=user).get(connection_name=connection_name)
            if x.db_type == 'psql':
                try:
                    d = {
                        'name': x.name,
                        'address': x.address,
                        'password': x.password,
                        'port': x.port,
                        'username': x.username
                    }
                    conn = connect_psql(d)
                    cursor = conn.cursor()
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                    tables = []
                    for table in cursor.fetchall():
                        tables.append(table[0])
                    details = {}
                    for table in tables:
                        # print(table)
                        cursor.execute("select column_name, data_type from information_schema.columns where table_name='{}'".format(table))
                        results = cursor.fetchall()
                        details[table] = results
                    return Response({"status": "ok", "connection_name": connection_name, "tables": tables, "details": details})
                except Exception as e:
                    return Response({"error": True, "message": "Unable to connect to database"})