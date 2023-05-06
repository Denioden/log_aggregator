from django_filters import rest_framework as filters
from log_access_apache.models import Log


class LogFilter(filters.FilterSet):

    remote_host = filters.CharFilter()

    request_time = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Log
        fields = ['remote_host', 'request_time']
