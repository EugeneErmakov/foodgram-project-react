from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[RegexValidator('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')],
        verbose_name='Цвет')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.FileField(
        upload_to='recipe_pic/',
        verbose_name='Изображение'
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=(
            MinValueValidator(1, message='Минимальное время приготовления - 1 минута'),
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='tag_recipes',
                            verbose_name='Тэг')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_tags',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Тег для рецепта'
        verbose_name_plural = 'Теги для рецептов'

    def __str__(self):
        return f'Тег "{self.tag}" для рецепта "{self.recipe}"'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(
            1, message='Нельзя создать рецепт без ингредиентов'),
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'Ингредиент "{self.ingredient}" для рецепта {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт из избранного'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipes'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart_user_recipes'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
