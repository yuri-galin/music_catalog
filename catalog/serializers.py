from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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

    def validate_album_info(self, album_info):
        # We need to add custom validation for album_info in order to check that album and order are unique everywhere
        albums = []
        order = []
        for album_item in album_info:
            if album_item["album"] in albums:
                error = f'You tried to add a track to the album with id {album_item["album"].id} more than once.'
                raise ValidationError(error)
            else:
                albums.append(album_item["album"])

            if album_item["order"] in order:
                error = f'A track must have a unique order field for each album. You tried to create a track ' \
                        f'with order {album_item["order"]} for more than one album.'
                raise ValidationError(error)
            else:
                order.append(album_item["order"])

        return album_info

    def create(self, validated_data):
        # In order for the endpoint to support POST we need to create a custom create method
        album_info_data = validated_data.pop('album_info')

        track = Track.objects.create(**validated_data)

        for album_info in album_info_data:
            AlbumItem.objects.create(track=track, album=album_info["album"], order=album_info["order"])

        return track

