from django.contrib import admin
from .models import Ingredient, IngredientReciepe, Tag, Recipe, ShoppingCart, Favorites



class IngredientReciepeInline(admin.TabularInline):
    model = IngredientReciepe
    min_num = 1
    extra = 1


class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    inlines = (IngredientReciepeInline,)
    empty_value_display = '-пусто-'


class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipes',
    )
    search_fields = (
        'user',
        'recipes',
    )
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipes',
    )
    search_fields = (
        'user',
        'recipes',
    )

admin.site.register(Ingredient, IngridientAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Tag, TagAdmin)