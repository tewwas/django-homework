from django.contrib import admin
from django.urls import path

from matches import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("matches", views.matches_list, name="matches"),
    path("matches/live", views.matches_live, name="matches_live"),
    path("matches/future", views.matches_future, name="matches_future"),
]