from django.shortcuts import render
import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import FavoriteArtist, FavoriteTrack, FavoriteAlbum, ListTrack
from .serializers import (
    FavoriteAlbumSerializer, FavoriteArtistSerializer, FavoriteTrackSerializer, ListTrackSerializer
)
import requests
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

#------------PEGAR TOKEN------------
@api_view(['POST'])
def api_get_token(request):
    try:
        if request.method == 'POST':
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({"token":token.key})
            else:
                return HttpResponseForbidden()
    except:
        return HttpResponseForbidden()
#PARA RODAR VER OS PASSOS 6 e 7 do HANDOUT 11
#--------CRIAR USER--------
@api_view(['POST'])
def api_user(request):
    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        
        if created:
            user.set_password(password)
            user.save()
            return Response({"detail": "Usuário cadastrado com sucesso"},status=204)
        
        return Response({"detail": "Usuário já cadastrado"}, status=204)
    
# Create your views here.
DEEZER = "https://api.deezer.com"

# --- Helpers Deezer (se já tiver no seu arquivo, pode reaproveitar) ---
DEEZER_ARTIST_URL = "https://api.deezer.com/artist/{id}/"
DEEZER_TRACK_URL  = "https://api.deezer.com/track/{id}/"
DEEZER_ALBUM_URL  = "https://api.deezer.com/album/{id}/"

#-------------LIST Track ------------- #PAREI AQUI (FAZENDO O LIST TRACK POST, GET e DELETE)
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def list_track(request, deezer_id:int):
    """
    POST   /list/<deezer_id>/  -> adiciona 1 track na lista (global)
    DELETE /favorite/<deezer_id>/  -> remove 1 track listada (global)
    GET    /favorite/<deezer_id>/  -> retorna 1 track listada (global)
    """
    if request.method == "POST":
        r = requests.get(DEEZER_TRACK_URL.format(id=deezer_id), timeout=10)
        if r.status_code != 200:
            return Response({"detail": "Deezer não encontrou essa track."}, status=404)
        data = r.json()

        list_track, created = ListTrack.objects.get_or_create(
            deezer_id=deezer_id,
            user=request.user,
            defaults={
                "title": data.get("title", ""),
                "artist_name": (data.get("artist") or {}).get("name", ""),
                "album_title": (data.get("album") or {}).get("title"),
                "album_cover": (data.get("album") or {}).get("cover_medium") or (data.get("album") or {}).get("cover"),
                "preview_url": data.get("preview"),
                "raw_json": data,
            },
        )
        serializer = ListTrackSerializer(list_track)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    if request.method == "DELETE":
        deleted, _ = ListTrack.objects.filter(user=request.user, deezer_id=deezer_id).delete()
        if deleted == 0:
            return Response({"detail": "Música não encontrada na lista."}, status=404)
        return Response(status=204)

    # GET único
    try:
        list_track = ListTrack.objects.get(user=request.user, deezer_id=deezer_id)
    except ListTrack.DoesNotExist:
        return Response({"detail": "Música não encontrada na lista."}, status=404)
    return Response(ListTrackSerializer(list_track).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_track_all(request):
    """GET /favorite/track/ -> lista global (sem usuário)"""
    list_tracks = ListTrack.objects.filter(user=request.user)
    return Response(FavoriteTrackSerializer(list_tracks, many=True).data)
    




#-------------------SEARCH-----------------


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

@api_view(["GET"])
@permission_classes([AllowAny])
def search_albums(request):
    q = request.query_params.get("q", "")
    if not q:
        return Response([], status=200)
    r = requests.get(f"{DEEZER}/search/album", params={"q": q}, timeout=10)
    data = r.json().get("data", [])

    #mapeia para um payload enxuto (id, nome, foto_)
    albums = []
    for it in data:
        albums.append({
                "deezer_id":it.get("id"),
                "title":it.get("title"),
                "artist_name": (it.get("artist") or {}).get("name"),
                "cover": it.get("cover_medium"),
                "raw_json": it
            }
        )
    
    return Response(albums, status=status.HTTP_200_OK)




# -------- ARTIST --------
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
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
            user=request.user,
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
        deleted, _ = FavoriteArtist.objects.filter(user=request.user,deezer_id=deezer_id).delete()
        if deleted == 0:
            return Response({"detail": "Favorito não encontrado."}, status=404)
        return Response(status=204)

    # GET único
    try:
        fav = FavoriteArtist.objects.get(user=request.user, deezer_id=deezer_id)
    except FavoriteArtist.DoesNotExist:
        return Response({"detail": "Favorito não encontrado."}, status=404)
    return Response(FavoriteArtistSerializer(fav).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def favorite_artist_all(request):
    """GET /favorite/artist/ -> lista global (sem usuário)"""
    favorites = FavoriteArtist.objects.filter(user=request.user)
    return Response(FavoriteArtistSerializer(favorites, many=True).data)


# -------- TRACK --------
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
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
            user=request.user,
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
        deleted, _ = FavoriteTrack.objects.filter(user=request.user, deezer_id=deezer_id).delete()
        if deleted == 0:
            return Response({"detail": "Favorito não encontrado."}, status=404)
        return Response(status=204)

    # GET único
    try:
        fav = FavoriteTrack.objects.get(user=request.user, deezer_id=deezer_id)
    except FavoriteTrack.DoesNotExist:
        return Response({"detail": "Favorito não encontrado."}, status=404)
    return Response(FavoriteTrackSerializer(fav).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def favorite_track_all(request):
    """GET /favorite/track/ -> lista global (sem usuário)"""
    favorites = FavoriteTrack.objects.filter(user=request.user)
    return Response(FavoriteTrackSerializer(favorites, many=True).data)

# -------- ALBUM --------
@api_view(["GET", "POST", "DELETE"])
def favorite_album(request, deezer_id: int):
    """
    POST   /favorite/album/<deezer_id>/  -> cria (global)
    DELETE /favorite/album/<deezer_id>/  -> remove (global)
    GET    /favorite/album/<deezer_id>/  -> retorna 1 favorito (global)
    """
    if request.method == "POST":
        r = requests.get(DEEZER_ALBUM_URL.format(id=deezer_id), timeout=10)
        if r.status_code != 200:
            return Response({"detail": "Deezer não encontrou esse álbum."}, status=404)
        data = r.json()

        fav, created = FavoriteAlbum.objects.get_or_create(
            deezer_id=deezer_id,
            user=request.user,
            defaults={
                "title": data.get("title", ""),
                "artist_name": (data.get("artist") or {}).get("name", ""),
                "cover": data.get("cover_medium") or data.get("cover"),
                "raw_json": data,
            },
        )
        serializer = FavoriteAlbumSerializer(fav)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    if request.method == "DELETE":
        deleted, _ = FavoriteAlbum.objects.filter(user=request.user, deezer_id=deezer_id).delete()
        if deleted == 0:
            return Response({"detail": "Favorito não encontrado."}, status=404)
        return Response(status=204)

    # GET único
    try:
        fav = FavoriteAlbum.objects.get(user=request.user, deezer_id=deezer_id)
    except FavoriteAlbum.DoesNotExist:
        return Response({"detail": "Favorito não encontrado."}, status=404)
    return Response(FavoriteAlbumSerializer(fav).data)

@api_view(["GET"])
def favorite_album_all(request):
    """GET /favorite/album/ -> lista global (sem usuário)"""
    favorites = FavoriteAlbum.objects.filter(user=request.user)
    return Response(FavoriteAlbumSerializer(favorites, many=True).data)

