from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .forms import UserChangeForm, UserCreationForm
from .models import Team

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (
            "User",
            {
                "fields": (
                    "happiness_level",
                    "happiness_level_changed",
                    "team",
                    "timezone",
                    "name",
                )
            },
        ),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = (
        "username",
        "name",
        "is_superuser",
        "team",
        "happiness_level",
        "can_change_happiness_level",
    )
    list_filter = ("team", "happiness_level", "is_superuser")
    search_fields = ["name"]
    autocomplete_fields = ["team"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ["name"]
