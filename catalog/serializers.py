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
    class Meta:
        model = AlbumItem
        fields = ['id', 'track', 'album', 'order']


class FullTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'band']