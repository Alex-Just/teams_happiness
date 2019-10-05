from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ForeignKey, Model, SET_NULL
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import MonitorField
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
    happiness_level_changed = MonitorField(monitor="happiness_level", blank=True, null=True)
    team = ForeignKey("users.Team", on_delete=SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.id})"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def can_change_happiness_level(self):
        if not self.happiness_level_changed:
            return
        user_tz_now = datetime.now(self.timezone)
        return user_tz_now - self.happiness_level_changed > timedelta(days=1)


class Team(Model):
    name = CharField(_("Name of Team"), max_length=255)

    def __str__(self):
        return f"{self.name} ({self.id})"
