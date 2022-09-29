from django_filters import filters, FilterSet

from reviews.models import Title


class TitlesFilters(FilterSet):
    """Фильтр сортировки"""
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='icontains')
    name = filters.CharFilter(field_name='name',
                              lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
