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
                    'Missing %s for %s' % (engine.tarball_name(), engine.name),
                    hint='Expected to find %s' % (engine.tarball_name()),
                    obj=engine,
                    id="engines.E001",
                )
            )

    return errors
