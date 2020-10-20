from django.db.models import Sum
from rest_framework import serializers
from apps.api.models import Artist, Album


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, instance):
        all_songs = instance.songs.all()
        if all_songs:
            split_timedelta = str(all_songs.aggregate(Sum('duration'))['duration__sum']).split(':')
            total_minutes = int(split_timedelta[1]) + (int(split_timedelta[0])*60)
            return '%s:%s' %(total_minutes, split_timedelta[2])
        return '00:00'

    class Meta:
        model = Album
        fields = '__all__'
