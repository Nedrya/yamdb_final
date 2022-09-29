from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api import filter, permissions, serializers
from reviews.models import Categories, Genre, Review, Title, User


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.UserTokenObtainPairSerializer


class UserViewSet(CreateViewSet):
    """Создание пользователя"""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            'email': serializer.data['email'],
            'username': serializer.data['username'],
        }
        return Response(
            data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Работа с пользователями"""
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = (permissions.Admin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            if request.user.role == 'user' and 'role' in request.data:
                serializer = self.get_serializer(request.user)
                return Response(serializer.data)
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class TitlesList(viewsets.ModelViewSet):
    """Посты"""
    queryset = Title.objects.all().annotate(Avg("reviews__score"))
    serializer_class = serializers.TitlesSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = filter.TitlesFilters
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Разделение сериализаторов POST и GET"""
        if self.request.method == 'GET':
            return serializers.TitlesSerializer
        return serializers.PostTitlesSerializer

    def get_permissions(self):
        """Разделение пермишена POST, PATCH и GET"""
        if self.request.method == 'POST' or 'PATCH':
            return (permissions.IsAdminOrReadOnly(),)
        return super().get_permissions()


class GenreList(viewsets.ModelViewSet):
    """Жанр"""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_permissions(self):

        if self.request.method == 'POST':
            return (permissions.Admin(),)
        return super().get_permissions()


class SlugGenreDel(APIView):
    """Удаление жанров"""
    def delete(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        return (permissions.Admin(),)


class SlugCategoriesDel(APIView):
    """Удаление жанров"""
    def delete(self, request, slug):
        category = get_object_or_404(Categories, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        return (permissions.Admin(),)


class CategoriesList(viewsets.ModelViewSet):
    """Категории"""
    serializer_class = serializers.CategorieSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        queryset = Categories.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

    def get_permissions(self):

        if self.request.method == 'POST':
            return (permissions.Admin(),)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAuthorAdminModeratorOrReadOnly)
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAuthorAdminModeratorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()
