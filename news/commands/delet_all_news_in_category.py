from django.core.management.base import BaseCommand, CommandError
from ..models import Post_news, Category_news


class Command(BaseCommand):
    help = 'Удалит все записи в данной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category_news.objects.get(name=options['category'])
                Post_news.objects.filter(postCategory__name=category.name).delete()
                self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
            except Category_news.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {category}'))
