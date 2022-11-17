from django.contrib import admin
from .models import Band, Album, Track, AlbumItem

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(AlbumItem)
class AlbumItemAdmin(admin.ModelAdmin):
    pass