from rest_framework import serializers
from .models import  FavoriteAlbum, FavoriteArtist, FavoriteTrack



class FavoriteArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteArtist
        fields = ["deezer_id","name","picture"]

class FavoriteTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTrack
        fields = ["deezer_id", "title", "artist_name", "album_title","album_cover", "preview_url"]

class FavoriteAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAlbum
        fields = ["deezer_id", "album_title", "artist_name", "album_cover"]