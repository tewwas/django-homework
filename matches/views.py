from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MatchForm, TournamentForm
from .models import Match, SportTournament
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MatchForm, TournamentForm


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


def match_create(request):
    if request.method == "POST":
        form = MatchForm(request.POST)

        if form.is_valid():
            match = form.save()
            return redirect("match_detail", match_id=match.id)
    else:
        form = MatchForm()

    return render(
        request,
        "matches/match_form.html",
        {
            "form": form,
            "title": "Создание матча",
            "button_text": "Создать матч",
        },
    )


def match_edit(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    if request.method == "POST":
        form = MatchForm(request.POST, instance=match)

        if form.is_valid():
            match = form.save()
            return redirect("match_detail", match_id=match.id)
    else:
        form = MatchForm(instance=match)

    return render(
        request,
        "matches/match_form.html",
        {
            "form": form,
            "title": "Редактирование матча",
            "button_text": "Сохранить изменения",
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


def tournament_create(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)

        if form.is_valid():
            tournament = form.save()
            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )
    else:
        form = TournamentForm()

    return render(
        request,
        "matches/tournament_form.html",
        {
            "form": form,
            "title": "Создание турнира",
            "button_text": "Создать турнир",
        },
    )


def tournament_edit(request, tournament_id):
    tournament = get_object_or_404(
        SportTournament,
        pk=tournament_id,
    )

    if request.method == "POST":
        form = TournamentForm(
            request.POST,
            instance=tournament,
        )

        if form.is_valid():
            tournament = form.save()
            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )
    else:
        form = TournamentForm(instance=tournament)

    return render(
        request,
        "matches/tournament_form.html",
        {
            "form": form,
            "title": "Редактирование турнира",
            "button_text": "Сохранить изменения",
        },
    )

def match_create(request):
    if request.method == "POST":
        form = MatchForm(request.POST)

        if form.is_valid():
            match = form.save()
            return redirect("match_detail", match_id=match.id)
    else:
        form = MatchForm()

    return render(
        request,
        "matches/match_form.html",
        {
            "form": form,
            "title": "Создание матча",
            "button_text": "Создать матч",
        },
    )


def match_edit(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    if request.method == "POST":
        form = MatchForm(request.POST, instance=match)

        if form.is_valid():
            match = form.save()
            return redirect("match_detail", match_id=match.id)
    else:
        form = MatchForm(instance=match)

    return render(
        request,
        "matches/match_form.html",
        {
            "form": form,
            "title": "Редактирование матча",
            "button_text": "Сохранить",
        },
    )


def tournament_create(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)

        if form.is_valid():
            tournament = form.save()
            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )
    else:
        form = TournamentForm()

    return render(
        request,
        "matches/tournament_form.html",
        {
            "form": form,
            "title": "Создание турнира",
            "button_text": "Создать турнир",
        },
    )


def tournament_edit(request, tournament_id):
    tournament = get_object_or_404(
        SportTournament,
        pk=tournament_id,
    )

    if request.method == "POST":
        form = TournamentForm(
            request.POST,
            instance=tournament,
        )

        if form.is_valid():
            tournament = form.save()
            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )
    else:
        form = TournamentForm(instance=tournament)

    return render(
        request,
        "matches/tournament_form.html",
        {
            "form": form,
            "title": "Редактирование турнира",
            "button_text": "Сохранить",
        },
    )