from django.db.models import Sum
from rest_framework import serializers
from apps.api.models import Artist, Album, Song, Country
from apps.api.utils import format_mintute_seconds


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, instance):
        all_songs = instance.songs.all()
        if all_songs:
            return format_mintute_seconds(all_songs.aggregate(Sum('duration'))['duration__sum'])
        return '00:00'

    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        duration = representation.pop('duration')
        representation['duration'] = format_mintute_seconds(duration)
        return representation
