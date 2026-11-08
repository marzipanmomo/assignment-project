import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Category, Product

CSV_PATH = Path(__file__).resolve().parents[2] / 'data' / 'products.csv'

class Command(BaseCommand):
    help = "Important categories and product from store/data/products.csv"

    def handle(self, *args, **options):
        created, updated, missing_images = 0, 0, []

        # utf-8-sig strips the hidden character excel adds to the first header
        with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                name = (row.get('name') or '').strip()
                if not name: #skip blank rows
                    continue

                product, was_created = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        'description': (row['description'] or '').strip(),
                        'price': row['price'].strip(),
                        'option': (row['filters/options' or '']).strip(),
                        'is_featured': row['featured'].strip().upper() == 'Y',
                        'image': f"products/{row['image file'].strip()}",
                    },
                )

                created += was_created
                updated += not was_created

                if not(Path(settings.MEDIA_ROOT) / product.image.name).exists():
                    missing_images.append(product.image.name)

                # room, aesthetic and product type are the categories

                product.categories.clear()
                for column, group in [('room','room'),('aesthetic','aesthetic'),('product type','type')]:
                    for cat_name in (row[column] or '').split(';'):
                        cat_name = cat_name.strip()
                        if not cat_name:
                            continue

                        category, _ = Category.objects.get_or_create(
                            slug=slugify(cat_name),
                            defaults={'name': cat_name, 'group': group},
                        )
                        product.categories.add(category)

        self.stdout.write(self.style.SUCCESS(
            f"Done: {created} created, {updated} updated, "
            f"{Category.objects.count()} categories."
        ))

        if missing_images:
            self.stdout.write(self.style.WARNING(
                "Image files not found in media/: " + ", ".join(missing_images)
            ))