from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"vote_session", views.VoteSessionViewSet)
router.register(r"timeslot", views.TimeslotViewSet)
router.register(r"vote", views.VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
