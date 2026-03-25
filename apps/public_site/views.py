from django.db import connection
from django.http import JsonResponse
from django.views import View


class LivenessView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


class ReadinessView(View):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return JsonResponse({"status": "ok"})
        except Exception:
            return JsonResponse({"status": "unavailable"}, status=503)
