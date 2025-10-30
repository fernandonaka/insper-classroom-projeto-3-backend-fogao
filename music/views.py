from django.shortcuts import render
import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import FavoriteArtist, FavoriteTrack
from .serializers import (
    FavoriteArtistSerializer, FavoriteTrackSerializer
)
import requests


# Create your views here.
DEEZER = "https://api.deezer.com"

@api_view(["GET"])
@permission_classes([AllowAny])
def search_artists(request):
    q = request.query_params.get("q", "")
    if not q:
        return Response([], status=200)
    r = requests.get(f"{DEEZER}/search/artist", params={"q": q}, timeout=10)
    data = r.json().get("data", [])

    #mapeia para um payload enxuto (id, nome, foto_)
    artistas = []
    for it in data:
        artistas.append({
                "deezer_id":it.get("id"),
                "name": it.get("name"),
                "picture": it.get("picture_medium") or it.get("picture"),
                "raw_json": it
            }
        )
    
    return Response(artistas, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_tracks(request):
    q = request.query_params.get("q", "")
    if not q:
        return Response([], status=200)
    r = requests.get(f"{DEEZER}/search/track", params={"q": q}, timeout=10)
    data = r.json().get("data", [])
    tracks = []
    for it in data:
        tracks.append({
                "deezer_id":it.get("id"),
                "title":it.get("title"),
                "artist_name": (it.get("artist") or {}).get("name"),
                "album_title": (it.get("album") or {}).get("title"),
                "album_cover": (it.get("album") or {}).get("cover_medium"),
                "preview_url": it.get("preview"),
                "raw": it
            }
        )

    return Response(tracks,status=status.HTTP_200_OK)



# --- Helpers Deezer (se já tiver no seu arquivo, pode reaproveitar) ---
DEEZER_ARTIST_URL = "https://api.deezer.com/artist/{id}/"
DEEZER_TRACK_URL  = "https://api.deezer.com/track/{id}/"

# -------- ARTIST --------
@api_view(["GET", "POST", "DELETE"])
def favorite_artist(request, deezer_id: int):
    """
    POST   /favorite/artist/<deezer_id>/  -> cria (global)
    DELETE /favorite/artist/<deezer_id>/  -> remove (global)
    GET    /favorite/artist/<deezer_id>/  -> retorna 1 favorito (global)
    """
    if request.method == "POST":
        # Busca no Deezer para popular os campos (ou use os dados que você já tiver)
        r = requests.get(DEEZER_ARTIST_URL.format(id=deezer_id), timeout=10)
        if r.status_code != 200:
            return Response({"detail": "Deezer não encontrou esse artista."}, status=404)
        data = r.json()

        fav, created = FavoriteArtist.objects.get_or_create(
            deezer_id=deezer_id,
            defaults={
                "name": data.get("name", ""),
                "picture": data.get("picture_medium") or data.get("picture"),
                "raw_json": data,
            },
        )
        # Se já existia, apenas retorna
        serializer = FavoriteArtistSerializer(fav)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    if request.method == "DELETE":
        deleted, _ = FavoriteArtist.objects.filter(deezer_id=deezer_id).delete()
        if deleted == 0:
            return Response({"detail": "Favorito não encontrado."}, status=404)
        return Response(status=204)

    # GET único
    try:
        fav = FavoriteArtist.objects.get(deezer_id=deezer_id)
    except FavoriteArtist.DoesNotExist:
        return Response({"detail": "Favorito não encontrado."}, status=404)
    return Response(FavoriteArtistSerializer(fav).data)


@api_view(["GET"])
def favorite_artist_all(request):
    """GET /favorite/artist/ -> lista global (sem usuário)"""
    favorites = FavoriteArtist.objects.order_by("-created_at")
    return Response(FavoriteArtistSerializer(favorites, many=True).data)


# -------- TRACK --------
@api_view(["GET", "POST", "DELETE"])
def favorite_track(request, deezer_id: int):
    """
    POST   /favorite/track/<deezer_id>/  -> cria (global)
    DELETE /favorite/track/<deezer_id>/  -> remove (global)
    GET    /favorite/track/<deezer_id>/  -> retorna 1 favorito (global)
    """
    if request.method == "POST":
        r = requests.get(DEEZER_TRACK_URL.format(id=deezer_id), timeout=10)
        if r.status_code != 200:
            return Response({"detail": "Deezer não encontrou essa track."}, status=404)
        data = r.json()

        fav, created = FavoriteTrack.objects.get_or_create(
            deezer_id=deezer_id,
            defaults={
                "title": data.get("title", ""),
                "artist_name": (data.get("artist") or {}).get("name", ""),
                "album_title": (data.get("album") or {}).get("title"),
                "album_cover": (data.get("album") or {}).get("cover_medium") or (data.get("album") or {}).get("cover"),
                "preview_url": data.get("preview"),
                "raw_json": data,
            },
        )
        serializer = FavoriteTrackSerializer(fav)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    if request.method == "DELETE":
        deleted, _ = FavoriteTrack.objects.filter(deezer_id=deezer_id).delete()
        if deleted == 0:
            return Response({"detail": "Favorito não encontrado."}, status=404)
        return Response(status=204)

    # GET único
    try:
        fav = FavoriteTrack.objects.get(deezer_id=deezer_id)
    except FavoriteTrack.DoesNotExist:
        return Response({"detail": "Favorito não encontrado."}, status=404)
    return Response(FavoriteTrackSerializer(fav).data)


@api_view(["GET"])
def favorite_track_all(request):
    """GET /favorite/track/ -> lista global (sem usuário)"""
    favorites = FavoriteTrack.objects.order_by("-created_at")
    return Response(FavoriteTrackSerializer(favorites, many=True).data)
