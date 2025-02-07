from django.db import models

# Create your models here.


class Gif(models.Model):
    default_gif = models.FileField(upload_to='banner/', blank=True, null=True)

    class Meta:
        db_table = 'gif_app_gif'
        verbose_name = 'Gif'
        verbose_name_plural = 'Gifs'