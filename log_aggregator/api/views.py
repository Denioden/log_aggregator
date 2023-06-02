from log_access_apache.models import Log
from .serializers import LogSerializer
from .filters import LogFilter

from drf_spectacular.utils import extend_schema

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(
    responses=LogSerializer,
    description='Get a list of logs',
)
class LogList(ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LogFilter
