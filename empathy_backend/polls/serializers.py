from rest_framework import serializers
from .models import VoteSession, Timeslot, Vote


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = "__all__"


class NestedTimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = ["id", "datetime"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        extra_kwargs = {"notes": {"required": False}}

    def validate(self, data):
        voted_ts = Timeslot.objects.get(pk=data["timeslot_id"].id)
        if data["session_id"].uuid != voted_ts.session_id.uuid:
            raise serializers.ValidationError(
                "session_id between vote and timeslot must be the same"
            )
        return data


class AttendaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["voter_name", "preferences", "notes"]


class VoteSessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteSession
        fields = ["uuid", "title", "place", "open_public", "notes"]
        extra_kwargs = {
            "title": {"required": True},
            "place": {"required": False},
            "notes": {"required": False},
        }


class VoteSessionReadSerializer(serializers.ModelSerializer):
    timeslots = NestedTimeslotSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = VoteSession
        fields = "__all__"
