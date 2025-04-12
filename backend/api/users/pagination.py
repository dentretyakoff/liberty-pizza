from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class LargeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = settings.LARGE_DEFAULT_LIMIT
    max_limit = settings.LARGE_MAX_LIMIT
