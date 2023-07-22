from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class BasePagination(PageNumberPagination):
    page_size_query_param = "page_limit"


class ModelViewSet(ModelViewSet):
    pagination_class = BasePagination

    def paginate_queryset(self, queryset):
        if not getattr(queryset, "ordered", False):
            queryset = queryset.order_by("-id")
        if "nopagination" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)