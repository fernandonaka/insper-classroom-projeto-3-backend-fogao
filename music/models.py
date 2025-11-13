
from django.db import models
from django.contrib.auth.models import User

class FavoriteArtist(models.Model):
    # Removido o FK para user
    deezer_id  = models.PositiveBigIntegerField()
    name       = models.CharField(max_length=255)
    picture    = models.URLField(blank=True, null=True)
    raw_json   = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'deezer_id')
    
    def __str__(self):
        return f"{self.name} ({self.deezer_id})"


class FavoriteTrack(models.Model):
    # Removido o FK para user
    deezer_id    = models.PositiveBigIntegerField()
    title        = models.CharField(max_length=255)
    artist_name  = models.CharField(max_length=255)
    album_title  = models.CharField(max_length=255, blank=True, null=True)
    album_cover  = models.URLField(blank=True, null=True)
    preview_url  = models.URLField(blank=True, null=True)
    raw_json     = models.JSONField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'deezer_id')
    
    def __str__(self):
        return f"{self.title} - {self.artist_name} ({self.deezer_id})"

class FavoriteAlbum(models.Model):
    # Removido o FK para user
    deezer_id   = models.PositiveBigIntegerField()
    title       = models.CharField(max_length=255)
    artist_name     = models.CharField(max_length=255)
    cover       = models.URLField(blank=True, null=True)
    raw_json    = models.JSONField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'deezer_id')
    

    def __str__(self):
        return f"{self.title} - {self.artist_name} ({self.deezer_id})"
    

class ListTrack(models.Model):
    # Removido o FK para user
    deezer_id    = models.PositiveBigIntegerField()
    title        = models.CharField(max_length=255)
    artist_name  = models.CharField(max_length=255)
    album_title  = models.CharField(max_length=255, blank=True, null=True)
    album_cover  = models.URLField(blank=True, null=True)
    preview_url  = models.URLField(blank=True, null=True)
    raw_json     = models.JSONField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'deezer_id')
    
    def __str__(self):
        return f"{self.title} - {self.artist_name} ({self.deezer_id})"