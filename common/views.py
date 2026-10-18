from django.db import connection
from django.db.utils import DatabaseError

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        data = {
            "status": "ok",
            "service": "Enterprise Project & Task Management API",
            "database": "connected",
        }

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        except DatabaseError:
            data["status"] = "degraded"
            data["database"] = "unavailable"

            return Response(data, status=503)

        return Response(data, status=200)
