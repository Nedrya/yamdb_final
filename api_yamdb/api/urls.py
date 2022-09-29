from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('auth/signup', views.UserViewSet, basename='signup')
router_v1.register('users', views.UsersViewSet, basename='users')
router_v1.register('titles', views.TitlesList, basename='titles')
router_v1.register('genres', views.GenreList, basename='genreList')
router_v1.register(
    'categories',
    views.CategoriesList,
    basename='categoriesList'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/categories/<str:slug>/', views.SlugCategoriesDel.as_view()),
    path('v1/genres/<str:slug>/', views.SlugGenreDel.as_view()),
    path(
        'v1/auth/token/',
        views.UserTokenObtainPairView.as_view(),
        name='token'
    ),
    path('v1/', include(router_v1.urls)),
]
