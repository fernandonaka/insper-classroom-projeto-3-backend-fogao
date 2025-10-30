from django.urls import path

from . import views

urlpatterns = [
    path('search/artist/', views.search_artists),
    path('search/track/',views.search_tracks),
    
    
    path('favorite/artist/<int:deezer_id>/', views.favorite_artist),
    path('favorite/track/<int:deezer_id>/', views.favorite_track),
    
    #rotas para mostrar todos os favoritos e todas as tracks
    path('favorite/artist/', views.favorite_artist_all),
    path('favorite/track/', views.favorite_track_all)
]
