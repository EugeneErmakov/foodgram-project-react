from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from users.models import Follow, User

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, CustomUserSerializer,
                          IngredientSerializer, RecipeSerializer,
                          RecipeShortInfoSerializer, SubscriptionSerializer,
                          TagSerializer)
from .utils import download_shopping_list


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=('GET',),
            url_path='subscriptions', detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=('POST', 'DELETE'),
            url_path='subscribe', detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        if request.method == 'POST':
            subscription = Follow.objects.create(
                user=user, author=get_object_or_404(User, id=id))
            serializer = SubscriptionSerializer(
                subscription,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            author = self.get_object()
            deleted = Follow.objects.get(
                user=user, author=author).delete()
            if deleted:
                return Response({
                    'message': 'Вы отписались от этого автора'},
                    status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Recipe.objects.annotate(
                is_favorited=Exists(
                    Favorite.objects.filter(
                        user=self.request.user,
                        recipe__pk=OuterRef('pk')
                    )
                ),
                is_in_shopping_cart=Exists(
                    Cart.objects.filter(
                        user=self.request.user,
                        recipe__pk=OuterRef('pk')
                    )
                )
            )
        else:
            queryset = Recipe.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateRecipeSerializer
        if self.action in ('shopping_cart', 'favorite'):
            return RecipeShortInfoSerializer
        return self.serializer_class

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self.update(request, *args, **kwargs)

    def _recipe_processing(self, request, model, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_object = model.objects.filter(user=request.user,
                                               recipe=recipe)
        if request.method == 'POST':
            if favorite_object.exists():
                raise serializers.ValidationError(
                    {'errors': 'Рецепт уже добавлен.'}
                )
            model.objects.create(user=request.user, recipe=recipe)
            return Response(self.get_serializer(recipe).data,
                            status=status.HTTP_201_CREATED)

        if not favorite_object.exists():
            raise serializers.ValidationError(
                {'errors': "Данный рецепт не добавлен."}
            )
        favorite_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        return self._recipe_processing(request, Favorite, kwargs['pk'])

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        return self._recipe_processing(request, Cart, kwargs['pk'])

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        if not request.user.cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return download_shopping_list(request)
