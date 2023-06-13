from django.db.models import Sum
from django.http.response import HttpResponse

from recipes.models import RecipeIngredient


def download_shopping_list(request):
    ingredients = RecipeIngredient.objects.filter(
        recipe__cart__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(amount=Sum('amount')).order_by('ingredient__name')
    shopping_list = 'Список покупок:\n\n'
    shopping_list += '\n'.join([
        f'- {ingredient["ingredient__name"]} {ingredient["amount"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients
    ])
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    return response
