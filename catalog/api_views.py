from rest_framework import viewsets
from .models import Band, Album, Track, AlbumItem
from .serializers import BandSerializer, AlbumSerializer, TrackSerializer, AlbumItemSerializer


class BandViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Band instances.
    """
    serializer_class = BandSerializer
    queryset = Band.objects.all()


class AlbumViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Album instances.
    """
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class TrackViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Track instances.
    """
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class AlbumItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing AlbumItem instances.
    """
    serializer_class = AlbumItemSerializer
    queryset = AlbumItem.objects.all()