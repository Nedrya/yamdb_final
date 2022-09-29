import random
import string

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUserManager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        user = super().create_superuser(username, email, password,
                                        **extra_fields)
        user.role = 'admin'
        user.save()
        return user


class User(AbstractUser):
    """Класс пользователей"""
    USER, MODERATOR, ADMIN = 'user', 'moderator', 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=10,
        default=''.join(random.sample(string.ascii_letters + string.digits,
                        10)),
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Genre (models.Model):
    """Модель жанра"""
    name = models.CharField(max_length=200, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='slugs',
                            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug'
            )
        ]

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""
    name = models.CharField(max_length=200, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='slugs',
        verbose_name='Жанр',
        help_text='Жанр отзыва',
    )
    category = models.ForeignKey(
        'Categories',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='slugs',
        verbose_name='Категории',
        help_text='Категории отзыва',
    )

    def __str__(self):
        return self.name[:15]


class Categories (models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=256, verbose_name='Название категорий')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='slugs',
                            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slugs'
            )
        ]

    def __str__(self):
        return self.slug


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(verbose_name='Дата комментария',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text}'
