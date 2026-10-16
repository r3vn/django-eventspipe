import hashlib
from django.db import models, transaction


class ArtifactManager(models.Manager):
    
    def get_or_create_artifact(self, data: bytes) -> "Artifact":
        # Compute the MD5 checksum of the data
        md5sum = hashlib.md5(data).hexdigest()

        with transaction.atomic():
            # Attempt to fetch the Artifact with a row lock
            artifact = self.select_for_update().filter(md5sum=md5sum).first()
            if artifact:
                return artifact
            
            # If no existing Artifact, create and save a new one
            artifact = self.create(data=data, md5sum=md5sum)
            artifact.save()
        
        return artifact


class Artifact(models.Model):
    data = models.BinaryField(blank=True)
    md5sum = models.CharField(max_length=32, blank=True, editable=False, unique=True)

    objects = ArtifactManager()

    @property
    def size(self) -> float:
        """
        Get size in KB of a file
        """
        return len(self.data) / 1000
