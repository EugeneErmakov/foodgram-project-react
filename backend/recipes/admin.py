from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('favorite_count',)

    @staticmethod
    def favorite_count(obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(Cart)
