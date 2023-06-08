from django.core.management.base import BaseCommand
from log_access_apache.utils import parser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        parser()
