from django.contrib import admin

# Register your models here.
from .models import Voice, Region_lan

#register the model so it will show up in the user interface
admin.site.register(Voice)
admin.site.register(Region_lan)