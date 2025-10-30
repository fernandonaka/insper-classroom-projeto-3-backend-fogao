from django.contrib import admin

# Register your models here.
from .models import Note, Tag


admin.site.register(Note)