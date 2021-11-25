from django.contrib import admin

from .models import VoteSession, Timeslot, Vote

admin.site.register(VoteSession)
admin.site.register(Timeslot)
admin.site.register(Vote)
