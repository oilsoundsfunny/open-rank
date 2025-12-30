import os
import django
import csv
from django.utils.dateparse import parse_date

# --- 0. Setup Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opensite.settings')
django.setup()

from openrank.models import *

FAMILIES_CSV = 'families.csv'
ENGINES_CSV = 'engines.csv'

# --- 1. Import families ---
with open(FAMILIES_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        EngineFamily.objects.get_or_create(
            name=row['name'],
            defaults={
                'author': row['author'],
                'website': row['website'],
            },
        )

# --- 2. Import engines ---
with open(ENGINES_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            family = EngineFamily.objects.get(name=row['family'])
        except EngineFamily.DoesNotExist:
            print('Skipping engine %s — family \'%s\' not found' % (row['version'], row['family']))
            continue

        Engine.objects.get_or_create(
            family=family,
            version=row['version'],
            defaults={
                'release_date': parse_date(row['release_date']),
                'nps': int(row['nps']),
                'latest': False,
            },
        )

# --- 3. Mark latest engine per family ---
Engine.objects.update(latest=False)

for family in EngineFamily.objects.all():
    latest_engine = (
        Engine.objects
        .filter(family=family, release_date__isnull=False)
        .order_by('-release_date')
        .first()
    )
    if latest_engine:
        latest_engine.latest = True
        latest_engine.save(update_fields=['latest'])
        print('Marked latest engine %s for family %s' % (latest_engine.version, family.name))

# --- 4. Add all Engines to all rating lists ---

for rating_list in RatingList.objects.all():
    rating_list.engines.add(*Engine.objects.all())

print('Import complete.')
