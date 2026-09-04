from django.contrib import admin
from django.urls import path

from matches import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("matches", views.matches_list, name="matches"),
    path("matches/live", views.matches_live, name="matches_live"),
    path("matches/future", views.matches_future, name="matches_future"),

    path("matches/create", views.match_create, name="match_create"),
    path(
        "matches/edit/<int:match_id>",
        views.match_edit,
        name="match_edit",
    ),
    path(
        "matches/<int:match_id>",
        views.match_detail,
        name="match_detail",
    ),

    path("tournaments", views.tournaments_list, name="tournaments"),

    path(
        "tournaments/create",
        views.tournament_create,
        name="tournament_create",
    ),
    path(
        "tournaments/edit/<int:tournament_id>",
        views.tournament_edit,
        name="tournament_edit",
    ),
    path(
        "tournaments/<int:tournament_id>",
        views.tournament_detail,
        name="tournament_detail",
    ),
]