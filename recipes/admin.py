from django.contrib import admin

from tag.models import Tag

from .models import Category, Recipe

# from django.contrib.contenttypes.admin import GenericStackedInline


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...

# Removing tag as GenericRelation of the contenttype

# class TagInLine(GenericStackedInline):
#    model = Tag
#    fields = 'name',
#    extra = 1  # qtd de campos que aparece em Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at'
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html'
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }
    autocomplete_fields = 'tags',
    # Removing tag as GenericRelation of the contenttype
    # inlines = [
    #    TagInLine,
    # ]


admin.site.register(Category, CategoryAdmin)
