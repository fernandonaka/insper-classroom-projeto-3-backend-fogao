from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .models import Note
from .serializers import NoteSerializer

@api_view(['GET', 'PUT','DELETE'])
def api_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404()
    
    if request.method == 'GET':
        serialized_note = NoteSerializer(note)
        return Response(serialized_note.data)

    if request.method == 'PUT':
        new_note_data = request.data
        note.title = new_note_data['title']
        note.content = new_note_data['content']
        note.save()
        serialized_note = NoteSerializer(note)
        return Response(serialized_note.data)
    
    elif request.method == 'DELETE':
        note.delete()
        return Response(status=204)
    

@api_view(['GET', 'POST'])
def api_all_notes(request): 
    if request.method == 'GET':
        notes=Note.objects.all()
        serialized_notes = NoteSerializer(notes,many=True)
        return Response(serialized_notes.data)

    if request.method == 'POST':
        new_note=NoteSerializer(data=request.data)
        new_note.is_valid(raise_exception=True)
        new_note.save()

        notes=Note.objects.all()
        serialized_notes = NoteSerializer(notes,many=True)
        return Response(serialized_notes.data)



    