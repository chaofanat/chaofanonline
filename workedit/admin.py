from django.contrib import admin
from django.http import HttpRequest

# Register your models here.

from .models import Novel,Chapter,AIapi,Uploadnovel
from typing import Any
from django.conf import settings

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(AIapi)


"""
class NovelAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'status', 'created_time')

admin.site.register(Novel, NovelAdmin)
"""
import os
@admin.register(Uploadnovel)
class UploadnovelAdmin(admin.ModelAdmin):
    list_display = ("id", "file_name", "file_path", "user", "enable", "check_result")
    list_display_links = ("id", "file_name", "user",  "enable", "check_result")
    search_fields = ("file_name",)
    list_filter = ("enable", "check_result")

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        baseurl = settings.STATICFILES_DIRS[0]
        if not settings.DEBUG:
            baseurl = settings.STATIC_ROOT
        path = os.path.join(baseurl , obj.file_path)
        if os.path.exists(path):
            os.remove(path)
        return super().delete_model(request, obj)
    
    actions = ["delete_model"]
