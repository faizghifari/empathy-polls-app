import uuid
from django.db import models


class VoteSession(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.TextField(null=False, blank=False)
    place = models.TextField(default="", blank=True)
    # is_mandatory = models.BooleanField(default=False)
    open_public = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    notes = models.TextField(default="", blank=True)

    def __str__(self):
        return "%s: %s" % (self.title, self.uuid)


class Timeslot(models.Model):
    session_id = models.ForeignKey(
        VoteSession, related_name="timeslots", on_delete=models.CASCADE, null=False
    )
    datetime = models.DateTimeField(null=False)

    class Meta:
        unique_together = ("session_id", "datetime")

    def __str__(self):
        return "%s: %s" % (self.session_id.title, self.datetime)


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
    voter_name = models.CharField(max_length=50, null=False, blank=False)
    preferences = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=PreferenceChoices.choices,
        default=PreferenceChoices.UNAVAILABLE,
    )
    notes = models.TextField(default="", blank=True)

    class Meta:
        unique_together = ("session_id", "timeslot_id", "voter_name")

    def __str__(self):
        return f"{self.session_id.title} -> {self.voter_name} at {self.timeslot_id.datetime}: {self.preferences.label}"
