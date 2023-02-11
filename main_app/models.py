from django.db import models


# Create your models here.
class Movie(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'deactivate'),
        ('3', 'delete')
    )

    name = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='Movie-thumbnail', blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    actor = models.CharField(max_length=100, blank=True, null=True)
    writer = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)

    def __str__(self):
        return str(self.name)
