import logging
from uuid import uuid4

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    uuid = models.UUIDField(default=uuid4, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
