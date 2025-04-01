import json

from django.core.management.base import BaseCommand

from delivery_points.models import Street, Area


class Command(BaseCommand):
    help = 'Загружает список улиц из test_data/delivery_point.json и список зон из test_data/areas.txt'  # noqa

    def handle(self, *args, **kwargs):
        try:
            with open('test_data/areas.txt') as f:
                for name in f:
                    _, created = Area.objects.get_or_create(name=name.strip())
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f'Зона {name.strip()} создана'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка загрузки: {e}'))

        try:
            with open('test_data/delivery_point.json', 'r', encoding='utf-8') as f:  # noqa
                data = json.load(f)
            products = [
                Street(name=item['name'], cost=item['cost'], area_id=item['area'])  # noqa
                for item in data
            ]
            Street.objects.bulk_create(products, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(
                f'Успешно загружено {len(products)} улиц'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка загрузки: {e}'))
