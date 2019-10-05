from django.db.models import Count, Avg
from rest_framework import serializers

from .models import User, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        read_only_fields = ("id", "name")
        fields = read_only_fields


class UserSerializer(serializers.ModelSerializer):
    statistics = serializers.SerializerMethodField(source="*")
    team = TeamSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "happiness_level",
            "statistics",
            "team",
        )
        read_only_fields = ("username", "id", "statistics", "team")

    def validate_happiness_level(self, value):
        if self.instance and not self.instance.can_change_happiness_level:
            raise serializers.ValidationError(
                "Users can update their happiness level only once per day."
            )
        return value

    def get_statistics(self, obj):
        user_count_by_happiness_level = obj.__class__.objects \
            .filter(team=obj.team) \
            .values("happiness_level") \
            .annotate(user_count=Count("id")) \
            if obj.team else None

        average_team_happiness = obj.__class__.objects \
            .filter(team=obj.team) \
            .values("team_id") \
            .annotate(average_team_happiness=Avg("happiness_level"))[0]["average_team_happiness"] \
            if obj.team else None

        return {
            "user_count_by_happiness_level": user_count_by_happiness_level,
            "average_team_happiness": average_team_happiness,
        }
