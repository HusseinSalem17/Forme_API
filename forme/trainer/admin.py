from django.contrib import admin

from .models import Program, Trainer, Workout

# Register your models here.
admin.site.register(Trainer)
admin.site.register(Program)
admin.site.register(Workout)
