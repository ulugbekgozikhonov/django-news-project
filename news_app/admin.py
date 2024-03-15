from django.contrib import admin
from news_app.models import Category, News, Contact, Comment


# Register your models here.

# admin.site.register(News)
# admin.site.register(Category)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish_time', 'status']
    list_filter = ['status', 'created_time', 'publish_time']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'enable_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def enable_comments(self, request, queryset):
        queryset.update(active=True)
