from django.contrib import admin

from gif_app.models import Gif


# Register your models here.


class gifAdmin(admin.ModelAdmin):
    model = Gif


admin.site.register(Gif, gifAdmin)