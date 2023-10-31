from django.contrib import admin

from .models import Comment, Title, Category, Genre, Review
from users.models import MyUser


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('name', 'year',)
    filter_horizontal = ('genre',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'confirmation_code',
                    'first_name',
                    'last_name',
                    'bio',
                    'role',)
    search_fields = ('username',)
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(MyUser, UserAdmin)
