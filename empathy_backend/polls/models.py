import uuid
from django.db import models


class VoteSession(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    title = models.TextField(null=False, unique=True)
    place = models.TextField()
    is_mandatory = models.BooleanField(default=False)
    open_public = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    notes = models.TextField()


class Timeslot(models.Model):
    session_id = models.ForeignKey(
        VoteSession, related_name="timeslots", on_delete=models.CASCADE, null=False
    )
    datetime = models.DateTimeField(null=False)


class Vote(models.Model):
    class PreferenceChoices(models.TextChoices):
        UNAVAILABLE = "UN", "Unavailable"
        LEAST = "LE", "Least Preferred"
        OKAY = "OK", "Okay"
        MOST = "MOST", "Most Preferred"

    session_id = models.ForeignKey(
        VoteSession, related_name="votes", on_delete=models.CASCADE, null=False
    )
    timeslot_id = models.ForeignKey(
        Timeslot, related_name="voted_timeslot", on_delete=models.CASCADE, null=False
    )
    voter_name = models.CharField(max_length=50, unique=True, null=False)
    preferences = models.CharField(
        max_length=50,
        null=False,
        choices=PreferenceChoices.choices,
        default=PreferenceChoices.UNAVAILABLE,
    )
    notes = models.TextField()
