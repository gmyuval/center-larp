from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Center LARP GM Panel"
admin.site.site_title = "Center LARP"
admin.site.index_title = "GM Dashboard"

urlpatterns = [
    path("gm/", admin.site.urls),
    path("health/", include("apps.public_site.health_urls")),
    path("", include("apps.payments_cardcom.urls")),
    path("", include("apps.applications.urls")),
    path("", include("apps.public_site.urls")),
]
