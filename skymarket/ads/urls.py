from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import AdViewSet, CommentViewSet, AdsByUserListView

router = SimpleRouter()
router.register('ads', AdViewSet)

comments_router = NestedSimpleRouter(
    router,
    'ads',
    lookup='ad'
)
comments_router.register('comments', CommentViewSet, basename='ad-comments')

urlpatterns = [
    path('ads/me/', AdsByUserListView.as_view()),
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
]
