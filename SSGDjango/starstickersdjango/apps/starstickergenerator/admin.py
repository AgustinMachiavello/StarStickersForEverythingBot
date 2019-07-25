from django.contrib import admin
from .models import GeneratedImage, CorpusRecord

# Register your models here.
admin.site.register(GeneratedImage)
admin.site.register(CorpusRecord)
