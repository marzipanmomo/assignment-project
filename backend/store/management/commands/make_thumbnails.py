from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps

size = 160

class Command(BaseCommand):
    help = "Create small square thumbnails of product images in media/thumbs/"
    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='rebuild existing thumbnails')

    def handle(self, *args, **options):
        src_dir = Path(settings.MEDIA_ROOT) / 'products'
        out_dir = Path(settings.MEDIA_ROOT) / 'thumbs'
        out_dir.mkdir(parents=True, exist_ok=True)
        made = skipped = 0

        for src in sorted(src_dir.glob('*')):
            if src.suffix.lower() not in {'.jpg', '.jpeg'}:
                continue
            dest = out_dir / src.name
            if dest.exists() and not options['force']:
                skipped += 1
                continue
            with Image.open(src) as img:
                img = ImageOps.exif_transpose(img).convert('RGB')
                ImageOps.fit(img, (SIZE, SIZE)).save(dest, format='JPEG', quality=80, optimize=True)
            made += 1

        self.stdout.write(self.style.SUCCESS(f"Thumbnails: {made} created, {skipped} already existed."))