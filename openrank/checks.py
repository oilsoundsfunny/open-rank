from django.conf import settings
from django.core.checks import Error, register
from pathlib import Path

from .models import *

@register()
def engine_artifact_check(app_configs, **kwargs):

    errors = []
    for engine in Engine.objects.filter(disabled=False):
        if not (Path(settings.ENGINE_ARTIFACT_DIR) / engine.tarball_name()).exists():
            errors.append(
                Error(
                    'Missing %s' % (engine.tarball_name()),
                    hint='Expected to find %s' % (engine.tarball_name()),
                    obj=engine,
                )
            )

    return errors

@register()
def book_artifact_check(app_configs, **kwargs):

    errors = []
    for rating_list in RatingList.objects.all():
        if not (Path(settings.BOOK_ARTIFACT_DIR) / rating_list.book_artifact()).exists():
            errors.append(
                Error(
                    'Missing %s for %s' % (rating_list.book_artifact(), rating_list),
                    hint='Expected to find %s' % (rating_list.book_artifact()),
                    obj=rating_list,
                )
            )

    return errors

