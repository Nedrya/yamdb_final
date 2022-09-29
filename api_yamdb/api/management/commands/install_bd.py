import csv

from django.core.management.base import BaseCommand

from reviews.models import Categories, Comment, Genre, Review, Title, User

CSV_FILES = {
    'users': User,
    'category': Categories,
    'genre': Genre,
    'titles': Title,
    'review': Review,
    'comments': Comment,
}


class Command(BaseCommand):
    help = 'Импорт данных из .csv файла'

    def handle(self, *args, **options):
        for file, model in CSV_FILES.items():
            with open(
                f'static/data/{file}.csv',
                newline='',
                encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'category' in row:
                        category = Categories.objects.get(pk=row['category'])
                        row['category'] = category
                    if 'author' in row:
                        row['author'] = User.objects.get(pk=row['author'])
                    if 'review_id' in row:
                        if file == 'comments':
                            row['review_id'] = int(row['review_id'])
                        else:
                            review = Review.objects.get(pk=row['review_id'])
                            row['review_id'] = review
                    model.objects.create(**row)
        self.add_genres_to_titles()

    def add_genres_to_titles(self):
        with open(
            'static/data/genre_title.csv',
            newline='',
            encoding='utf-8'
        ) as genre_title:
            reader = csv.DictReader(genre_title)
            for row in reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)
