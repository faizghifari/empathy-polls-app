from rest_framework import serializers
from .models import VoteSession, Timeslot, Vote


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    preferences = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = "__all__"
        extra_kwargs = {"notes": {"required": False}}

    def get_preferences(self, obj):
        return obj.get_preferences_display()

    def validate(self, data):
        voted_ts = Timeslot.objects.get(pk=data["timeslot_id"].id)
        if data["session_id"].uuid != voted_ts.session_id.uuid:
            raise serializers.ValidationError(
                "session_id between vote and timeslot must be the same"
            )
        return data


class VoteSessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteSession
        fields = ["uuid", "title", "place", "is_mandatory", "open_public", "notes"]
        extra_kwargs = {
            "title": {"required": True},
            "place": {"required": False},
            "notes": {"required": False},
        }


class VoteSessionReadSerializer(serializers.ModelSerializer):
    timeslots = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="datetime"
    )
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = VoteSession
        fields = "__all__"
