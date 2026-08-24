from django.contrib import admin

from .models import Match, Player, SportTournament


admin.site.register(Match)
admin.site.register(Player)
admin.site.register(SportTournament)