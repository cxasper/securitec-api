from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']


class Artist(models.Model):
    country = models.ForeignKey(
        'Country', models.CASCADE, related_name='artists', null=False
    )
    name = models.CharField(max_length=50, unique=True, null=False)
    about = models.TextField(null=True)

    class Meta:
        ordering = ['id']


class Album(models.Model):
    artist = models.ForeignKey(
        'Artist', models.CASCADE, related_name='albums', null=False
    )
    name = models.CharField(max_length=100, unique=True, null=False)
    cover_page = models.ImageField(null=True)
    description = models.TextField(null=False)
    release_year = models.DateField(null=False)

    class Meta:
        ordering = ['id']


class Song(models.Model):
    album = models.ForeignKey(
        'Album', models.CASCADE, related_name='songs', null=False
    )
    name = models.CharField(max_length=100, unique=True, null=False)
    duration = models.TimeField(null=False)

    class Meta:
        ordering = ['id']
