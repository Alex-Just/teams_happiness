from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ForeignKey, Model, SET_NULL
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from timezone_field import TimeZoneField


class User(AbstractUser):
    HAPPINESS_CHOICES = Choices(
        (1, "Unhappy", _("Unhappy")),
        (3, "Neutral", _("Neutral")),
        (5, "Very Happy", _("Very Happy")),
    )

    # First Name and Last Name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    timezone = TimeZoneField(_("Timezone of User"), blank=True, default="UTC")
    happiness_level = IntegerField(choices=HAPPINESS_CHOICES, default=HAPPINESS_CHOICES.Neutral)
    team = ForeignKey("users.Team", on_delete=SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Team(Model):
    name = CharField(_("Name of Team"), max_length=255)
