from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Match, SportTournament


class MatchViewsTests(TestCase):
    def setUp(self):
        now = timezone.now()

        self.tournament = SportTournament.objects.create(
            name="Summer Cup",
            start_date=now.date(),
            end_date=now.date() + timedelta(days=7),
        )

        self.old_match = Match.objects.create(
            location="Arena 1",
            start_time=now - timedelta(days=2),
            end_time=now - timedelta(days=2) + timedelta(hours=2),
            team1="Team A",
            team2="Team B",
        )

        self.live_match = Match.objects.create(
            location="Arena 2",
            start_time=now - timedelta(hours=1),
            end_time=now + timedelta(hours=1),
            team1="Team C",
            team2="Team D",
            tournament=self.tournament,
        )

        self.future_match = Match.objects.create(
            location="Arena 3",
            start_time=now + timedelta(hours=2),
            end_time=now + timedelta(hours=4),
            team1="Team E",
            team2="Team F",
        )

        self.later_match = Match.objects.create(
            location="Arena 4",
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, hours=2),
            team1="Team G",
            team2="Team H",
        )

        self.finished_tournament_match = Match.objects.create(
            location="Arena 5",
            start_time=now - timedelta(hours=4),
            end_time=now - timedelta(hours=2),
            team1="Team I",
            team2="Team J",
            score_team1=2,
            score_team2=1,
            winner="Team I",
            tournament=self.tournament,
        )

        self.finished_tournament_match_2 = Match.objects.create(
            location="Arena 6",
            start_time=now - timedelta(hours=3),
            end_time=now - timedelta(hours=1),
            team1="Team K",
            team2="Team L",
            score_team1=0,
            score_team2=3,
            winner="Team L",
            tournament=self.tournament,
        )

        self.future_tournament_match = Match.objects.create(
            location="Arena 7",
            start_time=now + timedelta(hours=3),
            end_time=now + timedelta(hours=5),
            team1="Team M",
            team2="Team N",
            tournament=self.tournament,
        )

    def test_matches_list(self):

        response = self.client.get(reverse("matches"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["matches"]),
            [
                self.later_match,
                self.future_tournament_match,
                self.future_match,
                self.live_match,
                self.finished_tournament_match_2,
                self.finished_tournament_match,
                self.old_match,
            ],
        )

    def test_live_matches(self):
        response = self.client.get(reverse("matches_live"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["matches"]),
            [self.live_match],
        )

    def test_future_matches(self):
        response = self.client.get(reverse("matches_future"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["matches"]),
            [
                self.future_match,
                self.future_tournament_match,
                self.later_match,
            ],
        )

    def test_match_detail(self):
        response = self.client.get(
            reverse("match_detail", args=[self.live_match.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["match"], self.live_match)

        self.assertContains(response, "Team C")
        self.assertContains(response, "Team D")
        self.assertContains(response, "Arena 2")
        self.assertContains(response, "Summer Cup")

        self.assertContains(
            response,
            self.tournament.start_date.strftime("%d.%m.%Y"),
        )

        self.assertContains(
            response,
            self.tournament.end_date.strftime("%d.%m.%Y"),
        )

        self.assertContains(
            response,
            reverse(
                "tournament_detail",
                args=[self.tournament.id],
            ),
        )

    def test_match_detail_not_found(self):
        response = self.client.get(
            reverse("match_detail", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    def test_tournaments_list(self):
        response = self.client.get(reverse("tournaments"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["tournaments"]),
            [self.tournament],
        )

        self.assertEqual(
            response.context["tournaments"][0].finished_matches_count,
            2,
        )

        self.assertContains(response, "Summer Cup")
        self.assertContains(response, "(2)")

        self.assertContains(
            response,
            reverse(
                "tournament_detail",
                args=[self.tournament.id],
            ),
        )

    def test_tournament_detail(self):
        response = self.client.get(
            reverse(
                "tournament_detail",
                args=[self.tournament.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tournament"], self.tournament)

        self.assertEqual(
            list(response.context["matches"]),
            [
                self.finished_tournament_match,
                self.finished_tournament_match_2,
                self.live_match,
                self.future_tournament_match,
            ],
        )

        self.assertContains(response, "Summer Cup")
        self.assertContains(response, "Team I")
        self.assertContains(response, "Team J")
        self.assertContains(response, "2 : 1")
        self.assertContains(response, "Team I")
        self.assertContains(response, "Team M")
        self.assertContains(response, "Team N")

        self.assertContains(
            response,
            reverse(
                "match_detail",
                args=[self.finished_tournament_match.id],
            ),
        )

        self.assertContains(
            response,
            reverse(
                "match_detail",
                args=[self.future_tournament_match.id],
            ),
        )

    def test_tournament_detail_not_found(self):
        response = self.client.get(
            reverse(
                "tournament_detail",
                args=[999999],
            )
        )

        self.assertEqual(response.status_code, 404)