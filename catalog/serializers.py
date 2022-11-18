from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from .models import Band, Album, Track, AlbumItem


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ['id', 'name',]


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'band', 'release_year']


class AlbumItemSerializer(serializers.ModelSerializer):
    album_name = serializers.ReadOnlyField(source="album.name")
    class Meta:
        model = AlbumItem
        fields = ['id', 'album', 'album_name', 'order']

    def run_validators(self, value):
        # We need to remove UniqueTogetherValidator because of DRF restrictions on nested objects.
        # Read more here: https://github.com/encode/django-rest-framework/issues/2996#issuecomment-151275959
        if self.context['request'].method == "PUT":
            for validator in self.validators:
                if isinstance(validator, UniqueTogetherValidator):
                    self.validators.remove(validator)
        super(AlbumItemSerializer, self).run_validators(value)


class TrackSerializer(serializers.ModelSerializer):
    band_name = serializers.ReadOnlyField(source="band.name")
    album_info = AlbumItemSerializer(many=True)

    class Meta:
        model = Track
        fields = ['id', 'name', 'band', 'band_name', 'album_info']

    def validate_album_info(self, album_info):
        # We need to add custom validation for album_info in order to check that album and order are unique everywhere
        # DRF doesn't support UniqueTogether validation for nested serializers
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

            if album_item["album"].band.id != self.initial_data["band"]:
                error = f'You cannot add a track of the band with id {self.initial_data["band"]} to the album of ' \
                        f'the band with id {album_item["album"].band.id}.'
                raise ValidationError(error)

            if self.context['request'].method == "PUT":
                try:
                    track_id = self.context.get('request').parser_context.get('kwargs').get('id')
                    album_item_same_order = AlbumItem.objects.get(album=album_item["album"],
                                                                  order=album_item["order"],
                                                                  track=track_id)

                    error = f'You cannot add a track with order number {album_item["order"]} to the album ' \
                            f'with id {album_item["album"].id} because it already has a track with this order number.'
                    raise ValidationError(error)
                except AlbumItem.DoesNotExist:
                    try:
                        album_item_same_order = AlbumItem.objects.get(album=album_item["album"],
                                                                      order=album_item["order"])

                        error = f'You cannot add a track with order number {album_item["order"]} to the album ' \
                                f'with id {album_item["album"].id} because it already has a track with this order number.'
                        raise ValidationError(error)
                    except AlbumItem.DoesNotExist:
                        pass

        return album_info

    def create(self, validated_data):
        # In order for the endpoint to support POST on our nested serializer we need to create a custom create method
        album_info_data = validated_data.pop('album_info')

        track = Track.objects.create(**validated_data)

        for album_info in album_info_data:
            AlbumItem.objects.create(track=track, album=album_info["album"], order=album_info["order"])

        return track

    def update(self, instance, validated_data):
        # In order for the endpoint to support PUT on our nested serializer we need to create a custom update method
        album_info_data = validated_data.pop('album_info', {})

        track = super(TrackSerializer, self).update(instance, validated_data)

        album_items = track.album_info.all()
        items_put = []
        for album_info in album_info_data:
            # if item exists - change
            if album_items.filter(album=album_info["album"]).count() == 1:
                album_item = album_items.filter(album=album_info["album"])[0]
                updated_fields = []
                for key in album_info:
                    if hasattr(album_item, key):
                        setattr(album_item, key, album_info[key])
                        updated_fields.append(key)

                album_item.save(update_fields=updated_fields)

                items_put.append(album_item.id)
            elif album_items.filter(order=album_info["order"]).count() == 1:
                album_item = album_items.filter(order=album_info["order"])[0]
                updated_fields = []
                for key in album_info:
                    if hasattr(album_item, key):
                        setattr(album_item, key, album_info[key])
                        updated_fields.append(key)

                album_item.save(update_fields=updated_fields)

                items_put.append(album_item.id)
            else:
                item = AlbumItem.objects.create(track=track, album=album_info["album"], order=album_info["order"])
                items_put.append(item.id)

        for item in album_items.exclude(id__in=items_put):
            item.delete()

        return track