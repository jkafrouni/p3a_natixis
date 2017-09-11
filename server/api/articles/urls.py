from rest_framework import routers

from .views import ArticleViewSet, SourceViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)
router.register(r'sources', SourceViewSet)
