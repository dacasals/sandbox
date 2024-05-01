from django.contrib.auth.models import Group, User
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from polls.models import Choice, Question

from .serializers import (
    ChoiceSerializer,
    GroupSerializer,
    QuestionSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_bulk_update(self, request, *args, **kwargs):
        # restrict the update to the filtered queryset
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    # Modify queryset to populate Question.choices in only 2 queries.

    def get_queryset(self):
        queryset = self.queryset
        return queryset.prefetch_related("choice_set")


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
