import hashlib
import uuid

from django.db import models, transaction

class Artifact(models.Model):
    uuid   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data   = models.BinaryField(blank=True)
    md5sum = models.CharField(max_length=32, editable=False, unique=True)

    @classmethod
    def get_or_create(cls, data: bytes) -> "Artifact":
        # Compute the MD5 checksum of the data
        md5sum = hashlib.md5(data).hexdigest()

        with transaction.atomic():
            # Attempt to fetch the Artifact with a row lock
            artifact = cls.objects.select_for_update().filter(md5sum=md5sum).first()
            if artifact:
                return artifact
            
            # If no existing Artifact, create and save a new one
            artifact = cls(data=data, md5sum=md5sum)
            artifact.save()
        
        return artifact

    @property
    def size(self) -> float:
        """
        Get size in KB of a file
        """
        return len(self.data) / 1000
