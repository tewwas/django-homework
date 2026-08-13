from django.shortcuts import render
from django.utils import timezone

from .models import Match


def matches_list(request):
    matches = Match.objects.order_by("-start_time")

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

    matches = Match.objects.filter(
        start_time__lte=now,
        end_time__gt=now,
    ).order_by("start_time")

    return render(
        request,
        "matches/match_list.html",
        {
            "matches": matches,
            "title": "Матчи в прямом эфире",
        },
    )


def matches_future(request):
    now = timezone.now()

    matches = Match.objects.filter(
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