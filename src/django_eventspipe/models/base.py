import uuid

from django.db import models


class UUID4Model(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True

    @property
    def short_uuid(self) -> str:
        """
        return short uuid
        """
        return str(self.pk).split("-")[0]
