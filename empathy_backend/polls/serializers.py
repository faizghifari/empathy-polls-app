from rest_framework import serializers
from .models import VoteSession, Timeslot, Vote


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        extra_kwargs = {
            "notes": {"required": False},
        }


class VoteSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteSession
        fields = "__all__"
        extra_kwargs = {
            "title": {"required": True},
            "place": {"required": False},
            "notes": {"required": False},
        }
