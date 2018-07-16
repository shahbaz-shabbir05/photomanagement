from _datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from photomanagement import settings


class Gallery(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        ordering = ('title',)

    def __str__(self):
        return self.title


def upload_photos(instance, filename):
    now_time = datetime.now().microsecond
    return '{}/{}'.format("Photos", '%s.jpg' % now_time)


class Photo(models.Model):
    title = models.CharField(_('title'), max_length=200)
    image = models.ImageField(_('image'), upload_to=upload_photos, null=True, blank=True)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
        ordering = ('title',)

    def __str__(self):
        return self.title
