from rest_framework import viewsets
from rest_framework.response import Response

from .models import VoteSession, Timeslot, Vote
from .serializers import (
    VoteSessionReadSerializer,
    VoteSessionWriteSerializer,
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
