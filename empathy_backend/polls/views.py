from django.shortcuts import redirect

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import VoteSession, Timeslot, Vote
from .serializers import (
    VoteSessionReadSerializer,
    VoteSessionWriteSerializer,
    AttendaceSerializer,
    TimeslotSerializer,
    VoteSerializer,
)


class TimeslotViewSet(viewsets.ModelViewSet):
    serializer_class = TimeslotSerializer
    queryset = Timeslot.objects.all()


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


class VoteSessionViewSet(viewsets.ModelViewSet):
    queryset = VoteSession.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return VoteSessionWriteSerializer
        return VoteSessionReadSerializer

    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()
        if session.is_finished:
            return redirect("votesession-results", pk=session.uuid)
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        session = self.get_object()
        if not session.is_finished:
            session.is_finished = True
            session.save()
        serialized_session = VoteSessionReadSerializer(session)
        results = serialized_session.data.copy()
        vote_results = results["timeslots"].copy()
        for ts in vote_results:
            ts["count_vote"] = 0
            ts["count_most"] = 0
            ts["count_okay"] = 0
            ts["count_least"] = 0
            ts["attendance"] = []
            for v in serialized_session.data["votes"]:
                if v["preferences"] != "UN" and v["timeslot_id"] == ts["id"]:
                    ts["count_vote"] += 1
                    if v["preferences"] == "MOST":
                        ts["count_most"] += 1
                    elif v["preferences"] == "OK":
                        ts["count_okay"] += 1
                    elif v["preferences"] == "LE":
                        ts["count_least"] += 1
                    attendee = Vote.objects.get(pk=v["id"])
                    ts["attendance"].append(AttendaceSerializer(attendee).data)
        vote_results = sorted(
            vote_results,
            key=lambda i: i["count_vote", "count_most", "count_okay", "count_least"],
            reverse=True,
        )
        results["vote_results"] = vote_results
        return Response(results)
