from .api_views import BandViewSet, AlbumViewSet, TrackViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/bands', BandViewSet, basename='band')
router.register(r'api/albums', AlbumViewSet, basename='album')
router.register(r'api/tracks', TrackViewSet, basename='tracks')
urlpatterns = router.urls