from django import forms

from .models import Match, SportTournament


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            "location",
            "start_time",
            "end_time",
            "team1",
            "team2",
            "score_team1",
            "score_team2",
            "winner",
            "tournament",
        ]

        widgets = {
            "start_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
            "end_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M"]


class TournamentForm(forms.ModelForm):
    class Meta:
        model = SportTournament
        fields = [
            "name",
            "start_date",
            "end_date",
        ]

        widgets = {
            "start_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
            "end_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_date"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_date"].input_formats = ["%Y-%m-%dT%H:%M"]