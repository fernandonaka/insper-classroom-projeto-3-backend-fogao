
from django.db import models

class FavoriteArtist(models.Model):
    # Removido o FK para user
    deezer_id  = models.PositiveBigIntegerField(unique=True)
    name       = models.CharField(max_length=255)
    picture    = models.URLField(blank=True, null=True)
    raw_json   = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.deezer_id})"


class FavoriteTrack(models.Model):
    # Removido o FK para user
    deezer_id    = models.PositiveBigIntegerField(unique=True)
    title        = models.CharField(max_length=255)
    artist_name  = models.CharField(max_length=255)
    album_title  = models.CharField(max_length=255, blank=True, null=True)
    album_cover  = models.URLField(blank=True, null=True)
    preview_url  = models.URLField(blank=True, null=True)
    raw_json     = models.JSONField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist_name} ({self.deezer_id})"
