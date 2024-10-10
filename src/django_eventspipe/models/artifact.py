import hashlib
from django.db import models

class Artifact(models.Model):
    data       = models.BinaryField(blank=True)
    md5sum     = models.CharField(max_length=32, blank=True, editable=False, unique=True)  # Unique MD5 checksum

    @classmethod
    def get_or_create(cls, data:bytes) -> object:
        # Compute the MD5 checksum of the data
        md5sum = hashlib.md5(data).hexdigest()

        if cls.objects.filter(md5sum=md5sum).exists():
            return cls.objects.get(md5sum=md5sum)

        file = cls(data=data,md5sum=md5sum)
        file.save()

        return file
        
    @property
    def size(self) -> float:
        """
        Get size in KB of a file
        """
        return len(self.data) / 1000
