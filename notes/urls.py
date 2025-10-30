from django.urls import path

from . import views

urlpatterns = [
    path('notes/<int:note_id>/', views.api_note),
    path('notes/',views.api_all_notes)
]
