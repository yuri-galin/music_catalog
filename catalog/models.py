import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def max_year_validator(value):
    return MaxValueValidator(datetime.date.today().year)(value)


class Band(models.Model):
    # the longest existing band name is 68 characters long
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(models.Model):
    # the longest existing album name is 865 characters long
    name = models.CharField(max_length=1000)
    band = models.ForeignKey(Band, related_name='albums', on_delete=models.CASCADE)
    # the first album ever was recorded in 1889 by Emile Berliner
    release_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1889), max_year_validator])

    def __str__(self):
        return self.name


class Track(models.Model):
    # the longest existing song name is 481 characters long
    name = models.CharField(max_length=600)
    band = models.ForeignKey(Band, related_name='tracks', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AlbumItem(models.Model):
    track = models.ForeignKey(Track, related_name='album_info', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='album_items', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"'{self.track}' in {self.album}"

    class Meta:
        verbose_name = "album item"
        verbose_name_plural = "album items"
        ordering = ('track', 'order', 'album')
        unique_together = (('track', 'order'),
                           ('track', 'album'),
                           ('order', 'album'))
