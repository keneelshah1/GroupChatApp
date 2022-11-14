from django.contrib import admin
from .models import UserData, Tasks, PhotoData, Tags, Phototag
# Register your models here.

admin.site.register(UserData)
admin.site.register(Tasks)
admin.site.register(PhotoData)
admin.site.register(Phototag)
admin.site.register(Tags)