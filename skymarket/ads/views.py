from django.contrib.auth import get_user_model
from rest_framework import pagination, viewsets
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Ad, Comment
from .permissions import IsOwnerOrAdmin
from .serializers import (
    AdSerializer,
    CommentSerializer,
    AdDetailSerializer,
    AdsByUserSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdModelFilter

User = get_user_model()


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdModelFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return AdSerializer
        if self.action == 'retrieve':
            return AdDetailSerializer
        if self.action == 'partial_update':
            return AdDetailSerializer
        if self.action == 'create':
            return AdDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            author_id=self.request.user.id,
        )

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny(), ]
        elif self.action == 'retrieve':
            return [IsAuthenticated(), ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            return [IsOwnerOrAdmin(), ]

        return super(self.__class__, self).get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('ad')
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, pk=ad_id)

        return self.queryset.filter(ad=ad)

    def perform_create(self, serializer):
        serializer.save(
            author_id=self.request.user.id,
            ad_id=self.kwargs.get('ad_pk'),
        )

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated(), ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            return [IsOwnerOrAdmin(), ]

        return super(self.__class__, self).get_permissions()


class AdsByUserListView(ListAPIView):
    queryset = Ad.objects.all().select_related('author')
    serializer_class = AdsByUserSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id
        user = get_object_or_404(User, pk=user_id)

        return self.queryset.filter(author=user)
