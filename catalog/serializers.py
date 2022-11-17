from rest_framework import serializers
from .models import Band, Album, Track, AlbumItem


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ['id', 'name',]


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'band', 'release_year']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'band']


class AlbumItemSerializer(serializers.ModelSerializer):
    album_name = serializers.ReadOnlyField(source="album.name")
    class Meta:
        model = AlbumItem
        fields = ['album', 'album_name', 'order']


class FullTrackSerializer(serializers.ModelSerializer):
    band_name = serializers.ReadOnlyField(source="band.name")
    album_info = AlbumItemSerializer(many=True)

    class Meta:
        model = Track
        fields = ['id', 'name', 'band', 'band_name', 'album_info']