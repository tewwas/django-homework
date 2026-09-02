from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Match, SportTournament


def matches_list(request):
    matches = Match.objects.select_related("tournament").order_by("-start_time")

    return render(
        request,
        "matches/match_list.html",
        {
            "matches": matches,
            "title": "Все матчи",
        },
    )


def matches_live(request):
    now = timezone.now()

    matches = Match.objects.select_related("tournament").filter(
        start_time__lte=now,
        end_time__gt=now,
    ).order_by("start_time")

    return render(
        request,
        "matches/match_list.html",
        {
            "matches": matches,
            "title": "Матчи сейчас",
        },
    )


def matches_future(request):
    now = timezone.now()

    matches = Match.objects.select_related("tournament").filter(
        start_time__gt=now,
    ).order_by("start_time")

    return render(
        request,
        "matches/match_list.html",
        {
            "matches": matches,
            "title": "Предстоящие матчи",
        },
    )


def match_detail(request, match_id):
    match = get_object_or_404(
        Match.objects.select_related("tournament"),
        pk=match_id,
    )

    return render(
        request,
        "matches/match_detail.html",
        {
            "match": match,
            "title": f"{match.team1} — {match.team2}",
        },
    )


def tournaments_list(request):
    now = timezone.now()

    tournaments = (
        SportTournament.objects
        .annotate(
            finished_matches_count=Count(
                "matches",
                filter=Q(matches__end_time__lt=now),
            )
        )
        .order_by("start_date", "id")
    )

    return render(
        request,
        "matches/tournament_list.html",
        {
            "tournaments": tournaments,
            "title": "Все турниры",
        },
    )


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(
        SportTournament,
        pk=tournament_id,
    )

    matches = tournament.matches.order_by("start_time")

    return render(
        request,
        "matches/tournament_detail.html",
        {
            "tournament": tournament,
            "matches": matches,
            "title": tournament.name,
        },
    )