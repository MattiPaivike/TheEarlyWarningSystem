from django.db import models

class Software(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Version(models.Model):
    version = models.CharField(max_length=50)
    dllink = models.CharField(max_length=300, blank=True)
    dllink_x86 = models.CharField(max_length=300, blank=True)
    dllink_x64 = models.CharField(max_length=300, blank=True)

    checksum = models.CharField(max_length=300, blank=True)
    checksum_x86 = models.CharField(max_length=300, blank=True)
    checksum_x64 = models.CharField(max_length=300, blank=True)
    checksum_type = models.CharField(max_length=50, blank=True)

    lastupdated = models.CharField(max_length=50, blank=True)

    software = models.ForeignKey(Software, on_delete=models.CASCADE)

    class Meta:
        ordering = ('software',)
        get_latest_by = "order_date"

    def __str__(self):
        return self.version
