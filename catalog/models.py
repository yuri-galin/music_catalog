from django.db import models


class Band(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=200)
    band = models.ForeignKey(Band, related_name='albums', on_delete=models.CASCADE)
    release_year = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=200)
    band = models.ForeignKey(Band, related_name='tracks', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AlbumItem(models.Model):
    track = models.ForeignKey(Track, related_name='album_items', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='album_items', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"'{self.name}' in {self.album}"

    class Meta:
        verbose_name = "album item"
        verbose_name_plural = "album items"
        ordering = ('track', 'order', 'album')
        unique_together = (('track', 'order'),
                           ('track', 'album'))