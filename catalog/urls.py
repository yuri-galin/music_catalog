from .api_views import BandViewSet, AlbumViewSet, TrackViewSet, AlbumItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/bands', BandViewSet, basename='band')
router.register(r'api/albums', AlbumViewSet, basename='album')
router.register(r'api/tracks', TrackViewSet, basename='track')
router.register(r'api/album_items', AlbumItemViewSet, basename='album_item')
urlpatterns = router.urls