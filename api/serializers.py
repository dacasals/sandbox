from django.contrib.auth.models import Group, User
from rest_framework import serializers

from api.bulk_serializers import BulkSerializerMixin, BulkListSerializer
from polls.models import Choice, Question


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ["url", "votes", "choice_text"]


class QuestionSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True)

    class Meta:
        model = Question
        fields = ["url", "question_text", "pub_date", "choices", "date_created"]
        list_serializer_class = BulkListSerializer
        # Since request defined in test use url we set this property to identify from where to extract model pk
        update_lookup_field = "url"
        lookup_field_type = int
