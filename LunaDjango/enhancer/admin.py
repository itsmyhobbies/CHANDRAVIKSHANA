from django.contrib import admin
from .models import UploadedImage

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'original', 'enhanced', 'uploaded_at')
    search_fields = ('id', 'uploaded_at')
    readonly_fields = ('enhanced', 'uploaded_at')