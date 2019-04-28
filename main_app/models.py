from django.db import models

# Create your models here.
class Software(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Version(models.Model):
    version = models.CharField(max_length=50)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)

    class Meta:
        ordering = ('software',)
        get_latest_by = "order_date"

    def __str__(self):
        return self.version
