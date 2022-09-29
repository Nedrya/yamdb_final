import datetime as dt

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import MAIL
from reviews.models import Categories, Genre, Title, User, Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['confirmation_code'] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['username'] = user.username
        token['confirmation_code'] = user.confirmation_code
        return {'token': str(token.access_token)}

    def validate(self, attrs):
        user = get_object_or_404(
            User,
            username=attrs['username'],
        )
        try:
            user = User.objects.get(
                username=attrs['username'],
                confirmation_code=attrs['confirmation_code'],
            )
            return self.get_token(user)
        except Exception:
            raise ValidationError('Неверный код')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        read_only=True,
    )
    confirmation_code = serializers.CharField(
        read_only=True,
    )
    bio = serializers.CharField(
        read_only=True,
    )

    class Meta:
        fields = ('id', 'email', 'username', 'role',
                  'confirmation_code', 'bio')
        model = User
        read_only_fields = ('role', 'bio')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.save()
        send_mail(
            'Confirmation code',
            f'{user.confirmation_code}',
            MAIL,
            [validated_data['email']],
            fail_silently=False,
        )
        return user

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Нельзя создать пользователя me')
        return value


class UsersSerializer(serializers.ModelSerializer):
    """Информация о пользователях"""
    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name',
                  'role', 'bio')
        model = User


class GenreSerializer(serializers.ModelSerializer):
    """Показ жанра"""
    name = serializers.CharField(required=False)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorieSerializer(serializers.ModelSerializer):
    """Показ категорий"""
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class PostTitlesSerializer(serializers.ModelSerializer):
    """Добавление публикаций"""
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True,
                                         required=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Categories.objects.all(),
                                            required=True)
    description = serializers.CharField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('rating',)

    def validate_year(self, value):
        """Проверка года"""
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год должен быть меньше или равен текущему')
        return value


class TitlesSerializer(serializers.ModelSerializer):
    """Чтение публикаций"""
    genre = GenreSerializer(required=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True)
    category = CategorieSerializer(required=True)
    description = serializers.CharField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('rating',)
