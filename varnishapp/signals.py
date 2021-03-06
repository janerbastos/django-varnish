from django.db.models.signals import post_save
from django.db.models import get_model
from django.conf import settings
from manager import manager

def absolute_url_purge_handler(sender, **kwargs):
    manager.run('purge.url', r'^%s$' % kwargs['instance'].get_absolute_url(), secret=getattr(settings, 'VARNISH_SECRET', None))

for model in getattr(settings, 'VARNISH_WATCHED_MODELS', ()):
    post_save.connect(absolute_url_purge_handler, sender=get_model(*model.split('.')))

def global_purge_handler(sender, **kwargs):
    manager.run('purge.url', r'.*', secret=getattr(settings, 'VARNISH_SECRET', None))

for model in getattr(settings, 'VARNISH_GLOBAL_WATCHED_MODELS', ()):
    post_save.connect(global_purge_handler, sender=get_model(*model.split('.')))
