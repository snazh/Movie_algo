from django.contrib import admin
from .models import UserMovie, Comment


class UserMovieAdmin(admin.ModelAdmin):
    list_display = ('user', 'movieID',)
    list_editable = ('movieID',)
    list_filter = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'movieID', 'created_time')
    list_editable = ('content',)
    list_filter = ('user',)


admin.site.register(UserMovie, UserMovieAdmin)
admin.site.register(Comment, CommentAdmin)
