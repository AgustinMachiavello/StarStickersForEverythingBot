# Django Models
from django.db import models

# Date and time
from django.utils import timezone

# slugify
from django.utils.text import slugify

# Random generator library
import random

# hash libraries
import base64
import hashlib


class GeneratedImage(models.Model):
    """Generated star sticker image model"""
    # image = models.ImageField(null=True, blank=False) NOT implemented as disk space hosting is limited
    sentence = models.TextField(null=True, blank=False)
    slug = models.SlugField(null=False, default='default')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            string_to_hash = (
                    str(self.sentence) +
                    str(self.created_at) +
                    str(random.randint(1, 999)))
            hasher = hashlib.sha1(string_to_hash.encode('utf-8'))
            hash_code = base64.urlsafe_b64encode(hasher.digest()[:10])
            self.slug = slugify(str(hash_code))
        self.updated_at = timezone.now()
        return super(GeneratedImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class CorpusRecord(models.Model):
    """Data generated by corpus"""
    comments_count = models.PositiveIntegerField(null=True, blank=False, default=0)
    exception_count = models.PositiveIntegerField(null=True, blank=False, default=0)
    slug = models.SlugField(null=False, default='default')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            string_to_hash = (
                    str(self.comments_count) +
                    str(self.created_at) +
                    str(random.randint(1, 999)))
            hasher = hashlib.sha1(string_to_hash.encode('utf-8'))
            hash_code = base64.urlsafe_b64encode(hasher.digest()[:10])
            self.slug = slugify(str(hash_code))
        self.updated_at = timezone.now()
        return super(CorpusRecord, self).save(*args, **kwargs)

    def __str__(self):
        return "Count {0} | Exc {1} ({2})".format(self.comments_count, self.exception_count, self.slug)