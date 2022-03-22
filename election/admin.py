from django.contrib import admin

from .models import Conseil, Bureau, Candidat

# Register your models here.
admin.site.register([Bureau, Candidat])
