from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

from .models import VoteSession, Timeslot, Vote
from .serializers import VoteSessionSerializer, TimeslotSerializer, VoteSerializer


class VoteSessionViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSessionSerializer
    queryset = VoteSession.objects.all()


class TimeslotViewSet(viewsets.ModelViewSet):
    serializer_class = TimeslotSerializer
    queryset = Timeslot.objects.all()


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
